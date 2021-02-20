import json
from models import User
from handlers import endpoint_handlers


class RestAPI:
    def __init__(self, database=None):
        if database:
            self.user_data = {f'{user["name"]}': User(user['name'], user['owes'], user['owed_by']) for user in
                              database['users']}
        else:
            self.user_data = {}

    def get(self, url, payload=None):
        allowed = ['/users']
        if url in allowed:
            return endpoint_handlers[url](self.user_data, payload)
        return json.dumps({'error': 'endpoint not found/request not allowed', 'status_code': 404})

    def post(self, url, payload=None):
        allowed = ['/iou', '/add']
        if url in allowed:
            if payload:
                return endpoint_handlers[url](self.user_data, payload)
            return json.dumps({'error': 'empty request payload'})
        return json.dumps({'error': 'endpoint not found/req not allowed', 'status_code': 404})
