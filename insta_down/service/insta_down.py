import json
import os
from datetime import datetime

import pytz
from django.http import JsonResponse

import hashlib
import jwt
import time

import insta_down.response.data_crawl as data_crawl_response
from insta_down.model.data_crawl import DataCrawl, Owner, ItemCrawl, User
from insta_down.module.insta_api import InstaAPI
from insta_down.module.insta_validator import InstaValidator
from insta_down.module.mongo_client import database
from insta_down.response.error import BAD_REQUEST, METHOD_NOT_ALLoW, MUST_HAVE_URL

db = database()
COL = os.environ.get('COL') or 'insta_down_datacrawl'
COL_USER = os.environ.get('COL_USER') or 'insta_down_data_user'
SECRET = 'nhomt@m-nt208.k21.antt'


def download_post(request):
    # validate request
    if request.method != 'POST':
        return METHOD_NOT_ALLoW
    try:
        body: dict = json.loads(request.body.decode('utf-8'))
        if 'url' not in body.keys():
            return MUST_HAVE_URL
    except Exception as e:
        print(e)
        return BAD_REQUEST

    # validate link
    validator = InstaValidator(body['url'])
    temp = validator.validate_url()
    if not temp['status']:
        return temp['response']

    # get shortcode
    temp = validator.validate_url_post()
    if not temp['status']:
        return temp['response']
    short_code = temp['response']

    # process
    insta_api = InstaAPI()
    id = short_code
    old_data = db[COL].find_one({'id': id}, {'_id': 0})
    if old_data is not None:
        return JsonResponse(
            data=data_crawl_response.to_dict(
                owner=old_data['owner'],
                count=old_data['count'],
                data=old_data['data']),
            content_type='application/json', status=200)

    response = insta_api.get_post(short_code)
    owner = Owner(
        id=response['data']['shortcode_media']['owner']['id'],
        avatar=response['data']['shortcode_media']['owner']['profile_pic_url'],
        name=response['data']['shortcode_media']['owner']['username'])
    data = []
    count = 0

    if response['data']['shortcode_media']['__typename'] == 'GraphSidecar':  # More than one photo/video in this post
        for item in response['data']['shortcode_media']['edge_sidecar_to_children']['edges']:
            if item['node']['__typename'] == "GraphImage":  # Only down load image.
                data.append(ItemCrawl(
                    id=item['node']['id'],
                    url=item['node']['display_url'],
                    height=item['node']['dimensions']['height'],
                    width=item['node']['dimensions']['width'],
                    thumbnail=item['node']['display_resources'][0]['src'],
                    shortcode=item['node']['shortcode'],
                    countLike=response['data']['shortcode_media']['edge_media_preview_like']['count'],
                    countComment=response['data']['shortcode_media']['edge_media_to_comment']['count']).__dict__)
                count += 1

    elif response['data']['shortcode_media']['__typename'] == 'GraphImage':  # Has only one photo
        data = [ItemCrawl(
            id=response['data']['shortcode_media']['id'],
            url=response['data']['shortcode_media']['display_url'],
            height=response['data']['shortcode_media']['dimensions']['height'],
            width=response['data']['shortcode_media']['dimensions']['width'],
            thumbnail=response['data']['shortcode_media']['display_resources'][0]['src'],
            shortcode=response['data']['shortcode_media']['shortcode'],
            countLike=response['data']['shortcode_media']['edge_media_preview_like']['count'],
            countComment=response['data']['shortcode_media']['edge_media_to_comment']['count']).__dict__]
        count += 1

    else:
        data = [dict(message="no image found")]
        return JsonResponse(
            data=data_crawl_response.to_dict(owner=owner, data=data, count=count),
            content_type='application/json', status=400)

    data_crawl = DataCrawl(
        id=id,
        owner=owner.__dict__,
        data=data,
        count=count,
        _expire_at=datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')))
    db[COL].insert(data_crawl.__dict__)

    return JsonResponse(
        data=data_crawl_response.to_dict(count=count, owner=owner.__dict__, data=data),
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

    old_data = db[COL].find_one({'id': user_name}, {'_id': 0})
    if old_data is not None:
        return JsonResponse(
            data=data_crawl_response.to_dict(
                owner=old_data['owner'],
                count=old_data['count'],
                data=old_data['data']),
            content_type='application/json', status=200)

    insta_api = InstaAPI()
    response = insta_api.get_user_info(user_name)
    id = response['graphql']['user']['id']
    owner = Owner(
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
                    data.append(ItemCrawl(
                        id=item['node']['id'],
                        url=item['node']['display_url'],
                        height=item['node']['dimensions']['height'],
                        width=item['node']['dimensions']['width'],
                        thumbnail=item['node']['thumbnail_src'],
                        shortcode=item['node']['shortcode'],
                        countLike=item['node']['edge_media_preview_like']['count'],
                        countComment=item['node']['edge_media_to_comment']['count']).__dict__)
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

    data_crawl = DataCrawl(
        id=user_name,
        owner=owner.__dict__,
        data=data,
        count=count,
        _expire_at=datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')))
    db[COL].insert(data_crawl.__dict__)

    return JsonResponse(
        data=data_crawl_response.to_dict(count=count, owner=owner.__dict__, data=data),
        content_type='application/json', status=200)


def register(request):
    if request.method != 'POST':
        return METHOD_NOT_ALLoW
    
    try:
        body: dict = json.loads(request.body.decode('utf-8'))
        if 'username' not in body.keys() or 'password' not in body.keys():
            return BAD_REQUEST #Or return validate_error
    except Exception as e:
        print(e)
        return BAD_REQUEST
    
    # Check if username exist
    username = body['username']
    matches_user = db[COL_USER].find_one({'username': username}, {'_id': 1})
    if matches_user is not None: #Exist
        # print(matches_user['_id']) Chưa get được Password từ user này, nếu ko sẽ phải find 2 lần.
        return JsonResponse(
            data={ 
                'message': 'Username is already exist'
            },
            content_type='application/json', status=400)
    # Not exist -> create new user.
    new_user = User(
        username=username, 
        password=hashlib.sha256(body['password'].encode('utf-8')).hexdigest()
        )
    db[COL_USER].insert(new_user.__dict__)
    return JsonResponse(
        data=data_crawl_response.to_dict(new_user.username, new_user.password),
        content_type='application/json', status=200)


def login(request):
    if request.method != 'POST':
        return METHOD_NOT_ALLoW
    
    try:
        body: dict = json.loads(request.body.decode('utf-8'))
        if 'username' not in body.keys() or 'password' not in body.keys():
            return BAD_REQUEST #Or return validate_error
    except Exception as e:
        print(e)
        return BAD_REQUEST

    # Check if username exist
    username = body['username']
    matches_user = db[COL_USER].find_one({'username': username}, {'_id': 1})
    if matches_user is None: #Not exist
        return JsonResponse(
            data={ 
                'message': 'Username is not exist'
            },
            content_type='application/json', status=404)
    # Exist -> Compare username, pw to login, generate token
    password=hashlib.sha256(body['password'].encode('utf-8')).hexdigest()
    logining_user = db[COL_USER].find_one({'username': username, 'password':password}, {'_id': 1})
    if logining_user is None: #Incorrect username or password
        return JsonResponse(
            data={ 
                'message': 'Login failed. Username or password is incorrect.'
            },
            content_type='application/json', status=403)
    # Login successful, generate JWT
    payload = {
        "username": username,
        "password": password,
        "start_at": int(time.time()),
        "exp": int(time.time())+3600 # 1 hour
    }

    token = jwt.encode(payload, SECRET, algorithm='HS256')
    
    # Decode below:
    # try:
    #     decoded = jwt.decode(token, SECRET, algorithms='HS256')
    # except jwt.ExpiredSignatureError:
    #     print("Token expired. Get new one")

    return JsonResponse(
            data={ 
                "message": 'Login successful.',
                "token": token.decode("utf-8")
            },
            content_type='application/json', status=200)