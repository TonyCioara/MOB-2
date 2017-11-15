....
...

import pdb

....
...

@app.route('/person')
def person_route():
    pdb.set_trace()

    person = {"name": "Eliel", 'age': 23}
    json_person = json.dumps(person)
    return (json_person, 200, None)
