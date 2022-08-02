import boto3
import pytest
from moto import mock_dynamodb
from lambdas import sign_up

@mock_dynamodb
def test_signup_lambda():
    ddb_client = boto3.resource('dynamodb',region_name="ap-south-1")
    table_name = 'users_data'
    table = ddb_client.create_table(TableName=table_name,
                                    KeySchema=[{'AttributeName': 'user_name','KeyType': 'HASH'}],
                                    AttributeDefinitions=[{'AttributeName': 'user_name','AttributeType': 'S'}],
                                    ProvisionedThroughput={
                                        'ReadCapacityUnits': 5,
                                        'WriteCapacityUnits': 5
                                    })
    data = {
        'body-json':{
            'user_name':'test',
            'password':'passwd',
            'email':'test@gmail.com'
        }
    }
    res = sign_up.lambda_handler(data,{})
    assert res['status'] == 200,res['status']
    data = {
        'body-json':{
            'user_name':'test',
            'password':'passwd'
        }
    }
    res = sign_up.lambda_handler(data,{})
    assert res['status'] == 400,res['status']