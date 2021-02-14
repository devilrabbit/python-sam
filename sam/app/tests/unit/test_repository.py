import json
import pytest
import boto3

from moto import mock_sqs, mock_s3, mock_dynamodb2
from hello_world.repository import QueueSQS, FileDaoS3, DataDaoDynamoDB

TEST_REGION_NAME = 'ap-northeast-1'
TEST_QUEUE_NAME = 'test-queue'

@mock_sqs
class TestQueueSQSMethods:

    def setup_method(self, method):
        self._sqs = boto3.client('sqs', region_name=TEST_REGION_NAME)
        self._sqs.create_queue(QueueName=TEST_QUEUE_NAME)

    def test_send(self):
        queue = QueueSQS(TEST_REGION_NAME, TEST_QUEUE_NAME)
        queue.send('test')

TEST_BUCKET_NAME = 'test-bucket'

@mock_s3
class TestFileDaoS3Methods:

    def setup_method(self, method):
        self._s3 = boto3.resource('s3')
        self._bucket = self._s3.Bucket(TEST_BUCKET_NAME)
        self._bucket.create()

    def test_delete_objects(self):
        self._bucket.put_object(
            Key='test-id-001/item1',
            Body='abc'.encode('utf-8')
        )
        self._bucket.put_object(
            Key='test-id-001/item2',
            Body='abc'.encode('utf-8')
        )

        dao = FileDaoS3(TEST_BUCKET_NAME)
        dao.delete_files('test-id-001')

        objects = list(self._bucket.objects.filter(Prefix='test-id-001').all())
        assert len(objects) == 0

TEST_TABLE_NAME = 'test-table'

@mock_dynamodb2
class TestDataDaoDynamoDBMethods:

    def setup_method(self, method):
        self._dynamodb = boto3.resource('dynamodb', region_name=TEST_REGION_NAME)
        self._table = self._dynamodb.create_table(
            TableName=TEST_TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'item_id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'item_type',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'item_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'item_type',
                    'AttributeType': 'S'
                }
            ]
        )

    def test_delete_item(self):
        self._table.put_item(Item={
            'item_id': 'test-id-001',
            'item_type': 'test'
        })

        dao = DataDaoDynamoDB(TEST_REGION_NAME, TEST_TABLE_NAME)
        dao.delete_data('test-id-001', 'test')

        res = self._table.get_item(Key={'item_id': 'test-id-001', 'item_type': 'test'})
        assert 'Item' not in res