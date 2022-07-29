import json
import boto3
import time
import botocore

def lambda_handler(event, context):
    # TODO implement
    data = event['body-json']

    def data_validation(cred):
        try:
            if 'user_name' in cred and 'password' in cred:
                valid = True
            else:
                valid = False
        except:
            valid = False
        return valid
    if not (data_validation(data)):
        return {
            'status': 400,
            'error_msg': 'Username/Password is required.'
        }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users_data')
    try:
        response = table.get_item(
            Key = {
                'user_name': data['user_name']
            }
        )
        if response['Item']:
            item = response['Item']
            if item['password'] == data['password']:
                valid = True
            else:
                valid = False
    except:
        valid = False
    if not valid:
        return {
            'status': 403,
            'error_msg' : 'Invalid credentials'
        }
    token = str(int(time.time())+3600)
    token += ":"+data['user_name']
    return {
        'status': 200,
        'auth_token': token,
        'token_expire_time': 3600
    }