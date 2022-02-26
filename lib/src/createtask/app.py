"""
Adds a new entry to our virtual queue.
Generates a random ID and returns this to the caller.
"""
import json
import os
import secrets
import time

import boto3

queue_table = boto3.resource("dynamodb").Table(os.environ.get("TABLE_NAME"))


def handler(event, _):
    print(event)
    entry_id = secrets.token_urlsafe(16)
    body = json.loads((event["body"]))
    queue_table.put_item(
        Item={
            "entryId": entry_id,
            "phoneNumber": body["phoneNumber"],
            "timeCreated": int(time.time()),
            "patientName": body["patientName"],
        }
    )
    return {"entryId": entry_id}
