from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage

from .models import WeddingMain, Phone, Account, Photo, Address, GuestBook, Music
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
    music = Music.objects.filter(wedding_id=wedding_id)

    if not wedding:
        return None

    photo_list = []
    main_image = None
    sub_image = None
    for photo in photos:

        # if wedding_id not in photo.img.url:
        #     continue

        if 'main_' in photo.img or 'main_' in photo.img.url:
            main_image = photo.img
        elif 'sub_' in photo.img or 'sub_' in photo.img.url:
            sub_image = photo.img
        else:
            photo_list.append(photo)

    data = {
        'info': wedding,
        'phone': phone[0] if phone else None,
        'account': account[0] if account else None,
        'address': address[0] if address else None,
        'main_image': main_image,
        'sub_image': sub_image,
        'photos': photo_list,
        'date': wedding_date(wedding.wedding_date, wedding.wedding_time),
        'music': music[0] if music else None
    }

    return data


# Admin
def login(request):
    if request.method == 'POST':
        wedding_id = request.POST['wedding_id']
        pw = request.POST['pw']

        try:
            wedding = WeddingMain.objects.get(wedding_id=wedding_id)

            if pw == wedding.passwd:
                # 로그인 성공
                request.session['user_id'] = wedding.wedding_id

                messages.success(request, '로그인 성공!')
                return HttpResponseRedirect(f'/user/admin/mypage/{wedding_id}')

            else:
                messages.error(request, '로그인 실패. 다시 시도해주세요.')

        except UserProfile.DoesNotExist:
            messages.error(request, '사용자가 존재하지 않습니다.')

    return render(request, 'main/admin/login.html')


def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']

    messages.info(request, '로그아웃 되었습니다.')

    return render(request, 'main/admin/login.html')


def register(request):
    if request.method == 'POST':
        wedding_id = request.POST.get('wedding_id')

        if WeddingMain.objects.filter(wedding_id=wedding_id):
            messages.warning(request, '이미 존재하는 유저입니다. 로그인 부탁드립니다.')
            return HttpResponseRedirect('/user/admin/login')

        if 'use_guestbook' in request.POST and request.POST.get('use_guestbook'):
            is_use_guestbook = True
        else:
            is_use_guestbook = False

        wedding_main = WeddingMain(
            wedding_id=wedding_id,
            passwd=request.POST['passwd'],
            groom_name=request.POST['groom_name'],
            bride_name=request.POST['bride_name'],

            use_guestbook=is_use_guestbook,
            wedding_date=request.POST['wedding_date'],
            wedding_time=request.POST['wedding_time'],
            reg_dtime=datetime.now(),
        )
        wedding_main.save()

        user_wedding = WeddingMain.objects.get(wedding_id=wedding_id)

        if not user_wedding:
            messages.warning(request, '회원 가입 실패')
            return render(request, 'main/admin/register.html')

        messages.success(request, '회원 성공, 로그인해주세요 :)')
        return HttpResponseRedirect('/user/admin/login')
    else:
        return render(request, 'main/admin/register.html')


def mypage(request, wedding_id):
    wedding = WeddingMain.objects.get(wedding_id=wedding_id)

    if not wedding:
        messages.warning(request, '존재하지 않는 Wedding ID 입니다.')
        return render(request, 'main/admin/login.html')

    elif request.session.get('user_id') is None or request.session.get('user_id') != wedding_id:
        messages.info(request, '로그인 해주세요.')
        return render(request, 'main/admin/login.html')

    if request.method == 'POST':

        print('[*] ', request.POST)
        print('[*] ', request.FILES)

        wedding_info_change = {}
        if request.POST.get('change_passwd'):
            if request.POST.get('passwd') == wedding.passwd:
                wedding_info_change['passwd'] = request.POST.get('change_passwd')
            else:
                messages.warning(request, '비밀번호가 틀렸습니다.')

        if request.POST.get('groom_father_name'):
            wedding_info_change['groom_father_name'] = request.POST.get('groom_father_name')
        if request.POST.get('groom_mother_name'):
            wedding_info_change['groom_mother_name'] = request.POST.get('groom_mother_name')
        if request.POST.get('bride_father_name'):
            wedding_info_change['bride_father_name'] = request.POST.get('bride_father_name')
        if request.POST.get('bride_mother_name'):
            wedding_info_change['bride_mother_name'] = request.POST.get('bride_mother_name')
        if request.POST.get('wedding_date'):
            wedding_info_change['wedding_date'] = request.POST.get('wedding_date')
        if request.POST.get('wedding_time'):
            wedding_info_change['wedding_time'] = request.POST.get('wedding_time')
        if 'use_guestbook' in request.POST and request.POST.get('use_guestbook'):
            wedding_info_change['use_guestbook'] = True
        else:
            wedding_info_change['use_guestbook'] = False
        if 'is_used' in request.POST and request.POST.get('is_used'):
            wedding_info_change['is_used'] = True
        else:
            wedding_info_change['is_used'] = False

        phone_change = {}
        if request.POST.get('groom_phone'):
            phone_change['groom_phone'] = request.POST.get('groom_phone')
        if request.POST.get('bride_phone'):
            phone_change['bride_phone'] = request.POST.get('bride_phone')
        if request.POST.get('groom_father_phone'):
            phone_change['groom_father_phone'] = request.POST.get('groom_father_phone')
        if request.POST.get('groom_mother_phone'):
            phone_change['groom_mother_phone'] = request.POST.get('groom_mother_phone')
        if request.POST.get('bride_father_phone'):
            phone_change['bride_father_phone'] = request.POST.get('bride_father_phone')
        if request.POST.get('bride_mother_phone'):
            phone_change['bride_mother_phone'] = request.POST.get('bride_mother_phone')

        account_change = {}
        if request.POST.get('groom_account'):
            account_change['groom_account'] = request.POST.get('groom_account')
        if request.POST.get('groom_father_account'):
            account_change['groom_father_account'] = request.POST.get('groom_father_account')
        if request.POST.get('groom_mother_account'):
            account_change['groom_mother_account'] = request.POST.get('groom_mother_account')
        if request.POST.get('bride_account'):
            account_change['bride_account'] = request.POST.get('bride_account')
        if request.POST.get('bride_father_account'):
            account_change['bride_father_account'] = request.POST.get('bride_father_account')
        if request.POST.get('bride_mother_account'):
            account_change['bride_mother_account'] = request.POST.get('bride_mother_account')

        address_change = {}
        if request.POST.get('address'):
            address_change['address'] = request.POST.get('address')
        if request.POST.get('address_tel'):
            address_change['address_tel'] = request.POST.get('address_tel')
        if request.POST.get('kakaomap_timestamp'):
            address_change['kakaomap_timestamp'] = request.POST.get('kakaomap_timestamp')
        if request.POST.get('kakaomap_key'):
            address_change['kakaomap_key'] = request.POST.get('kakaomap_key')

        if wedding_info_change:
            wedding_table = WeddingMain.objects.filter(wedding_id=wedding_id).update(**wedding_info_change)

        if phone_change:
            phone_table = Phone.objects.filter(wedding_id=wedding_id)
            if phone_table:
                phone_table.update(**phone_change)
            else:
                Phone.objects.create(wedding_id=wedding, **phone_change)

        if account_change:
            account_table = Account.objects.filter(wedding_id=wedding_id)
            if account_table:
                account_table.update(**account_change)
            else:
                Account.objects.create(wedding_id=wedding, **account_change)

        if address_change:
            address_table = Address.objects.filter(wedding_id=wedding_id)
            if address_table:
                address_table.update(**address_change)
            else:
                Address.objects.create(wedding_id=wedding, **address_change)

        if request.FILES:
            photos = Photo.objects.filter(wedding_id=wedding_id)

            main_image = request.FILES.get('main_image')
            sub_image = request.FILES.get('sub_image')

            old_main_image = None
            old_sub_image = None
            for photo in photos:

                # if wedding_id not in photo.img.url:
                #     continue

                if 'main_' in photo.img or 'main_' in photo.img.url:
                    old_main_image = photo
                elif 'sub_' in photo.img or 'sub_' in photo.img.url:
                    old_sub_image = photo

            if main_image:
                if old_main_image:
                    main_photo = Photo.objects.get(photo_id=old_main_image.photo_id)
                    main_photo.delete()
                    default_storage.delete(main_photo.img.path)
                main_image.name = f'main_{wedding_id}_' + main_image.name
                Photo.objects.create(wedding_id=wedding, img=main_image)

            if sub_image:
                if old_sub_image:
                    sub_photo = Photo.objects.get(photo_id=old_sub_image.photo_id)
                    sub_photo.delete()
                    default_storage.delete(sub_photo.img.path)
                sub_image.name = f'sub_{wedding_id}_' + sub_image.name
                Photo.objects.create(wedding_id=wedding, img=sub_image)

            images = request.FILES.getlist('images')

            for image in images:
                image.name = f'{wedding_id}_' + image.name
                Photo.objects.create(wedding_id=wedding, img=image)

            music_file = request.FILES.get('music_file')

            if music_file:
                temp = Music.objects.filter(wedding_id=wedding_id)

                if temp:
                    music = Music.objects.get(music_id=temp[0].music_id)
                    music.delete()
                    default_storage.delete(music.music_file.path)
                music = Music.objects.create(wedding_id=wedding, music_file=music_file)
                music.music_url = music.music_file.url
                music.save()

        messages.success(request, '수정 완료하였습니다. :)')

    result = admin_user_info(wedding_id)

    return render(request, 'main/admin/mypage.html', result)


def detail_photo(request, wedding_id, photo_id):
    photo = Photo.objects.get(photo_id=photo_id)

    if request.method == 'POST':
        photo.delete()
        messages.success(request, '삭제되었습니다.')

        return HttpResponseRedirect(f'/user/admin/mypage/{wedding_id}')

    return render(request, 'main/admin/photo.html', {'photo': photo, 'wedding_id': wedding_id})


def withdraw(request, wedding_id):
    user_data_delete = get_object_or_404(WeddingMain, wedding_id=wedding_id)

    if request.method == 'POST':
        wedding = WeddingMain.objects.get(wedding_id=wedding_id)

        passwd = request.POST.get('passwd')

        if passwd and passwd == wedding.passwd:
            user_data_delete.delete()
            messages.success(request, '탈퇴되었습니다.')

            return redirect('login')
        else:
            messages.warning(request, '비밀번호가 틀렸습니다.')

    return render(request, 'main/admin/withdraw.html', {'wedding_id': wedding_id})


# Invitation
def invitation(request, wedding_id):
    wedding = WeddingMain.objects.filter(wedding_id=wedding_id)
    phone = Phone.objects.filter(wedding_id=wedding_id)
    account = Account.objects.filter(wedding_id=wedding_id)
    address = Address.objects.filter(wedding_id=wedding_id)
    photos = Photo.objects.filter(wedding_id=wedding_id)
    music = Music.objects.filter(wedding_id=wedding_id)
    guestbooks = GuestBook.objects.filter(wedding_id=wedding_id).order_by('-reg_dtime')

    if not wedding:
        return render(request, 'main/error.html')
    elif not wedding[0].is_used:
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
        'info': wedding[0],
        'phone': phone[0] if phone else None,
        'account': account[0] if account else None,
        'address': address[0] if address else None,
        'main_image': main_image,
        'sub_image': sub_image,
        'photos': photo_list,
        'date': wedding_date(wedding[0].wedding_date, wedding[0].wedding_time),
        'is_guestbook_use': wedding[0].use_guestbook,
        'guestbook_list': guestbook_list,
        'music': music[0] if music else None
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
