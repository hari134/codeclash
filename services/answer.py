from flask import request ,jsonify, Blueprint
from utils.db import get_collection 

answer_routes = Blueprint('answer_routes',__name__)

@answer_routes.route('/new_answer',methods=['POST'])
def new_answer():
    question_id = request.json.get('question_id')
    answer = request.json.get('answer')
    data = {
        "question_id":question_id,
        "answer":answer
    }
    questions = get_collection("answers")
    questions.insert_one(data)

    return jsonify({'message': 'new answer added'})

@answer_routes.route('/get_answers/<question_id>',methods=['GET'])
def get_answers(question_id):
    answers = get_collection("answers")
    _answers = answers.find({"question_id":question_id},{"_id":0})
    _data = []
    for d in _answers:
        _data.append(d)

    return jsonify({'answers':_data})