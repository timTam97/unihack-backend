"""
Lambda authorizer for when clients try to connect
to the websocket. We check that their key is present
in the DB of generated keys.
"""
import json
import os
import secrets
import time

import boto3

key_table = boto3.resource("dynamodb").Table(os.environ.get("TABLE_NAME"))


def handler(event, _):
    print(event)
    entry_id = secrets.token_urlsafe(16)
    body = json.loads((event["body"]))
    key_table.put_item(
        Item={
            "entryId": entry_id,
            "phoneNumber": body["phoneNumber"],
            "timeCreated": int(time.time()),
            "patientName": body["patientName"],
        }
    )
    return json.dumps({"statusCode": 200, "body": {"entryId": entry_id}})
