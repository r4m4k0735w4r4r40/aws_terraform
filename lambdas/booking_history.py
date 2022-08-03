import json
import boto3
import time
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    try:
        if event['headers']['Auth']:
            valid = True
        token = event['headers']['Auth']
        ind = token.index(':')
        ex_time = int(token[:ind])
        if(int(time.time())>ex_time):
            valid = False
            msg = "Invalid Token/Expired."
    except :
        valid = False
        msg = 'Missing authentication token'
    if not valid:
        return ({
            "statusCode":403,
            "headers":{},
            "body":json.dumps(
                {
                    'status': 403,
                    'error_msg': msg
                }
            ),
            "isBase64Encoded":False
        })
    user_name = token[ind+1:]
    tickets_table = dynamodb.Table('ticket_data')
    response = tickets_table.scan(
            FilterExpression=Attr('user_name').eq(user_name)
    )
    valid = True
    if len(response['Items']) == 0:
        valid = False
    if not valid:
        return {
            "statusCode":200,
            "headers":{},
            "body":json.dumps(
                {
                    'status': 200,
                    'success': 'No booking history found.'
                }
            ),
            "isBase64Encoded":False
        }
    data = response['Items']
    return {
        "statusCode":200,
        "headers":{},
        "body":json.dumps(
            {
                'status': 200,
                'data': data
            }
        ),
        "isBase64Encoded":False
    }