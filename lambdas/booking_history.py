import json
import boto3
import time
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    try:
        if event['Authorization']:
            valid = True
        token = event['Authorization']
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
            'status': 403,
            'error_msg': msg
        })
    user_name = token[ind+1:]
    tickets_table = dynamodb.Table('ticket_data')

    try:
        response = tickets_table.scan(
            FilterExpression=Attr('user_name').eq(user_name)
        )
        # print(response)
        valid = False
        if response['Items']:
            valid = True
        if len(response['Items']) == 0:
            valid = False
    except:
        valid = False
    if not valid:
        return {
            'status': 200,
            'success': 'No booking history found.'
        }
    return {
        'status': 200,
        'data': response['Items']
    }