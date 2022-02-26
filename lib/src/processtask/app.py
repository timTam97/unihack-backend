"""
Retrieves and removes the person at the front of the queue, texts them that
they are ready to attend, and also sends the location of the clinic.
"""
import json
import os

import boto3

queue_table = boto3.resource("dynamodb").Table(os.environ.get("TABLE_NAME"))


def handler(event, _):
    print(event)
    body = json.loads((event["body"]))
    res = queue_table.scan()
    sortedItems = sorted(res["Items"], key=lambda x: int(x["timeCreated"]))
