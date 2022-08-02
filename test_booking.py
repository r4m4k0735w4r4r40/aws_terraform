import boto3
import pytest
from moto import mock_dynamodb
from lambdas import booking
from lambdas import booking_history
from boto3.dynamodb.conditions import Attr

@mock_dynamodb
def test_booking_and_booking_history_lambda():
    ddb_client = boto3.resource('dynamodb')
    table_name = 'ticket_data'
    table = ddb_client.create_table(TableName=table_name,
                                    KeySchema=[{'AttributeName': 'ticket_id','KeyType': 'HASH'}],
                                    AttributeDefinitions=[{'AttributeName': 'ticket_id','AttributeType': 'S'}],
                                    ProvisionedThroughput={
                                        'ReadCapacityUnits': 5,
                                        'WriteCapacityUnits': 5
                                    })
    data = {
        'Authorization':"1659436707:test",
        'body-json':{
            'bid':1001,
            'time':'07:00',
            'date':'05-08-2022'
        }
    }
    res = booking.lambda_handler(data,{})
    assert res['status'] == 200,res
    data = {
        'body-json':{
            'bid':1001,
            'time':'07:00',
            'date':'05-08-2022'
        }
    }
    res = booking.lambda_handler(data,{})
    assert res['status'] == 403,res
    data = {
        'Authorization':"1600000000:test",
        'body-json':{
            'bid':1001,
            'time':'07:00',
            'date':'05-08-2022'
        }
    }
    res = booking.lambda_handler(data,{})
    assert res['status'] == 403,res
    data = {
        'Authorization':"1659436707:test",
        'body-json':{
            'bid':1001,
            'date':'05-08-2022'
        }
    }
    res = booking.lambda_handler(data,{})
    assert res['status'] == 400,res

    # Testing booking history
    data = {
        'Authorization':"1659436707:test",
    }
    res = booking_history.lambda_handler(data,{})
    assert res['status'] == 200,res

    data = {
        'Authorization':"1659436707:test1",
    }
    res = booking_history.lambda_handler(data,{})
    assert res['status'] == 200,res

    res = booking_history.lambda_handler({},{})
    assert res['status'] == 403,res

    data = {
        'Authorization':"1600000000:test"
    }
    res = booking_history.lambda_handler(data,{})
    assert res['status'] == 403,res