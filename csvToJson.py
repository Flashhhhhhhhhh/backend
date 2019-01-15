#!/usr/bin/python

import csv
import json
import pandas as pd

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

# count the variation within each column/category
df = pd.read_csv('data.csv')
list1 = pd.read_csv('data.csv', nrows=1).columns.tolist()
list2 = []
count = 0
for thing in list1:
   for row in df[thing].unique():
      count = count + 1
   list2.append(count)
   count = 0

for thing in list1:
   print(thing)

for num in list2:
   print(num)
