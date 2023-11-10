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

        return mypage(request, wedding_id)

    else:
        return render(request, 'main/admin/login.html')

def register(request):
    if request.method == 'POST':
        wedding_id = request.POST.get('wedding_id')

        if WeddingMain.objects.get(wedding_id=wedding_id):
            messages.warning('이미 존재하는 유저입니다. 로그인 부탁드립니다.')
            return HttpResponseRedirect('/user/admin/login')

        wedding_main = WeddingMain(
            wedding_id=wedding_id,
            passwd=request.POST['passwd'],
            groom_name=request.POST['groom_name'],
            bride_name=request.POST['bride_name'],
            
            groom_father_name=request.POST.get('groom_father_name'),
            groom_mother_name=request.POST.get('groom_mother_name'),
            bride_father_name=request.POST.get('bride_father_name'),
            bride_mother_name=request.POST.get('bride_mother_name'),

            use_guestbook=request.POST.get('use_guestbook', False),
            wedding_date=request.POST['wedding_date'],
            wedding_time=request.POST['wedding_time'],
            reg_dtime=datetime.now(),
        )
        wedding_main.save()

        user_wedding = WeddingMain.objects.get(wedding_id=wedding_id)

        if not user_wedding:
            messages.warning('회원 가입 실패')
            return render(request, 'main/admin/register.html')
        
        phone = Phone(
            wedding_id=user_wedding,
            groom_phone=request.POST.get('groom_phone'),
            groom_father_phone=request.POST.get('groom_father_phone'),
            groom_mother_phone=request.POST.get('groom_mother_phone'),

            bride_phone=request.POST.get('bride_phone'),
            bride_father_phone=request.POST.get('bride_father_phone'),
            bride_mother_phone=request.POST.get('bride_mother_phone'),
        )
        phone.save()

        account = Account(
            wedding_id=user_wedding,
            groom_account=request.POST.get('groom_account'),
            groom_father_account=request.POST.get('groom_father_account'),
            bride_account=request.POST.get('bride_account'),
            bride_father_account=request.POST.get('bride_father_account'),
        )
        account.save()

        address = Address(
            wedding_id=user_wedding,
            address=request.POST['address'],
            address_tel=request.POST.get('address_tel'),

            kakaomap_timestamp=request.POST['kakaomap_timestamp'],
            kakaomap_key=request.POST['kakaomap_key'],
        )
        address.save()

        if request.FILES.get('img'):
            for p in request.FILES.get('img'):
                photos = Photo(
                    wedding_id=user_wedding,
                    img=p,
                )
                photos.save()

        messages.success('회원 성공, 로그인해주세요 :)')
        return HttpResponseRedirect('/user/admin/login')
    else:
        return render(request, 'main/admin/register.html')


def mypage(request, wedding_id):
    result = admin_user_info(wedding_id)

    if not result:
        return render(request, 'main/admin/login.html')

    return render(request, 'main/admin/mypage.html', result)


# Invitation
def invitation(request, wedding_id):
    wedding = WeddingMain.objects.get(wedding_id=wedding_id)
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
        'info': wedding,
        'phone': phone[0],
        'account': account[0],
        'address': address[0],
        'main_image': main_image,
        'sub_image': sub_image,
        'photos': photo_list,
        'date': wedding_date(wedding.wedding_date, wedding.wedding_time),
        'is_guestbook_use': wedding.use_guestbook,
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
