import boto3

from abc import ABCMeta, abstractmethod
from .models import Item
from .errors import FileDeleteError, RecordDeleteError, DeleteError

class QueueSQS:
    def __init__(self, region: str, queue_name: str):
        self._sqs = boto3.resource('sqs', region_name=region)
        self._queue = self._sqs.get_queue_by_name(QueueName=queue_name)

    def send(self, message: str):
        self._queue.send_message(MessageBody=message)

class FileDao(metaclass=ABCMeta):
    @abstractmethod
    def delete_files(self, prefix: str):
        raise NotImplementedError

class FileDaoS3(FileDao):
    def __init__(self, bucket_name: str):
        self._s3 = boto3.resource('s3')
        self._bucket = self._s3.Bucket(bucket_name)

    def delete_files(self, prefix: str) -> bool:
        try:
            objects = []
            for obj in self._bucket.objects.filter(Prefix=prefix):
                objects.append({'Key': obj.key})

            if len(objects) == 0:
                return False

            response = self._bucket.delete_objects(Delete={'Objects': objects, 'Quiet': False})
            if ('Errors' not in response) or (not response['Errors']):
                return False
            return True
        except Exception as e:
            raise FileDeleteError from e

class DataDao(metaclass=ABCMeta):
    @abstractmethod
    def delete_data(self, id: str, item_type: str):
        raise NotImplementedError

class DataDaoDynamoDB(DataDao):
    def __init__(self, region: str, table_name: str):
        self._dynamodb = boto3.resource('dynamodb', region_name=region)
        self._table = self._dynamodb.Table(table_name)

    def delete_data(self, id: str, item_type: str):
        try:
            self._table.delete_item(
                Key={
                    'item_id': id,
                    'item_type': item_type
                }
            )
        except Exception as e:
            raise RecordDeleteError from e

class Repository(metaclass=ABCMeta):
    @abstractmethod
    def delete(self, item: Item):
        raise NotImplementedError

class RepositoryImpl(Repository):
    def __init__(self, file_dao: FileDao, data_dao: DataDao):
        self._file_dao = file_dao
        self._data_dao = data_dao

    def delete(self, item: Item):
        try:
            self._file_dao.delete_files("%s/" % item.item_id)
            self._data_dao.delete_data(item.item_id, item.item_type)
        except Exception as e:
            raise DeleteError from e