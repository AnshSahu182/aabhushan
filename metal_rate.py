from flask import Blueprint, jsonify, request
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = MongoClient(os.getenv('MONGO_URI'))
db = client['aabhushan']
metal_rate = db['metal_rate']

rate_bp = Blueprint('rate', __name__)

@rate_bp.route('/rate', methods=['PUT','POST'])
def insert_rate():

    data = request.get_json()
    rates = data.get("rates")

    if not rates or not isinstance(rates, list):
        return jsonify({"error": "Rates must be provided as a list"}), 400

    try:
        for item in rates:
            name = item.get("name")
            price = item.get("price")

            if not name or price is None:
                return jsonify({"error": f"Missing fields in item: {item}"}), 400

            price = float(price)

            metal_rate.update_one(
                {"name": name},
                {
                    "$set": {
                        "price": price,
                        "updated_at": datetime.utcnow()
                    }
                },
                upsert=True  # Insert if not exists, update if exists
            )

        return jsonify({"message": "All metal rates saved successfully"}), 200

    except ValueError:
        return jsonify({"error": "Invalid input. Price must be a number."}), 400
    

@rate_bp.route('/rate', methods=['GET'])
def get_rates():
    rates = list(metal_rate.find({}, {"_id": 0}))  # Exclude _id field
    return jsonify(rates), 200