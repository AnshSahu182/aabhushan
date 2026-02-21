from flask import Blueprint, jsonify, request
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
from datetime import datetime

load_dotenv()

client = MongoClient(os.getenv('MONGO_URI'))
db = client['aabhushan']
metal_rate = db['metal_rate']
jewellery = db['jewellery']

calculate_bp = Blueprint('calculate', __name__)

@calculate_bp.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    name = data.get('name')
    gram = data.get('gram')
    making_percent = data.get('making_percent')
    metal = data.get('metal')

    if not all([name, metal, gram, making_percent]):

        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        rate = float(metal_rate.find_one({"_id": ObjectId(metal)})['price'])
        gram = float(gram)
        making_percent = float(making_percent)

        price = rate * gram
        total_cost = price * (1 + making_percent / 100)

        jewellery.insert_one({
            'name': name,
            'price': price,
            'gram': gram,
            'making_percent': making_percent,
            'total_cost': total_cost,
            'metal': ObjectId(metal),
            'created_at': datetime.utcnow() 
        })

        return jsonify({'name': name, 'price': price, 'total_cost': total_cost})
    
    except ValueError:
        return jsonify({'error': 'Invalid input. Price, gram, and making_percent must be numbers.'}), 400

@calculate_bp.route('/calculations', methods=['GET'])
def get_calculations():
    calculations = list(jewellery.find({}, {"_id": 0}))
    return jsonify(calculations), 200
