import json
from models import User


def _user_handler(user_data, payload):
    response = {'users': []}
    if payload:
        payload = json.loads(payload)
        for name in payload['users']:
            user = user_data.get(name, None)
            if user:
                response['users'].append({'name': user.name,
                                          'owes': user.owes,
                                          'owed_by': user.owed_by,
                                          'balance': user.balance
                                          })
            response['users'] = sorted(response['users'], key=lambda i: i['name'])
        return json.dumps(response)

    for name, user in user_data.items():
        response['users'].append({'name': user.name,
                                  'owes': user.owes,
                                  'owed_by': user.owed_by,
                                  'balance': user.balance
                                  })
        response['users'] = sorted(response['users'], key=lambda i: i['name'])
    return json.dumps(response)


def _create_user_handler(user_data, payload):
    payload = json.loads(payload)
    if payload['user'] in user_data:
        return json.dumps({'integrity_error': 'name already exists'})
    else:
        new_user = User(payload['user'])
        user_data[payload['user']] = new_user
        return json.dumps(
            {'name': new_user.name, 'owes': new_user.owes, 'owed_by': new_user.owed_by, 'balance': new_user.balance})


def _iou_handler(user_data, payload):
    payload = json.loads(payload)
    amount = payload['amount']

    if amount > 0:
        lender = user_data.get(payload['lender'], None)
        borrower = user_data.get(payload['borrower'], None)

        if lender and borrower:
            lender.lend(borrower, amount)
            return json.dumps(
                {'users': sorted([{'name': lender.name, 'owes': lender.owes, 'owed_by': lender.owed_by,
                                   'balance': lender.balance},
                                  {'name': borrower.name, 'owes': borrower.owes, 'owed_by': borrower.owed_by,
                                   'balance': borrower.balance}], key=lambda i: i['name'])})

    else:
        return json.dumps({'error': 'amount must be positive integer'})


endpoint_handlers = {
    '/users': _user_handler,
    '/add': _create_user_handler,
    '/iou': _iou_handler,
}
