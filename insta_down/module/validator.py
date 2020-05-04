from insta_down.module.insta_api import InstaAPI
from django.core.exceptions import ValidationError
import requests
class Validator:
    __url: str
    __insta_api: InstaAPI

    def __init__(self, url: str):
        self.__url = url
        self.__insta_api = InstaAPI()

    def validate_post(self):
        # return shortcode if link is post link of instagram else Raise BadRequest Exception
        short_code = self.__url.split("/")
        if (short_code[3] == "p") and (len(short_code) == 6) and (short_code[2] == "www.instagram.com"):
            return short_code[4]
        else: 
            raise ValidationError("Bad request")

    def validate_profile(self):
        # return userId if link is profile of user else Raise BadRequest Exception
        url = self.__url
        checkProfile = url.split("/")
        if (len(checkProfile) == 5) and (checkProfile[2] == "www.instagram.com"):
            userName = checkProfile[3]
            return userName
        else:
            raise ValidationError("Bad request")

    def Validator(self, link):
        #return url if the link is from Instagram else Raise BadRequest Exception
        url = link.split('/')
        if (url[2] == "www.instagram.com"):
            check = requests.get(link)
            if (check.status_code == 200):
                self.__url = link
                return self.__url
            else:
                raise ValidationError("Bad request")
        else:
            raise ValidationError('Bad request')
