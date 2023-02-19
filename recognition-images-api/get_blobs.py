import json
import os

import boto3

TABLE_NAME = os.environ["TABLE_NAME"]

dynamodb_client = boto3.client("dynamodb")
error_404 = {"statusCode": 404, "body": json.dumps({"error": "Blob not found"})}


def get_blobs(event, context):
    """Gets info about blob by blob_id"""
    blob_id = event["pathParameters"]["blob_id"]

    result = dynamodb_client.get_item(
        TableName=TABLE_NAME, Key={"blob_id": {"S": blob_id}}
    ).get("Item")

    if not result:
        return error_404

    try:
        labels = result.get("labels").get("SS")
        response_labels = []
        for label in labels:
            response_labels.append(json.loads(label))
    except AttributeError:
        return error_404

    return {
        "statusCode": 200,
        "body": json.dumps({"blob_id": blob_id, "labels": response_labels}),
    }
