import json
import boto3
import time


def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    try:
        if event['Authorization']:
            valid = True
        token = event['Authorization']
        ind = token.index(':')
        ex_time = int(token[:ind])
        if int(time.time()) > ex_time:
            valid = False
            msg = "Invalid Token/Expired."
    except:
        valid = False
        msg = 'Missing authentication token'
    if not valid:
        return {
            'status': 403,
            'error_msg': msg
        }
    booking_data = event['body-json']
    try:
        if booking_data['date'] and booking_data['time']:
            valid = True
    except:
        valid = False
    if not valid:
        return {
            'status': 400,
            'error_msg': 'Booking Date/Time Required.'
        }
    auth = token = event['Authorization']
    user_name = token[ind + 1:]
    tickets_table = dynamodb.Table('ticket_data')
    booking_data['ticket_id'] = str(int(time.time()))
    booking_data['user_name'] = user_name
    tickets_table.put_item(
        Item=booking_data
    )
    return {
        'status': 200,
        'succ': 'Bus booked successfully.',
        'data': booking_data
    }
