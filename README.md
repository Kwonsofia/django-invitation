# django-invitation
django invitaion project

## django MTV
M: Model -> DB, View의 요청을 받아 처리
T: Template -> User의 요청을 받아 View로 전달(html을 의미)
V: View -> Template으로 받은 요청으로 작업 및 Model에 작업 요청 (Template과 Model의 중간다리 역할)


## django setting

```
pip install django

django-admin startproject invitation

cd invitation

python manage.py startapp main
```


## django run
```
python manage.py runserver
```

admin에서 사용할 superuser 만들기
```
python manage.py createsuperuser

사용자 이름 (leave blank to use 'hmkwon'): 
이메일 주소: 
Password: 
Password (again):
Superuser created successfully.
```


## django application connect
main/models.py 에서 Table 생성
invitation/settings.py 에 INSTALLED_APPS 리스트에 main/apps.py에 있는 Class명 추가 (MainConfig) -> App 등록하는 과정

기존 프로젝트 DB Model에 Application의 DB Model을 이식
```
python manage.py makemigrations main
```
main/migrations 하위에 파일 생성됨

```
python manage.py migrate
```

```
python manage.py sqlmigrate main 변경기록번호
```

makemigrations VS migration
- makemigrations 은 application에서 model의 수정사항을 기록(프로젝트에 migration된 것 아님)
- migration 은 변화 기록을 참고하여 실제 변화 사항을 반영



## Reference
- https://velog.io/@hyeoneedyou/django-%EA%B0%9C%EB%B0%9C%ED%99%98%EA%B2%BD%EC%84%B8%ED%8C%85#5-%EC%84%9C%EB%B2%84-%EC%8B%A4%ED%96%89
- https://kante-kante.tistory.com/8
- https://github.com/dkyou7/TIL/blob/master/%ED%8C%8C%EC%9D%B4%EC%8D%AC/Django/6.%20%5BDjango%5D%20%ED%8F%BC%20%EB%A7%8C%EB%93%A4%EA%B8%B0.md // models.py에서 참고
