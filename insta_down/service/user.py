import hashlib
import json
import os
import time

import jwt
from django.http import JsonResponse

import insta_down.response.data_crawl as data_crawl_response
from insta_down.model.data_crawl import User
from insta_down.module.mongo_client import database
from insta_down.response.error import BAD_REQUEST, METHOD_NOT_ALLoW

db = database()
COL_USER = os.environ.get('COL_USER') or 'insta_down_data_user'
SECRET = 'nhomt@m-nt208.k21.antt'


def register(request):
    if request.method != 'POST':
        return METHOD_NOT_ALLoW

    try:
        body: dict = json.loads(request.body.decode('utf-8'))
        if 'username' not in body.keys() or 'password' not in body.keys():
            return BAD_REQUEST  # Or return validate_error
    except Exception as e:
        print(e)
        return BAD_REQUEST

    # Check if username exist
    username = body['username']
    matches_user = db[COL_USER].find_one({'username': username}, {'_id': 1})
    if matches_user is not None:  # Exist
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
            return BAD_REQUEST  # Or return validate_error
    except Exception as e:
        print(e)
        return BAD_REQUEST

    # Check if username exist
    username = body['username']
    matches_user = db[COL_USER].find_one({'username': username}, {'_id': 1})
    if matches_user is None:  # Not exist
        return JsonResponse(
            data={
                'message': 'Username is not exist'
            },
            content_type='application/json', status=404)
    # Exist -> Compare username, pw to login, generate token
    password = hashlib.sha256(body['password'].encode('utf-8')).hexdigest()
    logining_user = db[COL_USER].find_one({'username': username, 'password': password}, {'_id': 1})
    if logining_user is None:  # Incorrect username or password
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
        "exp": int(time.time()) + 3600  # 1 hour
    }

    token = jwt.encode(payload, SECRET, algorithm='HS256')

    return JsonResponse(
        data={"message": 'Login successful.', "token": token.decode("utf-8")},
        content_type='application/json', status=200)
