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
    data = {
        "question_id":str(uuid.uuid4()),
        "question":question,
        "ocr_text":ocr_text,
        "tag":tag,
        "fileanem":filename
    }
    questions = get_collection("questions")
    questions.insert_one(data)

    return jsonify({'message': 'new question added',
                    'question':question,
                    'ocr_data':ocr_text})