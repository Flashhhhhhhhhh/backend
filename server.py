from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from flask import request
from csvToJson import readFile
import werkzeug

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
      f = request.files['file']
      csv_data_array = request.form['file']
      csv_file = csv_data_array[0]
      convertedFile = readFile(csv_file)
      return convertedFile, 200

api.add_resource(TestData, "/test/<string:name>")
api.add_resource(FileUpload, "/upload")
app.run(debug=True,host='0.0.0.0',port=5001)
