from django.http import JsonResponse

from insta_down.model.data_crawl import DataCrawl, Owner, ItemCrawl
from insta_down.module.insta_api import InstaAPI
from insta_down.module.validator import Validator


def download_post(request):
    # validate
    validator = Validator('link')
    short_code = validator.validate_post()

    # processing
    insta_api = InstaAPI()
    response = insta_api.get_post(short_code)
    data = DataCrawl()
    data.id = response['data']['shortcode_media']['id']
    data.owner = Owner(
        id=response['data']['shortcode_media']['owner']['id'],
        avatar=response['data']['shortcode_media']['owner']['profile_pic_url'],
        name=response['data']['shortcode_media']['owner']['username'])
    data.data = [ItemCrawl(
        url=response['data']['shortcode_media']['display_url'],
        shortcode=response['data']['shortcode_media']['shortcode'],
        count_like=response['data']['shortcode_media']['edge_media_preview_like']['count'],
        count_comment=response['data']['shortcode_media']['edge_media_to_comment']['count'],
        thumbnail_url=response['data']['shortcode_media']['display_url'])]
    data.save()
    return JsonResponse(data.to_dict(), content_type='application/json')


def download_album(request):
    # validate
    validator = Validator('link')
    user_id = validator.validate_profile()

    # processing
    pass
