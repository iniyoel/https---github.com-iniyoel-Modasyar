from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal

# Create your models here.
class Profile(models.Model):
    # username = models.CharField(max_length=24, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.TextField(max_length=12, blank=True)
    last_name= models.TextField(max_length=12, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    money = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    is_completed = models.BooleanField(default=False)

    def _str_(self):
        return self.username
    
class Umkm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nama_umkm = models.CharField(max_length=50)
    deskripsi_singkat = models.TextField()
    
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
    
    industri = models.CharField(max_length=100, choices=industri_choices)
    ukuran_pasar = models.CharField(max_length=100)
    target_pelanggan = models.CharField(max_length=100)
    jangka_pengembalian = models.CharField(max_length=100)
    target_dana = models.IntegerField()
    proyeksi_imbal_hasil = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    foto_umkm = models.ImageField(upload_to='umkm_photos/')
    prospektus = models.FileField(upload_to='umkm_prospektus/')
    nomor_telepon = models.CharField(
        validators=[
            RegexValidator(
                regex=r'^\d{9,15}$',
                message="Nomor telepon harus dalam format internasional tanpa tanda '+', contoh: 6281234567890"
            )
        ],
        max_length=15,
        blank=True
    )
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    jenis_bagi_hasil_choices = [
        ('mudharabah', 'Mudharabah (Pendanaan hanya oleh investor)'),
        ('musyarakah', 'Musyarakah (Pendanaan investor dan pemilik umkm)'),
    ]
    harga_sukuk = models.IntegerField(default=10000)
    jenis_bagi_hasil = models.CharField(max_length=50, choices=jenis_bagi_hasil_choices, default='mudharabah')
    
    def __str__(self):
        return self.nama_umkm

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    umkm = models.ForeignKey(Umkm, on_delete=models.CASCADE)
    units_purcashed = models.PositiveIntegerField(null=True)
    total_investment = models.DecimalField(max_digits=22, decimal_places=2)
    transaction_date = models.DateField(default=timezone.now)
    total_payment = models.IntegerField(null=True)
    profit = models.DecimalField(max_digits=22, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.umkm.nama_umkm} - {self.transaction_date}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.profit = self.total_investment * (self.umkm.proyeksi_imbal_hasil / 100)
            
        self.user.profile.money -= self.total_payment
        self.user.profile.save()
        super().save(*args, **kwargs)

class EWallets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    SHOPEEPAY = 'ShopeePay'
    DANA = 'Dana'
    OVO = 'OVO'
    GOPAY = 'Gopay'

    WALLET_CHOICES = [
        (SHOPEEPAY, 'ShopeePay'),
        (DANA, 'Dana'),
        (OVO, 'OVO'),
        (GOPAY, 'Gopay'),
    ]

    wallet_number = models.CharField(max_length=100)
    wallet_type = models.CharField(max_length=20, choices=WALLET_CHOICES)

class Withdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tarik_saldo = models.IntegerField(null=True)
    
    def __str__(self):
        return f"Withdraw by {self.user.username}"
    
    def save(self, *args, **kwargs):
        profile = self.user.profile

        if profile.money < self.tarik_saldo:
            raise ValidationError("Insufficient funds for this withdrawal.")

        # Subtract the withdrawal amount from the user's balance
        profile.money -= self.tarik_saldo
        profile.save()

        super().save(*args, **kwargs)
    

class TopUp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"
     