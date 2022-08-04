import json
import boto3

client = boto3.client('lambda')


def invoke_lambda(arn, data={}):
    res = client.invoke(
        FunctionName=arn,
        Payload=json.dumps(data)
    )
    return json.load(res['Payload'])
# res = invoke_lambda("arn:aws:lambda:ap-south-1:728747466273:function:hello",'Test')
# print(res)
# import json
#
# import requests as req
#
# url = "https://fhktzads0e.execute-api.ap-south-1.amazonaws.com/dev/mydemoresource"
# r = req.post(url,data={"gfhg":"fssyug"},headers={"Auth":"dfgdygfy"})
# print(r.status_code)
# r = json.loads(r.text)
# print(r['Auth'])
# print(type(r['Auth']))