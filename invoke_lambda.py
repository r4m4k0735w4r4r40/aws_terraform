import json
import boto3

client = boto3.client('lambda')


def invoke_lambda(arn, data='User'):
    data = {'user':data}
    print(data)
    res = client.invoke(
        FunctionName=arn,
        Payload=json.dumps(data)
    )
    return json.load(res['Payload'])


# res = invoke_lambda("arn:aws:lambda:ap-south-1:728747466273:function:hello",'Test')
# print(res)