# Generated by Django 5.0.6 on 2024-06-22 23:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0025_profile_is_completed'),
    ]

    operations = [
        migrations.CreateModel(
            name='UMKM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_umkm', models.CharField(max_length=50)),
                ('deskripsi_singkat', models.TextField()),
                ('industri', models.CharField(choices=[('perdagangan', 'Perdagangan'), ('jasa', 'Jasa'), ('kuliner', 'Kuliner'), ('pertanian', 'Pertanian dan Perkebunan'), ('konstruksi', 'Konstruksi dan Properti'), ('kerajinan', 'Kerajinan dan Souvenir'), ('fashion', 'Fashion dan Tekstil'), ('perikanan', 'Perikanan dan Kelautan')], max_length=100)),
                ('ukuran_pasar', models.CharField(max_length=100)),
                ('target_pelanggan', models.CharField(max_length=100)),
                ('jangka_pengembalian', models.CharField(max_length=100)),
                ('target_dana', models.IntegerField()),
                ('proyeksi_imbal_hasil', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('foto_umkm', models.ImageField(upload_to='umkm_photos/')),
                ('prospektus', models.FileField(upload_to='umkm_prospektus/')),
                ('nomor_telepon', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Nomor telepon harus dalam format internasional tanpa tanda '+', contoh: 6281234567890", regex='^\\d{9,15}$')])),
                ('linkedin', models.URLField(blank=True)),
                ('instagram', models.URLField(blank=True)),
                ('harga_sukuk', models.IntegerField(default=10000)),
                ('jenis_bagi_hasil', models.CharField(choices=[('mudharabah', 'Mudharabah (Pendanaan hanya oleh investor)'), ('musyarakah', 'Musyarakah (Pendanaan investor dan pemilik umkm)')], default='mudharabah', max_length=50)),
            ],
        ),
    ]