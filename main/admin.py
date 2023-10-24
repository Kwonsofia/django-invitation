from django.contrib import admin
from .models import WeddingMain, Phone, Account, Address, Photos

# Register your models here.
admin.site.register(WeddingMain)
admin.site.register(Phone)
admin.site.register(Account)
admin.site.register(Address)
admin.site.register(Photos)
