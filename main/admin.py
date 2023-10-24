from django.contrib import admin
from .models import WeddingMain, Phone, Account, Address, Photo

# Register your models here.
class WeddingAdmin(admin.ModelAdmin):
    search_fields = ['wedding_id']


admin.site.register(WeddingMain, WeddingAdmin)
admin.site.register(Phone)
admin.site.register(Account)
admin.site.register(Address)
admin.site.register(Photo)
