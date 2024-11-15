from pymongo import MongoClient

from ..settings import settings


class MongoDBService:
    '''MongoDB Interface Layer

        Interfaces with the MongoDB connection defined in settings. Can optionally connect to a particular Collection by
        passing `collection='<collection>'` upon instantiation. Default Collection is `User`.
    '''
    client = MongoClient(settings.DATABASES['default']['CLIENT'])
    db = client[settings.DATABASES['default']['NAME']]

    class DoesNotExist(Exception):
        def __str__(self):
            return 'Document Does Not Exist'
    
    class MultipleDocumentsReturned(Exception):
        def __str__(self):
            return 'Multiple Documents Returned'

    def __init__(self, collection: str = 'User', *args, **kwargs):
        self.collection = self.db[collection]

    def __iter__(self):
        return iter([] if self.cursor is None else [doc for doc in self.cursor])

    def execute(self, find_one: bool = False):
        self.cursor = self.collection.find(self.query)

        if not find_one:
            return iter(self)
        
        num_docs = self.cursor.explain().get('executionStats', {}).get('nReturned', 0)

        if num_docs < 1:
            raise self.DoesNotExist
        
        elif num_docs > 1:
            raise self.MultipleDocumentsReturned
        
        return self.cursor.next()

    def filter(self, *args, **kwargs):
        execute = kwargs.pop('execute', False)
        self.query = kwargs

        if not execute:
            return self
        
        return self.execute()

    def get(self, *args, **kwargs):
        self.query = kwargs

        return self.execute(find_one=True)

    def get_or_create(self, *args, **kwargs):
        try:
            return (self.get(**kwargs), False)
        
        except self.DoesNotExist:
            return (self.create(**kwargs), True)

    def create(self, *args, **kwargs):
        instance = self.collection.insert_one(kwargs)

        return instance

    def update(self, instance: dict, *args, **kwargs):
        result = self.collection.update_one(filter=kwargs, update={
            '$set': instance
        })

        if not result.modified_count:
            pass

        return instance
