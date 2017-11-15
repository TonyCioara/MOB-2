import json
from flask import Flask, request
import pdb
# 1
from pymongo import MongoClient
# For serialization
from bson import Binary, Code
from bson.json_util import dumps

from until import JSONEncoder
app = Flask(__name__)

# 2
mongo = MongoClient('localhost', 27017)

# 3
app.db = mongo.local


@app.route('/person')
def person_route():
    person = {"name": "Eliel", 'age': 23}
    json_person = json.dumps(person)
    return (json_person, 200, None)


@app.route('/my_route')
def my_route():
    my_dict_from_json = request.json

    json_representation = JSONEncoder.encode(my_dict_from_json)

    return (json_representation, 200, None)


@app.route('/my_page')
def my_page_route():
    some_text = "I like cats"
    return some_text


@app.route('/users')
def get_user():

    # 1 Get Url params
    name = request.args.get('name')
    request.json

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


@app.route('/courses', methods = ['POST', 'GET'])
def get_or_post_course():

    if request.method == 'POST':
        courses_dict = request.json
        print(courses_dict)
        courses_collection = app.db.courses

        result = courses_collection.insert_one(courses_dict)

        # json_result = JSONEncoder().encode(courses_dict)
        json_result = dumps(courses_dict)

        return(json_result, 201, None)
    elif request.method == 'GET':
        courses_collection = app.db.courses
        collection = courses_collection.find()

        # json_result = JSONEncoder().encode(collection)
        json_result = dumps(collection)

        return (json_result, 200, None)


@app.route('/pets')
def pets_route():
    pet_1 = {"name": "Cow", 'age': 230}
    pet_2 = {"name": "Cat", 'age': 3}
    pet_3 = {"name": "Dawg", 'age': 2}
    pets = [pet_1, pet_2, pet_3]
    json_pets = json.dumps(pets)
    return json_pets


if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
