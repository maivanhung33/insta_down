from django.urls import path

from insta_down.service import user

urlpatterns = [
    path('register', user.register, name='register'),
    path('login', user.login, name='login')
]
