from django.urls import path
from insta_down.service import insta_down

urlpatterns = [
    path('', insta_down.download_post, name='download'),
]
