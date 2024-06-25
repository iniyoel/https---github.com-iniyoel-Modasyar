from django.contrib import admin
from .models import Profile,  EWallets, Withdraw, Umkm, Transaction, TopUp

# Register your models here.
admin.site.register(Profile)
admin.site.register(Transaction)
admin.site.register(Umkm)
admin.site.register(EWallets)
admin.site.register(Withdraw)
admin.site.register(TopUp)