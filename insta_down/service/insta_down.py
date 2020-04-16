from django.http import JsonResponse, HttpResponseBadRequest
from insta_down.model.data_crawl import DataCrawl, Owner, ItemCrawl
from insta_down.module.insta_api import InstaAPI
from insta_down.module.validator import Validator


def download_post(request):
    # do sth
    validator = Validator('link')
    if not validator.validate_post():
        raise HttpResponseBadRequest(status=400, reason='link is not correct')
    insta_api = InstaAPI()
    short_code = validator.get_short_code()
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
