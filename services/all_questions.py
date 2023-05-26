from flask import request ,jsonify, Blueprint
from utils.db import get_collection 

all_question_routes = Blueprint('all_question_routes',__name__)

@all_question_routes.route('/all_question',methods=['GET'])
def all_questions():
    questions = get_collection('questions')
    data = questions.find({},{"_id":0})
    _data = []
    for d in data:
        _data.append(d)

    return jsonify({"questions": list(_data)})