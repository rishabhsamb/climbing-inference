from flask import Flask, request, jsonify
import pickle
from numpy import array
import os

file = open('dumped-pipeline.pkl', 'rb')
clf = pickle.load(file)
file.close()
app = Flask(__name__)

@app.route("/predict")
def predict():
    try:
        difference = request.json['difference']
        gender = request.json['gender']
        height = request.json['height']
        weight = request.json['weight']
        data = array([[difference, gender, height, weight]])
        grade = clf.predict(data)
        return jsonify({"grade": grade[0]}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)