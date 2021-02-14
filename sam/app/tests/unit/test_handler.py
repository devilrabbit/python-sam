import os
import pytest
import mock
import boto3
from moto import mock_s3, mock_dynamodb2

REGION_NAME = 'ap-northeast-1'
BUCKET_NAME = 'bucket-test'
TABLE_NAME = 'table-test'

@pytest.fixture()
def sqs_event():
    """ Generates SQS Event"""

    return {
        "Records": [
            {
            "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
            "receiptHandle": "MessageReceiptHandle",
            "body": "{\"item_id\":\"test-id-001\",\"item_type\":\"test\"}",
            "attributes": {
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1523232000000",
                "SenderId": "123456789012",
                "ApproximateFirstReceiveTimestamp": "1523232000001"
            },
            "messageAttributes": {},
            "md5OfBody": "7b270e59b47ff90a553787216d55d91d",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:MyQueue",
            "awsRegion": "us-east-1"
            }
        ]
    }

@pytest.fixture()
def aws_resources():
    with mock_s3() as _, mock_dynamodb2() as _:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(BUCKET_NAME)
        bucket.create()

        dynamodb = boto3.resource('dynamodb', region_name=REGION_NAME)
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                { 'AttributeName': 'item_id', 'KeyType': 'HASH' },
                { 'AttributeName': 'item_type', 'KeyType': 'RANGE' }
            ],
            AttributeDefinitions=[
                { 'AttributeName': 'item_id', 'AttributeType': 'S' },
                { 'AttributeName': 'item_type', 'AttributeType': 'S' }
            ]
        )

        yield bucket, table

@mock.patch.dict(os.environ, {'REGION_NAME': REGION_NAME, 'BUCKET_NAME': BUCKET_NAME, 'TABLE_NAME': TABLE_NAME})
def test_lambda_handler(sqs_event, aws_resources, mocker):

    item_id = 'test-id-001'
    item_type = 'test'

    bucket, table = aws_resources

    bucket.put_object(
        Key='%s/item1' % item_id,
        Body='abc'.encode('utf-8')
    )
    table.put_item(Item={
        'item_id': item_id,
        'item_type': item_type
    })

    from hello_world import app
    app.lambda_handler(sqs_event, "")

    # check file deleted
    objects = list(bucket.objects.filter(Prefix=item_id).all())
    assert len(objects) == 0

    # check data deleted
    res = table.get_item(Key={'item_id': item_id, 'item_type': item_type})
    assert 'Item' not in res
