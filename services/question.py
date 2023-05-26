from flask import request ,jsonify, Blueprint
from utils.db import get_collection 
import numpy as np
from io import BytesIO
import cv2
import pytesseract
import os
import uuid

question_routes = Blueprint('question_routes',__name__)

@question_routes.route('/new_question',methods=['POST'])
def new_question():
    question = request.form['question']
    tag = request.form['tag']
    filename = ""
    ocr_text = ""
    if 'image' in request.files:
        image_file = request.files['image']
        filename = str(uuid.uuid4())
        image_file.save(os.path.join('uploads', filename))

        image_data = image_file.read()

        img_stream = BytesIO(image_data)
        img_array = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        # Perform OCR using pytesseract
        ocr_text = pytesseract.image_to_string(img)

    file_url = ":5000/client/file/" + filename
    data = {
        "question_id":str(uuid.uuid4()),
        "question":question,
        "ocr_text":ocr_text,
        "tag":tag,
        "filename":file_url
    }
    questions = get_collection("questions")
    questions.insert_one(data)

    return jsonify({'message': 'new question added',
                    'question':question,
                    'ocr_data':ocr_text})

@question_routes.route('/frequency',methods=['GET'])
def frequency():
    pipeline = [
        {"$group": {"_id": "$tag", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]

    questions = get_collection('questions')
    tag_frequency = questions.aggregate(pipeline)

    # Print the tag frequency
    data = {}
    for tag in tag_frequency:
        data[tag['_id']] = tag['count']

    return jsonify({"message":data})

@question_routes.route('/search', methods=['POST'])
def search_questions():
    query = request.json.get('query')  # Get the search query parameter

    # Create a regular expression pattern to match the search query
    regex_pattern = {'$regex': query, '$options': 'i'}  # Case-insensitive search

    # Search the 'question' and 'ocr_text' fields using the regex pattern
    query = {'$or': [{'question': regex_pattern}, {'ocr_text': regex_pattern}]}

    # Perform the search query in the MongoDB collection
    results = get_collection('questions').find(query,{"_id":0})

    # Convert the MongoDB cursor to a list of dictionaries
    _questions = []
    for q in results:
        _questions.append(q)

    # Return the search results as JSON
    return jsonify(_questions)