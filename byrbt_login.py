import requests
import json

class login:
    def __init__(self,config):
        self.session = requests.session()
        self.headers = config["headers"]
        self.url = config["url"]
        self.cookies = {}
        cookies_str = config["cookies_str"]
        for cookie_str in cookies_str.split("; "):
            self.cookies[cookie_str.split("=")[0]]=cookie_str.split("=")[1]