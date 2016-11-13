import requests


class APIHelper(object):
    def __init__(self, api_url):
        self.headers = {}
        self.api_url = api_url

    def do_request(self, method, url, data=None):
        response = requests.request(method, self.api_url + url, data=data, headers=self.headers)
        return response
