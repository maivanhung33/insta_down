from insta_down.module.insta_api import InstaAPI
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
        if (short_code[3] == "p") and (len(short_code) == 6):
            return short_code[4]
        else: 
            pass

    def validate_profile(self):
        # return userId if link is profile of user else Raise BadRequest Exception
        url = self.__url
        if url[-1:] != '/':
            url += '/'
        url = url + "?__a=1"
        try: 
            data = requests.get(url).json()
            user_id = data["logging_page_id"].replace("profilePage_", "")
            return user_id
        except:
            pass
