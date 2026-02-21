from flask import Flask,jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from pymongo import MongoClient
import os
load_dotenv()

app = Flask(__name__)
CORS(app)
client = MongoClient(os.getenv('MONGO_URI'))

from calculate import calculate_bp
from metal_rate import rate_bp  

app.register_blueprint(calculate_bp, url_prefix='/api')
app.register_blueprint(rate_bp, url_prefix='/api')

@app.route("/health", methods=["GET"])
def health_check():
    try:
        # simple MongoDB ping
        client.admin.command("ping")

        return jsonify({
            "status": "ok",
            "app": "running",
            "database": "connected"
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "app": "running",
            "database": "disconnected",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=3000)

