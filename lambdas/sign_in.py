import json
import boto3
import time

def lambda_handler(event, context):
    # TODO implement
    data = event['body']
    data = json.loads(data)
    def data_validation(cred):
        if 'user_name' in cred and 'password' in cred:
            valid = True
        else:
            valid = False
        return valid
    if not (data_validation(data)):
        return {
            "statusCode":400,
            "headers":{},
            "body":json.dumps(
                {
                    'status': 400,
                    'error_msg': 'Username/Password is required.'
                }
            ),
            "isBase64Encoded":False
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
            "statusCode":403,
            "headers":{},
            "body":json.dumps(
                {
                    'status': 403,
                    'error_msg' : 'Invalid credentials'
                }
            ),
            "isBase64Encoded":False
        }
    token = str(int(time.time())+3600)
    token += ":"+data['user_name']
    return {
        "statusCode":200,
        "headers":{},
        "body":json.dumps(
            {
                'status': 200,
                'auth_token': token,
                'token_expire_time': 3600
            }
        ),
        "isBase64Encoded":False
    }