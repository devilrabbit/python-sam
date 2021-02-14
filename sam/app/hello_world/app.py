import os

from .usecase import Usecase
from json import loads

from .models import Item
from .repository import RepositoryImpl
from .repository import FileDaoS3, DataDaoDynamoDB

REGION_NAME = os.environ.get('REGION_NAME', 'ap-northeast-1')
BUCKET_NAME = os.environ.get('BUCKET_NAME', 'bucket-example')
TABLE_NAME = os.environ.get('TABLE_NAME', 'table-example')

repository = RepositoryImpl(FileDaoS3(BUCKET_NAME), DataDaoDynamoDB(REGION_NAME, TABLE_NAME))
usecase = Usecase(repository)

def lambda_handler(event, context):
    for record in event['Records']:
        payload = loads(record['body'], parse_float=str)

        if 'item_id' not in payload or not payload['item_id']:
            continue
        if 'item_type' not in payload or not payload['item_type']:
            continue

        item = Item(payload['item_id'], payload['item_type'])
        usecase.delete(item)

