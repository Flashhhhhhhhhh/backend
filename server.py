from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from flask import request, jsonify
from src import DataClassifier
import werkzeug
import json

app = Flask(__name__)
CORS(app)
api = Api(app)

testData = [
   {
      "name" : "Barry Allen",
      "age" : 21,
      "occupation" : "Hosptial Analyst"
   },
   {
      "name" : "test",
      "age" : 55,
      "occupation" : "Thing Doer"
   },
]

class TestData(Resource):
   def get(self, name):
      for datum in testData:
         if (name == datum["name"]):
            return datum, 200
      return "Test data not found", 404

class FileUpload(Resource):
   # sending file to backend from frontend
   def post(self):
      return DataClassifier.classify_data(request.files['data_file'])

class UpdateFinal(Resource):
   # final upload of JSON with tag system
   def post(self):
      f = request.files['data_file'] #request the JSON file
      json_data_array = request.form['file'] # get the file array
      json_file = json_data_array[0] # get the specific JSON file
      convertedFile = json_file
      return convertedFile, 200 # return

api.add_resource(TestData, "/test/<string:name>")
api.add_resource(FileUpload, "/upload")
api.add_resource(UpdateFinal, "/updateFinal")
app.run(debug=True,host='0.0.0.0',port=5000)
