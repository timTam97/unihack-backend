"""
Given an entryId, this function will return that entry's position in the queue,
as well as an estimated appointment time based on their position in the queue.
"""
import json
import os
import time

import boto3

queue_table = boto3.resource("dynamodb").Table(os.environ.get("TABLE_NAME"))
# queue_table = boto3.resource("dynamodb").Table(
#     "UnihackBackendStack-UnihackQueueTableFB843234-1OO0HKXLWU4GE"
# )


def handler(event, _):
    print(event)
    body = event["headers"]
    res = queue_table.scan()
    sorted_items = sorted(res["Items"], key=lambda x: int(x["timeCreated"]))
    # print(res)
    print(sorted_items)
    queue_pos = -1
    for i in range(len(sorted_items)):
        if sorted_items[i]["entryId"] == body["entryid"]:
            queue_pos = i

    if queue_pos == -1:
        return 404

    estimated_appointment_time = queue_pos * (
        int(os.environ.get("APPOINTMENT_TIME")) * 60
    ) + int(time.time())

    return {
        "queuePosition": queue_pos,
        "estimatedAppointmentTime": estimated_appointment_time,
    }
