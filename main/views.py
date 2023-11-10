from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import WeddingMain, Phone, Account, Photo, Address, GuestBook
from .utils import wedding_date
from datetime import datetime


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def admin_user_info(wedding_id):
    wedding = WeddingMain.objects.get(wedding_id=wedding_id)
    phone = Phone.objects.filter(wedding_id=wedding_id)
    account = Account.objects.filter(wedding_id=wedding_id)
    address = Address.objects.filter(wedding_id=wedding_id)
    photos = Photo.objects.filter(wedding_id=wedding_id)

    if not wedding:
        return None
    
    photo_list = []
    main_image = None
    sub_image = None
    for photo in photos:

        if wedding_id not in photo.img.url:
            continue

        if 'main_' in photo.img:
            main_image = photo.img
        elif 'sub_' in photo.img:
            sub_image = photo.img
        else:
            photo_list.append(photo.img)

    data = {
        'info': wedding,
        'phone': phone[0] if phone else None,
        'account': account[0] if account else None,
        'address': address[0] if address else None,
        'main_image': main_image,
        'sub_image': sub_image,
        'photos': photo_list,
        'date': wedding_date(wedding.wedding_date, wedding.wedding_time),
    }

    return data


# Admin
def login(request):
    if request.method == 'POST':
        wedding_id = request.POST['wedding_id']
        pw = request.POST['pw']

        wedding = WeddingMain.objects.filter(wedding_id=wedding_id)

        if not wedding:
            messages.warning(request, '없는 유저입니다.')
            return render(request, 'main/admin/register.html')

        elif wedding[0].passwd != pw:
            messages.warning(request, '비밀번호가 틀렸습니다.')
            return render(request, 'main/admin/login.html')

        return HttpResponseRedirect(f'/user/admin/mypage/{wedding_id}')

    else:
        return render(request, 'main/admin/login.html')

def register(request):
    if request.method == 'POST':
        wedding_id = request.POST.get('wedding_id')

        if WeddingMain.objects.filter(wedding_id=wedding_id):
            messages.warning(request, '이미 존재하는 유저입니다. 로그인 부탁드립니다.')
            return HttpResponseRedirect('/user/admin/login')

        wedding_main = WeddingMain(
            wedding_id=wedding_id,
            passwd=request.POST['passwd'],
            groom_name=request.POST['groom_name'],
            bride_name=request.POST['bride_name'],

            use_guestbook=request.POST.get('use_guestbook', False),
            wedding_date=request.POST['wedding_date'],
            wedding_time=request.POST['wedding_time'],
            reg_dtime=datetime.now(),
        )
        wedding_main.save()

        user_wedding = WeddingMain.objects.get(wedding_id=wedding_id)

        if not user_wedding:
            messages.warning(request, '회원 가입 실패')
            return render(request, 'main/admin/register.html')

        address = Address(
            wedding_id=user_wedding,
            address=request.POST['address'],
            address_tel=request.POST.get('address_tel'),

            kakaomap_timestamp=request.POST['kakaomap_timestamp'],
            kakaomap_key=request.POST['kakaomap_key'],
        )
        address.save()

        if request.FILES:
            main_image = request.FILES.get('main_image')
            sub_image = request.FILES.get('sub_image')

            if main_image:
                main_image.name = f'main_{wedding_id}_' + main_image.name
                Photo.objects.create(wedding_id=user_wedding, img=main_image)
            
            if sub_image:
                sub_image.name = f'sub_{wedding_id}_' + sub_image.name
                Photo.objects.create(wedding_id=user_wedding, img=sub_image)

            images = request.FILES.getlist('images')

            for image in images:
                image.name = f'{wedding_id}_' + image.name
                Photo.objects.create(wedding_id=user_wedding, img=image)

        messages.success(request, '회원 성공, 로그인해주세요 :)')
        return HttpResponseRedirect('/user/admin/login')
    else:
        return render(request, 'main/admin/register.html')


def mypage(request, wedding_id):
    wedding = WeddingMain.objects.get(wedding_id=wedding_id)

    if not wedding:
        messages.warning(request, '존재하지 않는 Wedding ID 입니다.')
        return render(request, 'main/admin/login.html')
    
    if request.method == 'POST':
        if request.FILES:
            images = request.FILES.getlist('images')

            for image in images:
                Photo.objects.create(wedding_id=wedding, img=image)

        messages.success(request, '수정 완료하였습니다. :)')

    result = admin_user_info(wedding_id)

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

    main_image = None
    sub_image = None
    for photo in photos:

        if wedding_id not in photo.img.url:
            continue

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
        'phone': phone[0] if phone else None,
        'account': account[0] if account else None,
        'address': address[0] if address else None,
        'main_image': main_image,
        'sub_image': sub_image,
        'photos': photo_list,
        'date': wedding_date(wedding[0].wedding_date, wedding[0].wedding_time),
        'is_guestbook_use': wedding[0].use_guestbook,
        'guestbook_list': guestbook_list
    }

    return render(request, 'main/invitation.html', data)


def guestbook_list(request, wedding_id):
    guestbook = GuestBook.objects.filter(wedding_id=wedding_id).order_by('-reg_dtime')

    data = {
        'guestbook_list': guestbook,
    }

    return render(request, 'main/guestbook.html', data)


def guestbook(request, wedding_id):
    guestbook = GuestBook()

    if request.POST.get('message'):
        guestbook.name = request.POST['name']
        guestbook.message = request.POST['message']
        guestbook.wedding_id = wedding_id
        guestbook.passwd = request.POST['passwd']

        guestbook.save()

    return HttpResponseRedirect(f'/{wedding_id}#comment')


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
