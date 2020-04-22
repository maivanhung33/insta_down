from django.urls import path
from insta_down.service import insta_down

urlpatterns = [
    path('post', insta_down.download_post, name='download_post'),
    path('album', insta_down.download_album, name='download_album'),
]
