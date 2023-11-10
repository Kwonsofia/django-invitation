"""
URL configuration for invitation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('user/admin/login', views.login, name='login'),
    path('user/admin/register', views.register, name='register'),
    path('user/admin/mypage/<str:wedding_id>', views.mypage, name='mypage'),
    path('<str:wedding_id>', views.invitation),
    path('<str:wedding_id>/guestbooks', views.guestbook_list, name='guestbooks'),
    path('<str:wedding_id>/guestbook', views.guestbook, name='guestbook'),
    path('guestbook/delete/<str:msg_id>', views.guestbook_delete, name='guestbook_delete'),
    path('guestbooks/delete/<str:msg_id>', views.guestbook_list_delete, name='guestbook_list_delete'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
