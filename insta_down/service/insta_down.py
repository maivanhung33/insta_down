import json
from datetime import datetime

import pytz
from django.http import JsonResponse

import insta_down.response.post as post_response
from insta_down.model.data_crawl import DataCrawl
from insta_down.module.insta_api import InstaAPI
from insta_down.module.validator import Validator


def download_post(request):
    # validate
    if request.method != 'POST':
        return JsonResponse(data={"message": "Method not allow"}, status=405)
    body: dict = json.loads(request.body.decode('utf-8'))
    if 'url' not in body.keys():
        return JsonResponse(data={'message': 'must have url'},
                            content_type='application/json', status=400)
    validator = Validator(body['url'])
    short_code = validator.validate_url_post()

    # processing
    insta_api = InstaAPI()
    response = insta_api.get_post(short_code)
    id = response['data']['shortcode_media']['id']
    owner = dict(
        id=response['data']['shortcode_media']['owner']['id'],
        avatar=response['data']['shortcode_media']['owner']['profile_pic_url'],
        name=response['data']['shortcode_media']['owner']['username'])

    data = []
    count = 0

    if response['data']['shortcode_media']['__typename'] == 'GraphSidecar':  # More than one photo/video in this post
        for item in response['data']['shortcode_media']['edge_sidecar_to_children']['edges']:
            if item['node']['__typename'] == "GraphImage":  # Only down load image.
                data.append(dict(
                    id=item['node']['id'],
                    url=item['node']['display_url'],
                    height=item['node']['dimensions']['height'],
                    width=item['node']['dimensions']['width'],
                    thumbnail=item['node']['display_resources'][0]['src'],
                    shortcode=item['node']['shortcode'],
                    countLike=response['data']['shortcode_media']['edge_media_preview_like']['count'],
                    countComment=response['data']['shortcode_media']['edge_media_to_comment']['count']))
                count += 1

    elif response['data']['shortcode_media']['__typename'] == 'GraphImage':  # Has only one photo
        data = [dict(
            id=response['data']['shortcode_media']['id'],
            url=response['data']['shortcode_media']['display_url'],
            height=response['data']['shortcode_media']['dimensions']['height'],
            width=response['data']['shortcode_media']['dimensions']['width'],
            thumbnail=response['data']['shortcode_media']['display_resources'][0]['src'],
            shortcode=response['data']['shortcode_media']['shortcode'],
            countLike=response['data']['shortcode_media']['edge_media_preview_like']['count'],
            countComment=response['data']['shortcode_media']['edge_media_to_comment']['count'])]
        count += 1

    else:
        data = [dict(
            message="no image found"
        )]
        return JsonResponse(
            data=post_response.to_dict(id=id, owner=owner, data=data),
            content_type='application/json', status=400)

    data_crawl = DataCrawl(
        id=id,
        owner=owner,
        data=data,
        count=count,
        _expireAt=datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')))
    data_crawl.save()

    return JsonResponse(
        data=post_response.to_dict(id=id, owner=owner, data=data),
        content_type='application/json', status=200)


def download_album(request):
    # validate
    if request.method != 'POST':
        return JsonResponse(data={"message": "Method not allow"}, status=405)
    body: dict = json.loads(request.body.decode('utf-8'))
    if 'url' not in body.keys():
        return JsonResponse(data={'message': 'must have url'},
                            content_type='application/json', status=400)
    validator = Validator(body['url'])
    validator.validate_url()
    user_name = validator.validate_url_profile()
    # user_name = 'kygomusic'  # This line is temporary.

    # processing
    insta_api = InstaAPI()
    response = insta_api.get_user_info(user_name)
    id = response['graphql']['user']['id']
    owner = dict(
        id=id,
        avatar=response['graphql']['user']['profile_pic_url'],
        name=response['graphql']['user']['username']
    )

    data = []
    count = 0

    end_cursor = ''
    while (end_cursor != None):
        response2 = insta_api.get_posts(id, end_cursor)

        for item in response2['data']['user']['edge_owner_to_timeline_media']['edges']:
            if item['node']['__typename'] == 'GraphImage':  # One photo/video in this post
                data.append(dict(
                    id=item['node']['id'],
                    url=item['node']['display_url'],
                    height=item['node']['dimensions']['height'],
                    width=item['node']['dimensions']['width'],
                    thumbnail=item['node']['thumbnail_src'],
                    shortcode=item['node']['shortcode'],
                    countLike=item['node']['edge_media_preview_like']['count'],
                    countComment=item['node']['edge_media_to_comment']['count']))
                count += 1

            elif item['node']['__typename'] == 'GraphSidecar':  # More than one photo/video in this post
                for node_item in item['node']['edge_sidecar_to_children']['edges']:
                    if node_item['node']['__typename'] == 'GraphImage':
                        data.append(dict(
                            id=node_item['node']['id'],
                            url=node_item['node']['display_url'],
                            height=node_item['node']['dimensions']['height'],
                            width=node_item['node']['dimensions']['width'],
                            thumbnail=node_item['node']['display_resources'][0]['src'],
                            shortcode=item['node']['shortcode'],
                            countLike=item['node']['edge_media_preview_like']['count'],
                            countComment=item['node']['edge_media_to_comment']['count']))
                        count += 1

        end_cursor = response2['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']

        ''' # Function below is useless because the same function is in insta_api.get_posts()
        if end_cursor is not None:
            # Remove the last = in the end_cursor
            end_cursor = end_cursor.replace("=", "")
            # Append  == at last by url encode
            end_cursor += '%3D%3D' '''

    data_crawl = DataCrawl(
        id=id,
        owner=owner,
        data=data,
        count=count,
        _expireAt=datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')))
    data_crawl.save()

    return JsonResponse(
        data=post_response.to_dict(id=id, owner=owner, data=data),
        content_type='application/json', status=200)
