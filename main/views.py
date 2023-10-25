from django.shortcuts import render
from .models import WeddingMain, Phone, Account, Photo, Address
from .utils import wedding_date


# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def invitation(request, wedding_id):
    wedding = WeddingMain.objects.filter(wedding_id=wedding_id)
    phone = Phone.objects.filter(wedding_id=wedding_id)
    account = Account.objects.filter(wedding_id=wedding_id)
    address = Address.objects.filter(wedding_id=wedding_id)
    photos = Photo.objects.filter(wedding_id=wedding_id)

    if not wedding:
        return render(request, 'main/error.html')
    
    photo_list = []
    for photo in photos:

        if 'main_' in photo.img.url:
            main_image = photo.img
        elif 'sub_' in photo.img.url:
            sub_image = photo.img
        else:
            photo_list.append(photo.img)

    data = {
        'info': wedding[0],
        'phone': phone[0],
        'account': account[0],
        'address': address[0],
        'main_image': main_image,
        'sub_image': sub_image,
        'photos': photo_list,
        'date': wedding_date(wedding[0].wedding_date, wedding[0].wedding_time)
    }

    return render(request, 'main/invitation.html', data)
