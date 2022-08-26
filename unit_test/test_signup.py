import boto3
import pytest
from moto import mock_dynamodb
from lambdas import sign_up
import json

@mock_dynamodb
def test_signup_lambda():
    ddb_client = boto3.resource('dynamodb')
    table_name = 'users_data'
    table = ddb_client.create_table(TableName=table_name,
                                    KeySchema=[{'AttributeName': 'user_name','KeyType': 'HASH'}],
                                    AttributeDefinitions=[{'AttributeName': 'user_name','AttributeType': 'S'}],
                                    ProvisionedThroughput={
                                        'ReadCapacityUnits': 5,
                                        'WriteCapacityUnits': 5
                                    })
    data = {
            'body': json.dumps(
                {
                    'user_name':'test',
                    'password':'passwd',
                    'email':'test@gmail.com'
                }
            )
        }
    res = sign_up.lambda_handler(data,{})
    assert res['statusCode'] == 200,res
    data = {
            'body': json.dumps(
                {
                    'user_name':'test',
                    'password':'passwd'
                }
            )
        }
    res = sign_up.lambda_handler(data,{})
    assert res['statusCode'] == 400,res