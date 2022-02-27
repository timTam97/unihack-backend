"""
Retrieves and removes the person at the front of the queue, texts them that
they are ready to attend, and also sends the location of the clinic.
"""
import json
import os

import boto3

queue_table = boto3.resource("dynamodb").Table(os.environ.get("TABLE_NAME"))


def response(message, status_code):
    return {
        "statusCode": str(status_code),
        "body": json.dumps(message),
        "headers": {
            "Content-Type": "application/json",
            # LMAO I HATE API GATEWAY
            "Access-Control-Allow-Origin": "*",
        },
    }


def handler(event, _):
    print(event)
    res = queue_table.scan()["Items"]
    for i in range(len(res)):
        for k in res[i]:
            if k == "timeCreated":
                res[i][k] = int(res[i][k])
    return response(res, 200)
