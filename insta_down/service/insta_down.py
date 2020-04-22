from django.http import JsonResponse

import insta_down.response.post as post_response
from insta_down.model.data_crawl import DataCrawl
from insta_down.module.insta_api import InstaAPI
from insta_down.module.validator import Validator


def download_post(request):
    # validate
    if request.method != 'GET':
        return JsonResponse(data={"message": "Method not allow"}, status=405)
    validator = Validator('link')
    short_code = validator.validate_post()
    short_code = 'B-pTcmQn5I1'

    # processing
    insta_api = InstaAPI()
    response = insta_api.get_post(short_code)
    id = response['data']['shortcode_media']['id']
    owner = dict(
        id=response['data']['shortcode_media']['owner']['id'],
        avatar=response['data']['shortcode_media']['owner']['profile_pic_url'],
        name=response['data']['shortcode_media']['owner']['username'])
    data = [dict(
        id=response['data']['shortcode_media']['id'],
        url=response['data']['shortcode_media']['display_url'],
        shortcode=response['data']['shortcode_media']['shortcode'],
        count_like=response['data']['shortcode_media']['edge_media_preview_like']['count'],
        count_comment=response['data']['shortcode_media']['edge_media_to_comment']['count'],
        thumbnail_url=response['data']['shortcode_media']['display_url'])]

    data_crawl = DataCrawl(
        id=id,
        owner=owner,
        data=data)
    data_crawl.save(force_insert=True)

    return JsonResponse(
        data=post_response.to_dict(id, owner, data),
        content_type='application/json', status=200)


def download_album(request):
    # validate
    if request.method != 'POST':
        return JsonResponse(data={"message": "Method not allow"}, status=405)
    validator = Validator('link')
    user_id = validator.validate_profile()

    # processing
    pass
