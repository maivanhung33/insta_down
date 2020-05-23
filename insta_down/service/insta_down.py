import json

from django.http import JsonResponse

import insta_down.response.post as post_response
from insta_down.module.insta_api import InstaAPI
from insta_down.module.insta_validator import InstaValidator
from insta_down.response.error_response import BAD_REQUEST, METHOD_NOT_ALLoW, MUST_HAVE_URL


def download_post(request):
    # validate
    if request.method != 'POST':
        return METHOD_NOT_ALLoW
    try:
        body: dict = json.loads(request.body.decode('utf-8'))
        if 'url' not in body.keys():
            return MUST_HAVE_URL
    except Exception as e:
        print(e)
        return BAD_REQUEST

    validator = InstaValidator(body['url'])
    temp = validator.validate_url()
    if not temp['status']:
        return temp['response']
    temp = validator.validate_url_post()
    if not temp['status']:
        return temp['response']
    short_code = temp['response']

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
            message="no image found")]
        return JsonResponse(
            data=post_response.to_dict(id=id, owner=owner, data=data),
            content_type='application/json', status=400)

    # data_crawl = DataCrawl(
    #     id=id,
    #     owner=owner,
    #     data=data,
    #     count=count,
    #     _expireAt=datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')))
    # data_crawl.save()

    return JsonResponse(
        data=post_response.to_dict(id=id, owner=owner, data=data),
        content_type='application/json', status=200)


def download_album(request):
    # validate
    if request.method != 'POST':
        return METHOD_NOT_ALLoW
    try:
        body: dict = json.loads(request.body.decode('utf-8'))
        if 'url' not in body.keys():
            return MUST_HAVE_URL
    except Exception as e:
        print(e)
        return BAD_REQUEST

    validator = InstaValidator(body['url'])
    temp = validator.validate_url()
    if not temp['status']:
        return temp['response']

    temp = validator.validate_url_profile()
    if not temp['status']:
        return temp['response']
    user_name = temp['response']
    # processing
    insta_api = InstaAPI()
    response = insta_api.get_user_info(user_name)
    id = response['graphql']['user']['id']
    owner = dict(
        id=id,
        avatar=response['graphql']['user']['profile_pic_url'],
        name=response['graphql']['user']['username'])

    data = []
    count = 0

    end_cursor = ''
    while end_cursor is not None:
        response = insta_api.get_posts(id, end_cursor)
        edges = response['data']['user']['edge_owner_to_timeline_media']['edges']
        if len(edges) != 0:
            for item in edges:
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

        end_cursor = response['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
    # data_crawl = DataCrawl(
    #     id=id,
    #     owner=owner,
    #     data=data,
    #     count=count,
    #     _expireAt=datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')))
    # data_crawl.save()

    return JsonResponse(
        data=post_response.to_dict(id=id, owner=owner, data=data),
        content_type='application/json', status=200)
