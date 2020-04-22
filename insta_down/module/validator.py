from insta_down.module.insta_api import InstaAPI


class Validator:
    __url: str
    __insta_api: InstaAPI

    def __init__(self, url: str):
        self.__url = url
        self.__insta_api = InstaAPI()

    def validate_post(self):
        pass
        # return shortcode if link is post link of instagram else Raise BadRequest Exception
        return

    def validate_profile(self):
        pass
        # return userId if link is profile of user else Raise BadRequest Exception
        return
