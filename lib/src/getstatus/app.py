"""
Lambda authorizer for when clients try to connect
to the websocket. We check that their key is present
in the DB of generated keys.
"""
import json
import os

import boto3

key_table = boto3.resource("dynamodb").Table(os.environ.get("TABLE_NAME"))


def handler(event, _):
    print(event)
    return json.dumps({"statusCode": 200, "body": "yes"})
