import json
from urllib.parse import urlencode

import requests

from eventbrite.exceptions import UnauthorizedError, WrongFormatInputError, ContactsLimitExceededError


class Client(object):
    URL = "https://www.eventbriteapi.com/v3/"
    AUTH_URL = "https://www.eventbrite.com/oauth/"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, api_key=None, client_secret=None, redirect_uri=None, access_token=None):
        self.CLIENT_ID = api_key
        self.CLIENT_SECRET = client_secret
        self.REDIRECT_URI = redirect_uri
        if access_token:
            self.set_token(access_token)

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
        self.headers.update({"Content-Type": "application/x-www-form-urlencoded"})
        return self.post("token", data=body, auth_url=True)

    def set_token(self, token):
        self.headers.update({"Authorization": f"Bearer {token}"})

    def get_current_user(self):
        return self.get("users/me/")

    def get_user_organizations(self):
        return self.get("users/me/organizations/")

    def list_categories(self):
        return self.get("categories")

    def list_subcategories(self):
        return self.get("subcategories")

    def list_formats(self):
        return self.get("formats")

    def list_venues(self, organization_id):
        return self.get(f"organizations/{organization_id}/venues/")

    def list_organizers(self, organization_id):
        return self.get(f"organizations/{organization_id}/organizers/")

    def list_events(self, organization_id):
        return self.get(f"organizations/{organization_id}/events/")

    def get_event(self, event_id):
        return self.get(f"events/{event_id}/")

    def create_event(self, organization_id, data):
        return self.post(f"organizations/{organization_id}/events/", data=json.dumps(data))

    def get_order(self, order_id):
        return self.get(f"orders/{order_id}/")

    def list_webhooks(self, organization_id):
        return self.get(f"organizations/{organization_id}/webhooks/")

    def create_webhook(self, organization_id, endpoint_url, actions, event_id=""):
        data = {"endpoint_url": endpoint_url, "actions": actions, "event_id": event_id}
        return self.post(f"organizations/{organization_id}/webhooks/", data=json.dumps(data))

    def delete_webhook(self, webhook_id):
        return self.delete(f"webhooks/{webhook_id}/")

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

    def request(self, method, endpoint, auth_url=False, **kwargs):
        url = self.AUTH_URL if auth_url else self.URL
        return requests.request(method, url + endpoint, headers=self.headers, **kwargs)

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
