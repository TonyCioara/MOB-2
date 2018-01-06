import json
from flask import Flask, request, make_response
from flask_restful import Resource, Api
from pymongo import ReturnDocument
import pdb
# 1
import bcrypt
from pymongo import MongoClient
# For serialization
from bson import Binary, Code
from bson.json_util import dumps

from until import JSONEncoder
app = Flask(__name__)
api = Api(app)

# 2å
mongo = MongoClient("mongodb://Tony:12345678@ds131687.mlab.com:31687/trip_planner_db")

# 3
app.bcrypt_rounds = 12
app.db = mongo.trip_planner_db


def validate_auth(email, password):

    user_collection = app.db.users
    user = user_collection.find_one({'email': email})

    if user is None:
        return False
    else:
        encodedPassword = password.encode('utf-8')

        if bcrypt.hashpw(encodedPassword, user['password']) == user['password']:
            return True
        else:
            return False


def authenticated_request(func):

    def wrapper(*args, **kwargs):
        auth = request.authorization

        if not auth or not validate_auth(auth.username, auth.password):
            return ({'error': 'Basic Auth Required.'}, 401, None)

        return func(*args, **kwargs)

    return wrapper


class User(Resource):

    def post(self):

        users_collection = app.db.users

        # 2 parsed Request Body
        new_user = request.json

        if ('password' in new_user and 'email' in new_user):
            password = new_user['password']
            encodedPassword = password.encode('utf-8')

            hashed = bcrypt.hashpw(
                encodedPassword, bcrypt.gensalt(app.bcrypt_rounds)
            )

        new_user['password'] = hashed

        result = users_collection.insert_one(new_user)

        user = users_collection.find_one({'_id': result.inserted_id})

        if result is not None:
            return(None, 201, {"Content-Type": "application/json", "User": "Tony"})
        else:
            return (None, 400, None)

    @authenticated_request
    def get(self):

        # 1 Get Url params
        email = request.authorization.username

        # 2 Our users users collection
        users_collection = app.db.users

        # 3 Find document in users collection
        result = users_collection.find_one(
            {'email': email}
        )

        if result is not None:
            result.pop('password')
            return (result, 200, None)
        else:
            return(None, 404, None)

    @authenticated_request
    def put(self):

        email = request.authorization.username

        users_collection = app.db.users

        # 2 parsed Request Body
        new_user = request.json

        result = users_collection.find_one_and_replace({'email': email}, new_user, return_document=ReturnDocument.AFTER)

        # pdb.set_trace()

        if result is not None:
            result.pop('password')
            return(result, 200, {"Content-Type": "application/json", "User": "Tony"})
        else:
            return (None, 404, None)

    @authenticated_request
    def patch(self):

        email = request.authorization.username

        users_collection = app.db.users

        # 2 parsed Request Body
        new_user = request.json
        set_values = {}
        if 'email' in new_user:
            set_values['email'] = new_user["email"]
        if 'trips' in new_user:
            set_values['trips'] = new_user["trips"]

        mongo_set = {'$set': set_values}

        result = users_collection.find_one_and_update(
            {'email': email},
            mongo_set,
            return_document=ReturnDocument.AFTER
        )

        if result is not None:
            result.pop('password')
            return(result, 200, {"Content-Type": "application/json", "User": "Tony"})
        else:
            return (None, 404, None)


class Trip(Resource):

    def get(self):
        destination = request.args.get('destination')

        trips_collection = app.db.trips

        result = trips_collection.find_one({'destination': destination})

        if result is not None:
            return (result, 200, None)
        else:
            return(None, 404, None)

    def post(self):

        trips_collection = app.db.trips

        # 2 parsed Request Body
        new_destination = request.json

        result = trips_collection.insert_one(new_destination)

        trip = trips_collection.find_one({'_id': result.inserted_id})

        # pdb.set_trace()

        if result is not None:
            return(trip, 201, {"Content-Type": "application/json", "User": "Tony TJ"})
        else:
            return (None, 400, None)

    def put(self):

        destination = request.args.get('destination')

        trips_collection = app.db.trips

        # 2 parsed Request Body
        new_destination = request.json

        result = trips_collection.find_one_and_replace({'destination': destination}, new_destination, return_document=ReturnDocument.AFTER)

        # pdb.set_trace()

        if result is not None:
            return(result, 200, {"Content-Type": "application/json", "User": "Tony TJ"})
        else:
            return (None, 404, None)

    def patch(self):

        destination = request.args.get('destination')

        trips_collection = app.db.trips

        # 2 parsed Request Body
        new_destination = request.json
        set_values = {}
        if 'destination' in new_destination:
            set_values['destination'] = new_destination["destination"]
        if 'trip_day_amount' in new_destination:
            set_values['trip_day_amount'] = new_destination["trip_day_amount"]

        mongo_set = {'$set': set_values}

        result = trips_collection.find_one_and_update(
            {'destination': destination},
            mongo_set,
            return_document=ReturnDocument.AFTER
        )

        if result is not None:
            return(result, 200, {"Content-Type": "application/json", "User": "Tony TJ"})
        else:
            return (None, 404, None)


api.add_resource(User, '/users')
api.add_resource(Trip, '/trips')


@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(JSONEncoder().encode(data), code)
    resp.headers.extend(headers or {})
    return resp


if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
