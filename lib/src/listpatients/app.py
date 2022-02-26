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
    return queue_table.scan()["Items"]
