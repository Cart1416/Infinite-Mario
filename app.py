from flask import Flask, send_from_directory, request, jsonify, abort
import json
import os
import time
import string
import random

app = Flask(__name__)

UPLOAD_FOLDER = 'levels'

@app.route('/')
def hello_world():
    return send_from_directory("public", "index.html")

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory("public", path)

@app.route('/upload', methods=['POST'])
def upload_level():
    if 'file' not in request.files:
        return jsonify({"error": "No file part", "message": "Error"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file", "message": "Error"}), 400
    if file:
        level_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        filename = f"{level_id}.json"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return jsonify({"message": f"Level uploaded successfully. ID: {level_id}", "filename": filename}), 200

@app.route('/get_level/<level_id>', methods=['GET'])
def get_level(level_id):
    filename = f"{level_id}.json"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        return send_from_directory(UPLOAD_FOLDER, filename)
    else:
        return jsonify({"error": "Level not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6942, debug=True)
