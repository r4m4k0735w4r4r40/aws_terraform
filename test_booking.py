import boto3
import pytest
from moto import mock_dynamodb
from lambdas import booking
from lambdas import booking_history
import time
@pytest.fixture
def auth_token():
    token = str(int(time.time())+3600)
    token += ":test"
    return token
@mock_dynamodb
def test_booking_and_booking_history_lambda(auth_token):
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
        'Authorization':auth_token,
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
        'Authorization':auth_token,
        'body-json':{
            'bid':1001,
            'date':'05-08-2022'
        }
    }
    res = booking.lambda_handler(data,{})
    assert res['status'] == 400,res

    # Testing booking history
    data = {
        'Authorization':auth_token,
    }
    res = booking_history.lambda_handler(data,{})
    assert res['status'] == 200,res

    data = {
        'Authorization':auth_token,
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