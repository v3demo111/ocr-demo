from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from collections import OrderedDict

class SpeedSchema(object):

    def __init__(self, DB, ID):
        self.db = MongoClient("mongodb://localhost:27017/")[DB]
        self.ID = ID
        video_schema = {
            'vidID': {
                'type': 'string',
                'minlength': 1,
                'required': True,
            },
            'time': {
                'type': 'int',
                'required': True,
            },
            'speed': {
                'type': 'double',
                "required": True,
            }
        }

        collection = self.ID
        validator = {'$jsonSchema': {'bsonType': 'object', 'properties': {}}}
        required = []

        for field_key in video_schema:
            field = video_schema[field_key]
            properties = {'bsonType': field['type']}
            minimum = field.get('minlength')

            if type(minimum) == int:
                properties['minimum'] = minimum

            if field.get('required') is True: required.append(field_key)

            validator['$jsonSchema']['properties'][field_key] = properties

        if len(required) > 0:
            validator['$jsonSchema']['required'] = required

        query = [('collMod', collection),
                ('validator', validator)]

        try:
            self.db.create_collection(collection)
        except CollectionInvalid:
            pass

        command_result = self.db.command(OrderedDict(query))
    
    def create_one(self,obj):
        result=self.db[self.ID].insert_one(obj)





