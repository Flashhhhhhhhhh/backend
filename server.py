from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

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

api.add_resource(TestData, "/test/<string:name>")
app.run(debug=True,host='0.0.0.0')
