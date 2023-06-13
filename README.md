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