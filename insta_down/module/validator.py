import requests
from django.core.exceptions import ValidationError

from insta_down.module.insta_api import InstaAPI


class Validator:
    __url: str
    __insta_api: InstaAPI

    def __init__(self, url: str):
        self.__url = url
        self.__insta_api = InstaAPI()

    def validate_url_post(self):
        # return shortcode if link is post link of instagram else Raise BadRequest Exception
        short_code = self.__url.split("/")
        if (short_code[3] == "p") and (len(short_code) == 6) and (short_code[2] == "www.instagram.com"):
            return short_code[4]
        else:
            raise ValidationError("Bad request")

    def validate_url_profile(self):
        # return userId if link is profile of user else Raise BadRequest Exception
        url = self.__url
        check_profile = url.split("/")
        if (len(check_profile) >= 4) and (check_profile[2] == "www.instagram.com"):
            user_name = check_profile[3]
            return user_name
        else:
            raise ValidationError("Bad request")

    def validate_url(self):
        # return url if the link is from Instagram else Raise BadRequest Exception
        url = self.__url.split('/')
        if (url[2] == "www.instagram.com"):
            check = requests.get(self.__url)
            if (check.status_code != 200):
                raise ValidationError("Bad request")
        else:
            raise ValidationError('Bad request')
