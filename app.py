from flask import Flask
from flask_cors import CORS, cross_origin
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

from student import Student

app = Flask(__name__)
ors = CORS(app)
app.config.from_object('config.Config')

mongo = PyMongo(app)


@app.route('/student', methods=['GET'])
@cross_origin()
def get_all():
    student = mongo.db.heroku_v7l9xvr5
    output = []
    for s in student.find():
        output.append(Student.jsonify(s))
    return jsonify({'result': output})


@app.route('/student/<anonymous_id>', methods=['GET'])
@cross_origin()
def get_one(anonymous_id):
    student = mongo.db.heroku_v7l9xvr5
    s = student.find_one({'anonymous_id': anonymous_id})
    if s:
        return jsonify({'result': Student.jsonify(s)})
    return jsonify({'result': "No such anonymous_id"})


@app.route('/student', methods=['POST'])
@cross_origin()
def add():
    student = mongo.db.heroku_v7l9xvr5
    data = Student.jsonify(request.json)
    student_id = student.insert(data)

    new_student = student.find_one({'_id': student_id })
    return jsonify({'result': Student.jsonify(new_student)})


@app.route('/student/<anonymous_id>', methods=['PATCH'])
@cross_origin()
def update(anonymous_id):
    student = mongo.db.heroku_v7l9xvr5
    data = Student.jsonify(request.json)
    s = student.update({"anonymous_id": anonymous_id}, data)
    print(s)
    if s:
        return jsonify({'result': s})
    return jsonify({'result': 'Error'})


if __name__ == '__main__':
    app.run(debug=False)
