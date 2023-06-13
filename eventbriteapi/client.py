import json
from urllib.parse import urlencode

import requests

from eventbriteapi.exceptions import UnauthorizedError, WrongFormatInputError, ContactsLimitExceededError


class Client(object):
    AUTH_URL = "https://www.eventbrite.com/oauth/"
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}

    def __init__(self, api_key, client_secret, redirect_uri):
        self.CLIENT_ID = api_key
        self.CLIENT_SECRET = client_secret
        self.REDIRECT_URI = redirect_uri

    def authorization_url(self, state=None):
        params = {"response_type": "code", "client_id": self.CLIENT_ID, "redirect_uri": self.REDIRECT_URI}
        if state:
            params["state"] = state
        return self.AUTH_URL + "authorize?" + urlencode(params)

    def get_access_token(self, code):
        body = {
            "grant_type": "authorization_code",
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "code": code,
            "redirect_uri": self.REDIRECT_URI,
        }
        return self.post("token", data=body)

    def get(self, endpoint, **kwargs):
        response = self.request("GET", endpoint, **kwargs)
        return self.parse(response)

    def post(self, endpoint, **kwargs):
        response = self.request("POST", endpoint, **kwargs)
        return self.parse(response)

    def delete(self, endpoint, **kwargs):
        response = self.request("DELETE", endpoint, **kwargs)
        return self.parse(response)

    def put(self, endpoint, **kwargs):
        response = self.request("PUT", endpoint, **kwargs)
        return self.parse(response)

    def patch(self, endpoint, **kwargs):
        response = self.request("PATCH", endpoint, **kwargs)
        return self.parse(response)

    def request(self, method, endpoint, **kwargs):
        return requests.request(method, self.AUTH_URL + endpoint, headers=self.headers, **kwargs)

    def parse(self, response):
        status_code = response.status_code
        if "Content-Type" in response.headers and "application/json" in response.headers["Content-Type"]:
            try:
                r = response.json()
            except ValueError:
                r = response.text
        else:
            r = response.text
        if status_code == 200:
            return r
        if status_code == 204:
            return None
        if status_code == 400:
            raise WrongFormatInputError(r)
        if status_code == 401:
            raise UnauthorizedError(r)
        if status_code == 406:
            raise ContactsLimitExceededError(r)
        if status_code == 500:
            raise Exception
        return r
