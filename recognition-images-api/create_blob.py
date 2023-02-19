import json
import os
import uuid

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

TABLE_NAME = os.environ["TABLE_NAME"]
BUCKET_NAME = os.environ["BUCKET_NAME"]

dynamodb_client = boto3.client("dynamodb")
s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))

response_bad_request = {"statusCode": 400, "body": json.dumps({"error": "Invalid callback url supplied"})}


def create_blob(event, context):
    """Generates id and saves blob info (blob_id, callback_url)
    """

    event_body = event['body']

    if not event_body:
        return response_bad_request

    callback_url = json.loads(event_body)["callback_url"]
    if not callback_url:
        return response_bad_request

    blob_id = str(uuid.uuid4())

    dynamodb_client.put_item(
        TableName=TABLE_NAME,
        Item={
            'blob_id': {"S": blob_id},
            'callback_url': {"S": callback_url}
        }
    )

    try:
        upload_url = s3_client.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': f"{blob_id}"
            },
            ExpiresIn=3600,
            HttpMethod='PUT'
        )
    except ClientError as e:
        return e

    return {
        "statusCode": 201,
        "body": json.dumps(
            {
                "blob_id": blob_id,
                "upload_url": upload_url
            }
        )
    }
