# eventbrite-python
![](https://img.shields.io/badge/version-0.1.0-success) ![](https://img.shields.io/badge/Python-3.8%20|%203.9%20|%203.10%20|%203.11-4B8BBE?logo=python&logoColor=white)  

*eventbrite-python* is an API wrapper for Eventbrite, written in Python.  
This library uses Oauth2 for authentication.
## Installing
```
pip install eventbrite-python
```
## Usage
```python
# if you have an access token:
from eventbrite.client import Client
client = Client(access_token=access_token)
```
```python
# Or if you are using Oauth2 to get an access_token:
from eventbrite.client import Client
client = Client(api_key, client_secret, redirect_uri)
```
To obtain and set an access token:
1. ***Build authorization URL***
```python
url = client.authorization_url(state="123456")
```
2. ***Get access token***
```python
token = client.get_access_token(code)
```
3. ***Set token***
```python
client.set_token(access_token)
```
### Info
#### Get current user
```python
me = client.get_current_user()
```
#### Get user organizations
```python
organizations = client.get_user_organizations()
```
#### List categories
```python
categories = client.list_categories()
```
#### List subcategories
```python
subcategories = client.list_subcategories()
```
#### List formats
```python
formats = client.list_formats()
```
#### List venues
```python
venues = client.list_formats(organization_id)
```
#### List organizers
```python
organizers = client.list_organizers(organization_id)
```
### Events
#### List events
```python
events = client.list_events(organization_id)
```
#### Get event
```python
event = client.get_event(event_id)
```
#### Create event
```python
event = client.create_event(organization_id, data)
```
### Orders
#### Get order
```python
order = client.get_order(order_id)
```
### Webhooks
#### List webhooks
```python
webhooks = client.list_webhooks(organization_id)
```
#### Create webhook
```python
webhook = client.create_webhook(organization_id,  endpoint_url, actions, event_id="")
```
#### Delete webhook
```python
deleted = client.delete_webhook(webhook_id)
```