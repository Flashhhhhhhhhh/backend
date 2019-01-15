#!/usr/bin/python

import csv
import json

csvFilePath = "data.csv"
jsonFilePath = "happy.json"

# Read the CSV and add the data to a dictionary...
data = {}
with open(csvFilePath) as csvFile:
   csvReader = csv.DictReader(csvFile)
   for csvRow in csvReader:
      id = csvRow["id"]
      data[id] = csvRow

#print(data)
# Add data to a root node...
root = {}
root["id"] = data

# Write data to a JSON file

with open(jsonFilePath, "w") as jsonFile:
   jsonFile.write(json.dumps(root, indent=4))
