import json
import os

import boto3
import urllib3

TABLE_NAME = os.environ["TABLE_NAME"]
dynamodb_client = boto3.client("dynamodb")

callback_headers = {"Content-Type": "application/json"}
error_404 = {
    "statusCode": 400,
    "body": json.dumps({"error": "No record with specified blob_id"}),
}


def make_callback(event, context):
    """Callback with rekognition result"""
    blob_id = event["Records"][0]["dynamodb"]["Keys"]["blob_id"]["S"]

    result = dynamodb_client.get_item(
        TableName=TABLE_NAME, Key={"blob_id": {"S": blob_id}}
    ).get("Item")
    if not result:
        return error_404

    labels = result.get("labels").get("SS")
    if not labels:
        return error_404
    else:
        response_labels = []
        for label in labels:
            response_labels.append(json.loads(label))
        callback_url = result["callback_url"]["S"]
        data = {"blob_id": blob_id, "labels": response_labels}
        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            callback_url,
            body=json.dumps(data),
            headers=callback_headers,
            retries=False,
        )

        return {"statusCode": 200}
