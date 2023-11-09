from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import WeddingMain, Phone, Account, Photo, Address, GuestBook
from .utils import wedding_date


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def admin_user_info(wedding_id):
    wedding = WeddingMain.objects.filter(wedding_id=wedding_id)
    phone = Phone.objects.filter(wedding_id=wedding_id)
    account = Account.objects.filter(wedding_id=wedding_id)
    address = Address.objects.filter(wedding_id=wedding_id)
    photos = Photo.objects.filter(wedding_id=wedding_id)

    if not wedding:
        return None

    data = {
        'info': wedding[0],
        'phone': phone[0],
        'account': account[0],
        'address': address[0],
        'photos': photos,
        'date': wedding_date(wedding[0].wedding_date, wedding[0].wedding_time),
    }

    return data


# Admin
def admin_main(request):
    return render(request, 'main/admin/login.html')


def login(request):
    wedding_id = request.POST['wedding_id']
    pw = request.POST['pw']

    wedding = WeddingMain.objects.filter(wedding_id=wedding_id)

    if not wedding:
        messages.warning(request, '없는 유저입니다.')
        return render(request, 'main/admin/register.html')

    elif wedding[0].passwd != pw:
        messages.warning(request, '비밀번호가 틀렸습니다.')
        return render(request, 'main/admin/login.html')

    return mypage(request, wedding_id)


def register(request):
    return render(request, 'main/admin/register.html')


def mypage(request, wedding_id):
    result = admin_user_info(wedding_id)

    if not result:
        return render(request, 'main/admin/login.html')

    return render(request, 'main/admin/mypage.html', result)


# Invitation
def invitation(request, wedding_id):
    wedding = WeddingMain.objects.filter(wedding_id=wedding_id)
    phone = Phone.objects.filter(wedding_id=wedding_id)
    account = Account.objects.filter(wedding_id=wedding_id)
    address = Address.objects.filter(wedding_id=wedding_id)
    photos = Photo.objects.filter(wedding_id=wedding_id)
    guestbooks = GuestBook.objects.filter(wedding_id=wedding_id).order_by('-reg_dtime')

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

    guestbook_list = []
    for guestbook in guestbooks:

        if guestbook.message:
            guestbook_list.append(guestbook)
        if len(guestbook_list) >= 3:
            break

    data = {
        'info': wedding[0],
        'phone': phone[0],
        'account': account[0],
        'address': address[0],
        'main_image': main_image,
        'sub_image': sub_image,
        'photos': photo_list,
        'date': wedding_date(wedding[0].wedding_date, wedding[0].wedding_time),
        'guestbook_list': guestbook_list
    }

    return render(request, 'main/invitation.html', data)


def guestbook_list(request, wedding_id):
    guestbook = GuestBook.objects.filter(wedding_id=wedding_id).order_by('-reg_dtime')

    data = {
        'guestbook_list': guestbook,
    }

    return render(request, 'main/guestbook.html', data)


def guestbook(request):
    guestbook = GuestBook()

    if request.POST['message']:
        guestbook.name = request.POST['name']
        guestbook.message = request.POST['message']
        guestbook.wedding_id = request.POST['wedding_id']
        guestbook.passwd = request.POST['passwd']

        guestbook.save()

    return HttpResponseRedirect(f'/{guestbook.wedding_id}#comment')


def guestbook_delete(request, msg_id):
    wedding_id = request.POST['wedding_id']
    passwd = request.POST['passwd']

    guestbook = GuestBook.objects.get(wedding_id=wedding_id, msg_id=msg_id)

    if guestbook.passwd == passwd:
        guestbook.delete()
        messages.success(request, '삭제되었습니다.')
    else:
        messages.warning(request, '비밀번호가 틀렸습니다.')

    return HttpResponseRedirect(f'/{guestbook.wedding_id}#comment')


def guestbook_list_delete(request, msg_id):
    passwd = request.POST['passwd']

    guestbook = GuestBook.objects.get(msg_id=msg_id)

    if guestbook.passwd == passwd:
        guestbook.delete()
        messages.success(request, '삭제되었습니다.')
    else:
        messages.warning(request, '비밀번호가 틀렸습니다.')

    return HttpResponseRedirect(f'/{guestbook.wedding_id}/guestbook')
