import json
import boto3
import time

def lambda_handler(event, context):
    # TODO implement
    # return event
    data = event['body']
    data = json.loads(data)
    def data_validation(user):
        try:
            if user['user_name'] and user['password'] and user['email']:
                valid = True
        except:
            valid = False
        return valid
    if not (data_validation(data)):
        return {
            "statusCode":400,
            "headers":{},
            "body":json.dumps(
                {
                    'status': 400,
                    'error_msg': 'Missing required fields.'
                }
            ),
            "isBase64Encoded":False
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
            "statusCode":500,
            "headers":{},
            "body":json.dumps(
                {
                    'status':500,
                    'error_msg': 'Internal server error.'
                }
            ),
            "isBase64Encoded":False
        }
    return ({
        "statusCode":200,
        "headers":{},
        "body":json.dumps(
            {
                'status': 200,
                'success': 'User added successfully.'
            }
        ),
        "isBase64Encoded":False
    })