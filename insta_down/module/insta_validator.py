import requests

from insta_down.module.insta_api import InstaAPI
from insta_down.response.error_response import VALIDATE_ERROR


class InstaValidator:
    VALIDATE_ERROR = dict(status=False,
                          response=VALIDATE_ERROR)
    __url: str
    __insta_api: InstaAPI

    def __init__(self, url: str):
        self.__url = url
        self.__insta_api = InstaAPI()

    def set_response(self, data):
        return dict(status=True,
                    response=data)

    def validate_url_post(self):
        short_code = self.__url.split("/")
        # Recheck
        if (short_code[3] == "p") and (len(short_code) == 6) and (short_code[2] == "www.instagram.com"):
            return self.set_response(short_code[4])
        else:
            return self.VALIDATE_ERROR

    def validate_url_profile(self):
        url = self.__url
        check_profile = url.split("/")
        if (len(check_profile) >= 4) and (check_profile[2] == "www.instagram.com"):
            user_name = check_profile[3]
            return self.set_response(user_name)
        else:
            return self.VALIDATE_ERROR

    def validate_url(self):
        # return url if the link is from Instagram else Raise BadRequest Exception
        url = self.__url.split('/')
        if url[2] == "www.instagram.com":
            check = requests.get(self.__url)
            if check.status_code != 200:
                return self.VALIDATE_ERROR
        else:
            return self.VALIDATE_ERROR
        return self.set_response(None)
