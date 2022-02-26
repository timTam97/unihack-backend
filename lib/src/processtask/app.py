"""
Retrieves and removes the person at the front of the queue, texts them that
they are ready to attend, and also sends the location of the clinic.
"""
import json
import os

import boto3

queue_table = boto3.resource("dynamodb").Table(os.environ.get("TABLE_NAME"))
sns = boto3.client("sns")


def handler(event, _):
    print(event)
    res = queue_table.scan()
    print(res)
    if not res["Items"]:
        return 404
    front_queue_member = sorted(res["Items"], key=lambda x: int(x["timeCreated"]))[0]
    queue_table.delete_item(Key={"entryId": front_queue_member["entryId"]})
    sns.publish(
        PhoneNumber=front_queue_member["phoneNumber"],
        Message="Hi {}, you are at the front of the queue! Head through for your 10 minute appointment.".format(
            front_queue_member["patientName"]
        ),
        MessageAttributes={
            "AWS.SNS.SMS.SenderID": {"DataType": "String", "StringValue": "QubeBooking"}
        },
    )
    return 200
