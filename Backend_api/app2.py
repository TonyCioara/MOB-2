import json
from flask import Flask, request, make_response
from flask_restful import Resource, Api
import pdb
# 1
from pymongo import MongoClient
# For serialization
from bson import Binary, Code
from bson.json_util import dumps

from until import JSONEncoder
app = Flask(__name__)
api = Api(app)

# 2
mongo = MongoClient('localhost', 27017)

# 3
app.db = mongo.local


class User(Resource):

    def post(self):

        name = request.args.get('name')

        new_user = request.json

        users_collection = app.db.users

        result = users_collection.insert_one(new_user)

        user = users_collection.find_one({'name': name})

        json_result = JSONEncoder().encode(result)

        return (json_result, 200, None)

    def get(self):

        # 1 Get Url params
        name = request.args.get('name')

        # 2 Our users users collection
        users_collection = app.db.users

        # 3 Find document in users collection
        result = users_collection.find_one(
            {'name': name}
        )

        # 4 Convert result to json from python dict
        json_result = JSONEncoder().encode(result)

        # 5 Return json as part of the response body
        return (json_result, 200, None)

    def put(self):

        name = request.args.get('name')

        new_user = request.json

        users_collection = app.db.users

        user = users_collection.find_one({'name': name})

        if user not in users_collection:
            result = users_collection.insert_one(new_user)
        else:
            result = users_collection[user] = new_user

        json_result = JSONEncoder().encode(result)

        return json_result


api.add_resource(User, '/users')


@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(JSONEncoder().encode(data), code)
    resp.headers.extend(headers or {})
    return resp


if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
