from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, Umkm, Transaction, EWallets, Withdraw, TopUp
from .forms import UserProfileForm, UMKMForm, WithdrawForm, EWalletForm, TopUpForm
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
import json
from datetime import datetime
from django.utils import timezone
from django.db.models import Sum

def home(request): 
    return render(request, "Dashboard.html")

def homelogged(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None
    
    context = {
        'profile': profile,
    }
    return render(request, "Dashboard-logged.html", context)

def login(request):
    return render(request, "Login.html")

def explore(request):
    umkms = Umkm.objects.all()
    context ={
        'umkms' : umkms
    }
    return render(request, "exploreUmkm.html", context)

@login_required
def explorelogged(request):
    umkms = Umkm.objects.all()
    profile = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None
    
    context = {
        'profile': profile,
        'umkms' : umkms,
    }
    return render(request, "exploreUmkm-logged.html", context)

@login_required
def tingkatkanmodal(request):
    if request.method == 'POST':
        form = UMKMForm(request.POST, request.FILES)
        if form.is_valid():
            umkm = form.save(commit=False)
            umkm.user = request.user
            umkm.save()
            return redirect('umkmprofile', umkm_id=umkm.id)
    else:
        form = UMKMForm()

    profile = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None
    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, "tingkatkan-modal.html", context)

@login_required
def umkmprofile(request, umkm_id):
    umkm = Umkm.objects.get(pk=umkm_id)    
    profile = get_object_or_404(Profile, user=request.user)
    transaction = Transaction.objects.filter(umkm=umkm)

    context = {
        'profile': profile,
        'umkm': umkm,
        'transaction' : transaction,
    }
    return render(request, "profilUmkm.html", context)

@login_required
def transaction(request, umkm_id):
    umkm = get_object_or_404(Umkm, pk=umkm_id)
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        units= int(request.POST.get('units', 10))
        price_per_unit = umkm.harga_sukuk
        total_investment = units * price_per_unit
        total_payment = total_investment + 2000

        if profile.money >= total_payment:
            profile.money -= total_payment
            profile.save

            Transaction.objects.create(
                user = request.user,
                umkm = umkm,
                units_purcashed = units,
                total_payment = total_payment,
                total_investment = total_investment,
                transaction_date = timezone.now()
            )

            return redirect(reverse("explorelogged"))
    return render(request, 'transaksi.html', {'umkm':umkm, 'profile':profile})


@login_required
def withdrawForm(request):
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
    
    if request.method == 'POST':
        form = EWalletForm(request.POST)
        if form.is_valid():
            # Simpan instance EWallets dengan mengaitkannya dengan user yang saat ini login
            ewallet_instance = form.save(commit=False)  # Tunggu sebelum menyimpan untuk mengatur user_id
            ewallet_instance.user = request.user  # Atur user_id
            ewallet_instance.save()
            return redirect('withdraw')  # Ganti 'withdraw' dengan nama URL sebenarnya untuk halaman withdraw
    else:
        form = EWalletForm()

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'Withdraw-form.html', context)

@login_required
def withdraw(request):
    profile = None
    error_message = None
    
    # Ambil informasi profil dan e-wallet
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None
    
    ewallets = EWallets.objects.all()

    # Inisialisasi form default
    form = WithdrawForm()

    # Proses pengiriman form
    if request.method == 'POST':
        selected_ewallet = request.POST.get('account')
        
        # Pastikan e-wallet terpilih
        if not selected_ewallet:
            error_message = 'Pilih e-wallet terlebih dahulu.'
        else:
            form = WithdrawForm(request.POST)
            
            # Validasi form jika valid
            if form.is_valid():
                tarik_saldo = form.cleaned_data['tarik_saldo']
                
                # Periksa saldo cukup atau tidak
                if profile.money < tarik_saldo:
                    form.add_error('tarik_saldo', 'Dana tidak mencukupi untuk penarikan ini.')
                else:
                    # Buat objek Withdraw dan simpan
                    withdraw = Withdraw(user=request.user, tarik_saldo=tarik_saldo)
                    withdraw.save()
                    
                    return redirect('withdraw-success')  # Redirect ke halaman sukses setelah penarikan berhasil

    # Persiapkan konteks untuk merender template
    context = {
        'ewallets': ewallets,
        'profile': profile,
        'money': profile.money if profile else 0,
        'username': request.user.username,
        'form': form,  # Pastikan form diinisialisasi di sini untuk menghindari UnboundLocalError
        'error_message': error_message,
    }

    return render(request, 'Withdraw.html', context)
   
@login_required
def withdrawSuccess(request):
    # Pastikan ada cara untuk mendapatkan profile.id di sini, contoh:
    profile = request.user.profile  # Gantikan dengan cara yang sesuai untuk mendapatkan profile
    
    context = {
        'profile': profile,
    }
    return render(request, "Withdraw-berhasil.html", context)
@login_required
def userdetail(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if profile.is_completed:
        return redirect('userdashboard', profile_id=profile.id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            profile.is_completed = True
            profile.save()
            return redirect('userdashboard', profile_id=profile.id)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'user-profile-detail.html', {'form': form})

@login_required
def userdashboard(request, profile_id):
    profile = Profile.objects.get(id = profile_id)
    if profile:
        profile = get_object_or_404(Profile, id=profile_id)
        context ={
            'username': request.user.username,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'phone_number': profile.phone_number,
            'birth_date': profile.birth_date,
            'profile_id': profile_id,
        }
        return render(request, 'user-dashboard.html', context)
    else:
        return render(request, 'user-dashboard.html', context)

def aboutus(request):
    return render(request, "aboutUs.html")

@login_required
def aboutUslogged(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None
    
    context = {
        'profile': profile,
        'username': request.user.username
    }
    return render(request, "aboutUs-logged.html", context)

@login_required
def investporto(request):
    profile = None
    total_profit_all_transactions = 0

    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None
        
        # Menghitung total keuntungan dari semua transaksi
        total_profit_all_transactions = Transaction.objects.filter(user=request.user).aggregate(total_profit=Sum('profit'))['total_profit'] or 0

    context = {
        'profile': profile,
        'money': profile.money if profile else 0,
        'username': request.user.username,
        'profit_all_transactions': total_profit_all_transactions,
    }
    return render(request, "invest-portofolio.html", context)

def detailPorto(request):
    profile = None
    transactions = (
        Transaction.objects.filter(user=request.user)
        .values('umkm__id', 'umkm__nama_umkm', 'umkm__industri', 'umkm__proyeksi_imbal_hasil', 'umkm__foto_umkm')
        .annotate(total_investment=Sum('total_investment'), total_profit=Sum('profit'))
    )
    
    # Menghitung total keuntungan dari semua transaksi
    total_profit_all_transactions = Transaction.objects.filter(user=request.user).aggregate(total_profit=Sum('profit'))['total_profit'] or 0
    
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None
    
    context = {
        'profile': profile,
        'username': request.user.username,
        'transactions': transactions,
        'profit_all_transactions': total_profit_all_transactions,
    }
    return render(request, 'detail-porto.html', context)

@login_required
def growth(request):
    user_umkms = Umkm.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(umkm__in=user_umkms)
    profile = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None
    
    context = {
        'profile': profile,
        'user_umkms' : user_umkms,
        'transactions' : transactions,
    }
    return render(request, "bisnis-growth.html", context)

def topupOption(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None
    
    if request.method == 'POST':
        form = TopUpForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            # Simpan data top-up ke dalam database
            topup_instance = TopUp(user=request.user, amount=amount)
            topup_instance.save()
            
            # Tambahkan amount ke uang di profil pengguna
            try:
                profile = Profile.objects.get(user=request.user)
                profile.money += amount
                profile.save()
            except Profile.DoesNotExist:
                # Handle jika profil pengguna tidak ditemukan
                return render(request, 'opsi-topup.html', {'form': form, 'error_message': 'Profil tidak ditemukan.'})
            
            # Redirect ke halaman atau lakukan tindakan selanjutnya
            return redirect('investporto')  # Ganti 'investPorto' dengan nama URL yang sesuai
            
    else:
        form = TopUpForm()  # Ini akan menginisialisasi form untuk request method GET

    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, "opsi-topup.html", context)

@login_required
def topupPayment(request):
    payment_type = request.GET.get('type')
    profile = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None
    
    context = {
        'profile': profile,
        'payment_type' : payment_type,
    }
    return render(request, "pembayaran-topup.html", context)