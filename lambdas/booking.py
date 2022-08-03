import json
import boto3
import time


def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    try:
        if event['headers']['Auth']:
            valid = True
        token = event['headers']['Auth']
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
            "statusCode":403,
            "headers":{},
            "body":json.dumps(
                {
                    'status': 403,
                    'error_msg': msg
                }
            ),
            "isBase64Encoded":False
        }
    booking_data = event['body']
    booking_data = json.loads(booking_data)
    try:
        if booking_data['date'] and booking_data['time']:
            valid = True
    except:
        valid = False
    if not valid:
        return {
            "statusCode":400,
            "headers":{},
            "body":json.dumps(
                {
                    'status': 400,
                    'error_msg': 'Booking Date/Time Required.'
                }
            ),
            "isBase64Encoded":False
        }
    # auth = token = event['Auth']
    token = event['headers']['Auth']
    user_name = token[ind + 1:]
    tickets_table = dynamodb.Table('ticket_data')
    booking_data['ticket_id'] = str(int(time.time()))
    booking_data['user_name'] = user_name
    tickets_table.put_item(
        Item=booking_data
    )
    return {
        "statusCode":200,
        "headers":{},
        "body":json.dumps(
            {
                'status': 200,
                'msg': 'Bus booked successfully.',
                'data': booking_data
            }
        ),
        "isBase64Encoded":False
    }
