from django.db import models

# Create your models here.

class WeddingMain(models.Model):
    wedding_id = models.CharField(max_length=20, primary_key=True)
    passwd = models.CharField(max_length=60)
    groom_name = models.CharField(max_length=10)
    groom_father_name = models.CharField(max_length=10, null=True)
    groom_mother_name = models.CharField(max_length=10, null=True)
    bride_name = models.CharField(max_length=10)
    bride_father_name = models.CharField(max_length=10, null=True)
    bride_mother_name = models.CharField(max_length=10, null=True)
    use_guestbook = models.BooleanField(default=False)
    wedding_date = models.DateField("wedding date")
    wedding_time = models.CharField(max_length=20)
    reg_dtime = models.DateTimeField(auto_now_add=True)

class Phone(models.Model):
    wedding_id = models.ForeignKey(WeddingMain, on_delete=models.CASCADE)
    groom_phone = models.CharField(max_length=13)
    groom_father_phone = models.CharField(max_length=13, null=True)
    groom_mother_phone = models.CharField(max_length=13, null=True)
    bride_phone = models.CharField(max_length=13)
    bride_father_phone = models.CharField(max_length=13, null=True)
    bride_mother_phone = models.CharField(max_length=13, null=True)

class Account(models.Model):
    wedding_id = models.ForeignKey(WeddingMain, on_delete=models.CASCADE)
    groom_account = models.CharField(max_length=30)
    groom_father_account = models.CharField(max_length=30, null=True)
    bride_account = models.CharField(max_length=30)
    bride_father_account = models.CharField(max_length=30, null=True)

class Address(models.Model):
    wedding_id = models.ForeignKey(WeddingMain, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    address_tel = models.CharField(max_length=100, null=True)
    kakaomap_timestamp = models.IntegerField()
    kakaomap_key = models.CharField(max_length=10)

class GuestBook(models.Model):
    wedding_id = models.CharField(max_length=20)
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    passwd = models.CharField(max_length=60)
    message = models.CharField(max_length=500, default='')
    reg_dtime = models.DateTimeField(auto_now_add=True)

class Photo(models.Model):
    wedding_id = models.ForeignKey(WeddingMain, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='img')  # image를 넣을때는 {id}_{number}.jpg 형식으로 네이밍 필요
