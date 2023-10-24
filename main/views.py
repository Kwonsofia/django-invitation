from django.shortcuts import render
from .models import WeddingMain, Phone, Account, Photo, Address
from .utils import wedding_date


# Create your views here.
def index(request, wedding_id):
    wedding = WeddingMain.objects.get(wedding_id=wedding_id)
    phone = Phone.objects.get(wedding_id=wedding_id)
    account = Account.objects.get(wedding_id=wedding_id)
    address = Address.objects.get(wedding_id=wedding_id)

    if not wedding:
        return render(request, 'main/error.html')

    data = {
        'info': wedding,
        'phone': phone,
        'account': account,
        'address': address,
        'date': wedding_date(wedding.wedding_date)
    }

    return render(request, 'main/index.html', data)
