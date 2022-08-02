from invoke_lambda import *
import json
from behave import *
@given("interface arn '{arn}'")
def sign_up_in(context,arn):
    context.arn = arn
    print(context.config.userdata['token'])

@when("given data '{uname}' '{passwd}' '{mail}'")
def post_data(context,uname,passwd,mail):
    data = {'user_name': uname, 'password': passwd, 'email': mail}
    context.res = invoke_lambda(context.arn, {'body-json': data})

@when("given data '{uname}' '{passwd}'")
def post_data(context,uname,passwd):
    data = {'user_name': uname, 'password': passwd}
    context.res = invoke_lambda(context.arn,{'body-json':data})

@when("given data {bid} '{time}' '{date}'")
def post_data(context,bid,time,date):
    data = {'user_name': 'test', 'password': 'passwd'}
    res = invoke_lambda(context.arn,{'body-json':data})
    # res = json.load(res)
    token = res['auth_token']
    data = {'bid':bid,'time':time,'date':date}
    context.res = invoke_lambda(context.arn,{'Authorization':token,'body-json':data})
@when("requested for history")
def post_data(context):
    data = {'user_name': 'test', 'password': 'passwd'}
    res = invoke_lambda(context.arn,{'body-json':data})
    # res = json.load(res)
    token = res['auth_token']
    context.res = invoke_lambda(context.arn,{'Authorization':token})

@then("the {end} response is {num}")
def the_response(context,end, num):
    assert context.res['status'] == int(num), context.res

