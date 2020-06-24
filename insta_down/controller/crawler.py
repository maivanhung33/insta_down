from django.urls import path

from insta_down.service import crawler

urlpatterns = [
    path('post', crawler.download_post, name='download_post'),
    path('album', crawler.download_album, name='download_album')
]
