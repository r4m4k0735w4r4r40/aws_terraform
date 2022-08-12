from behave import *
import json
import boto3

client = boto3.client('lambda')


def invoke_lambda(arn, data={}):
    res = client.invoke(
        FunctionName=arn,
        Payload=json.dumps(data)
    )
    return json.load(res['Payload'])

@fixture()
def before_all(context):
    context.auth_token = ""

@given("interface arn '{arn}'")
def sign_up_in(context,arn):
    context.arn = arn

@when("given user data '{uname}' '{passwd}' '{mail}'")
def post_data(context,uname,passwd,mail):
    data = {'user_name': uname, 'password': passwd, 'email': mail}
    context.res = invoke_lambda(context.arn, {'body': json.dumps(data)})

@when("given login data '{uname}' '{passwd}'")
def post_data(context,uname,passwd):
    data = {'user_name': uname, 'password': passwd}
    res = invoke_lambda(context.arn,{'body':json.dumps(data)})
    context.res = res
    # res = json.loads(res['body'])
    # context.auth_token = res['auth_token']

@when("given booking data '{bid}' '{time}' '{date}'")
def post_data(context,bid,time,date):
    data = {'user_name': 'test', 'password': 'passwd'}
    res = invoke_lambda('signin_lambda',{'body':json.dumps(data)})
    res = json.loads(res['body'])
    token = res['auth_token']
    data = {'bid':bid,'time':time,'date':date}
    context.res = invoke_lambda(context.arn,{'headers':{'Auth':token},'body':json.dumps(data)})
@when("requested for history")
def post_data(context):
    data = {'user_name': 'test', 'password': 'passwd'}
    res = invoke_lambda('signin_lambda',{'body':json.dumps(data)})
    res = json.loads(res['body'])
    token = res['auth_token']
    context.res = invoke_lambda(context.arn,{'headers':{'Auth':token}})

@then("the {end} response is {num}")
def the_response(context,end, num):
    assert context.res['statusCode'] == int(num), context.res['statusCode']
    # assert False,context