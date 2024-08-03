from flask import Flask, send_from_directory, request, jsonify, abort
import json
import os
import time
import string
import random
from datetime import datetime

app = Flask(__name__)

LEVELS_FOLDER = 'levels'
OFFICIAL_LEVELS_FOLDER = 'officiallevels'
IMAGES_FOLDER = 'images'


os.makedirs(LEVELS_FOLDER, exist_ok=True)
os.makedirs(OFFICIAL_LEVELS_FOLDER, exist_ok=True)
os.makedirs(IMAGES_FOLDER, exist_ok=True)


# Launch_Date = datetime(2024, 10, 1) # october 1
Launch_Date = datetime(2024, 8, 1) #temp for test

@app.route('/')
def hello_world():
    return send_from_directory("public", "index.html")

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory("public", path)

#get numericalid of today's level
@app.route('/leveltodayid', methods=['GET'])
def leveltodayid():
    today = datetime.now()
    levelnum = (today - Launch_Date).days + 1
    return str(levelnum)

@app.route('/getofficiallevel/<level_id>', methods=['GET'])
def getofficiallevel(level_id):
    today = datetime.now()
    maxlevelnum = (today - Launch_Date).days + 1
    levelidint = int(level_id)
    if levelidint > maxlevelnum or levelidint < 1:
        return "access denied", 403
    else:
        filename = f"{level_id}.json"
        filepath = os.path.join(OFFICIAL_LEVELS_FOLDER, filename)
        return send_from_directory(OFFICIAL_LEVELS_FOLDER, filename)

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
        filepath = os.path.join(LEVELS_FOLDER, filename)
        file.save(filepath)
        return jsonify({"message": f"Level uploaded successfully. ID: {level_id}", "filename": filename}), 200

@app.route('/get_level/<level_id>', methods=['GET'])
def get_level(level_id):
    filename = f"{level_id}.json"
    filepath = os.path.join(LEVELS_FOLDER, filename)
    if os.path.exists(filepath):
        return send_from_directory(LEVELS_FOLDER, filename)
    else:
        return jsonify({"error": "Level not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6942, debug=True)
