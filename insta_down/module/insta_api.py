import requests


class InstaAPI:
    __header: dict
    __payload: dict
    __query_param: dict
    __url: str
    BASE_URL = "https://www.instagram.com/graphql/query/"
    USER_INFO_URL = "https://www.instagram.com/"

    def __init__(self):
        self.__header = {'cookie': 'sessionid=5711537494%3AsqShow1gFBehyH%3A22;',
                         'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
        self.__payload = {}
        self.__query_param = {}
        self.__url = ''

    def set_header(self, key: str, value):
        self.__header[key] = value
        print(self.__header)

    def set_body(self, data: dict):
        self.__payload = data

    def set_param(self, k: str, v: str):
        self.__query_param[k] = v
        print(self.__query_param)

    def set_url(self, url: str):
        self.__url = url

    def get_posts(self, user_id, cursor: str):
        cursor = cursor.replace("=", '')
        cursor += '%3D%3D' if cursor != '' else ''
        url = self.BASE_URL + r'?query_hash=e769aa130647d2354c40ea6a439bfc08&variables=%7B%22id%22%3A%22'
        url += str(user_id) + r'%22%2C%22first%22%3A50%2C%22after%22%3A%22'
        url += str(cursor) + r'%22%7D'
        return requests.get(url).json()

    def get_post(self, short_code):
        url = self.BASE_URL + r'?query_hash=a92f76e852576a71d3d7cef4c033a95e&variables=%7B%22shortcode%22%3A%22'
        url += str(short_code) + r'%22%7D'
        return requests.get(url).json()

    def get_user_info(self, user_name):
        url = self.USER_INFO_URL + str(user_name) + r'/?__a=1'
        response=requests.get(url)
        print(response.status_code)
        print(response.text)
        return requests.get(url).json()
