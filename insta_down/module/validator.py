from insta_down.module.insta_api import InstaAPI


class Validator:
    __url: str
    __insta_api: InstaAPI

    def __init__(self, url: str):
        self.__url = url
        self.__insta_api = InstaAPI()

    def validate_post(self):
        pass
        return True

    def validate_profile(self):
        pass
        return True

    def get_short_code(self):
        return 'B-pTcmQn5I1'

    def get_url(self):
        return self.__url
