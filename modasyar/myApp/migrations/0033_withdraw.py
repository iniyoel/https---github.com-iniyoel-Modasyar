# Generated by Django 5.0.6 on 2024-06-23 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0032_remove_ewallet_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tarik_saldo', models.IntegerField(null=True)),
            ],
        ),
    ]
