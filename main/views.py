from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import WeddingMain, Phone, Account, Photo, Address, GuestBook
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
    guestbook = GuestBook.objects.filter(wedding_id=wedding_id).order_by('-reg_dtime')

    if not wedding:
        return render(request, 'main/error.html')
    
    photo_list = []
    for photo in photos:

        # if wedding_id not in photo.img.url:
        #     continue

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
        'date': wedding_date(wedding[0].wedding_date, wedding[0].wedding_time),
        'guestbook_list': guestbook
    }

    return render(request, 'main/invitation.html', data)

def guestbook(request):
    if request.method == 'POST':
        
        name = request.POST['name']
        message = request.POST['message']
        wedding_id = request.POST['wedding_id']
        passwd = request.POST['passwd']
        guestbook = GuestBook(name=name, message=message, wedding_id=wedding_id, passwd=passwd)
        guestbook.save()
        return HttpResponseRedirect('/')
