from django.http import JsonResponse

from insta_down.module.insta_api import InstaAPI


def download(request):
    # do sth
    insta_api = InstaAPI()
    return JsonResponse(insta_api.get_post("B-pTcmQn5I1"))
