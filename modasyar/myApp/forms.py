from django import forms
from .models import Profile, EWallets, Umkm, TopUp
from django.forms.widgets import DateInput
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number', 'birth_date']
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].input_formats = ['%Y-%m-%d']

class UMKMForm(forms.Form):
    nama_umkm = forms.CharField(label='Nama UMKM', max_length=100, required=True)
    deskripsi_singkat = forms.CharField(widget=forms.Textarea, label='Deskripsi Singkat', required=True)
    industri_choices = [
        ('perdagangan', 'Perdagangan'),
        ('jasa', 'Jasa'),
        ('kuliner', 'Kuliner'),
        ('pertanian', 'Pertanian dan Perkebunan'),
        ('konstruksi', 'Konstruksi dan Properti'),
        ('kerajinan', 'Kerajinan dan Souvenir'),
        ('fashion', 'Fashion dan Tekstil'),
        ('perikanan', 'Perikanan dan Kelautan'),
    ]
    industri = forms.ChoiceField(choices=industri_choices, label='Industri', required=True)
    ukuran_pasar = forms.CharField(label='Ukuran Pasar', max_length=100, required=True)
    target_pelanggan = forms.CharField(label='Target Pelanggan', max_length=100, required=True)
    jangka_pengembalian = forms.CharField(label='Jangka Pengembalian', max_length=100, required=True)
    target_dana = forms.IntegerField(label='Target Pengumpulan Dana', required=True)
    proyeksi_imbal_hasil = forms.DecimalField(
        label='Proyeksi Imbal Hasil (%)',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        widget=forms.NumberInput(attrs={'step': '0.01'}), required=True
    )
    foto_umkm = forms.ImageField(label='Foto UMKM (JPEG/PNG only)', required=True)
    prospektus = forms.FileField(label='Unggah Prospektus (PDF)', required=True)
    nomor_telepon = forms.CharField(label='Nomor Telepon', max_length=15, widget=forms.TextInput(attrs={'type': 'tel'}))
    linkedin = forms.URLField(label='LinkedIn', required=False)
    instagram = forms.URLField(label='Instagram', required=False)
    
    jenis_bagi_hasil_choices = [
        ('mudharabah', 'Mudharabah (Pendanaan hanya oleh investor)'),
        ('musyarakah', 'Musyarakah (Pendanaan investor dan pemilik umkm)'),
    ]
    harga_sukuk = forms.IntegerField(label='Harga Sukuk', required=True)
    jenis_bagi_hasil = forms.ChoiceField(choices=jenis_bagi_hasil_choices, label='Jenis Bagi Hasil', required=True)
    
class UMKMForm(forms.ModelForm):
    class Meta:
        model = Umkm
        exclude = ['user']
        fields = '__all__'

class EWalletForm(forms.ModelForm):
    class Meta:
        model = EWallets
        fields = ['wallet_number', 'wallet_type']
      
class WithdrawForm(forms.Form):
    tarik_saldo = forms.IntegerField(min_value=10000, label='Withdrawal Amount')

class TopUpForm(forms.Form):
    amount = forms.DecimalField(max_digits=22, decimal_places=2, min_value=0.01, label='', required=True)

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount
