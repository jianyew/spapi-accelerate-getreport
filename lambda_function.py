
import json
import requests
import boto3
from urllib.parse import parse_qs, urlencode



def lambda_handler(event, context):
    print(event)
    request = event['Records'][0]['cf']['request']
    params = {k : v[0] for k, v in parse_qs(request['querystring']).items()}
    ohost = params['ohost']
    print(ohost)
    path = request['uri']
    print(path)
    querystring = params['p']
    s3uri = "https://" + ohost + path + "?" + querystring;
    print(s3uri)
    s3key = path[1:]

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('gerp-download')
    obj = bucket.Object(s3key)

    r = requests.get(s3uri, stream=True)
    print(r.raw)

    obj.upload_fileobj(r.raw)

    return request
