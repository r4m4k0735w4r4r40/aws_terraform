import boto3
import pytest
from moto import mock_dynamodb
from lambdas import sign_in

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
        'user_name':'test',
        'password':'passwd',
        'email':'test@gmail.com'
    }
    table.put_item(
        Item=data
    )
    data = {
        'body-json':{
            'user_name':'test',
            'password':'passwd'
        }
    }
    res = sign_in.lambda_handler(data,{})
    assert res['status'] == 200,res
    data = {
        'body-json':{
            'user_name':'test'
        }
    }
    res = sign_in.lambda_handler(data,{})
    assert res['status'] == 400,res
    data = {
        'body-json':{
            'user_name':'test',
            'password':'passwd1'
        }
    }
    res = sign_in.lambda_handler(data,{})
    assert res['status'] == 403,res
    data = {
        'body-json':{
            'user_name':'test1',
            'password':'passwd'
        }
    }
    res = sign_in.lambda_handler(data,{})
    assert res['status'] == 403,res