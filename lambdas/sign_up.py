import json
import boto3
import time

def lambda_handler(event, context):
    # TODO implement
    # return event
    data = event['body-json']
    def data_validation(user):
        try:
            if user['user_name'] and user['password'] and user['email']:
                valid = True
        except:
            valid = False
        return valid
    if not (data_validation(data)):
        return {
            'status': 400,
            'data': data,
            'error_msg': 'Missing required fields.'
        }
    id = str(int(time.time()))
    data['id'] = id
    dynamodb = boto3.resource('dynamodb')
    try:
        table = dynamodb.Table('users_data')
        table.put_item(
            Item = data
        )
    except Exception:
        return {
            'status':500,
            'error_msg': 'Internal server error.'
        }
    return ({
        'status': 200,
        'success': 'User added successfully.'
    })