from uuid import uuid4

from pymongo import MongoClient

from ..settings import settings


class MongoDBService:
    client = MongoClient(settings.DATABASES['default']['URL'])
    db = client[settings.DATABASES['default']['DATABASE']]
    USER_COLLECTION = 'User'

    def create_user(self, data):
        data['id'] = str(uuid4())
        self.db[self.USER_COLLECTION].insert_one(data)

    def get_user(self, *args, **kwargs):
        cursor = self.db[self.USER_COLLECTION].find_one(**kwargs)

        return cursor
