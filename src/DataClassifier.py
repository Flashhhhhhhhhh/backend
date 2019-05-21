#!/usr/bin/python

from flask import jsonify
from src.CsvFileHandler import CsvInterpreter
from src.MachineLearning import OntologyToTagMapGenerator, TrainingDataGenerator, MLClassifier
from json import load

def classify_data(csv_file_list, ont_list):
    # ML components
    OntologyToTagMapGenerator.create_tag_map(ont_list)
    TrainingDataGenerator.create_training_data()
    MLClassifier.classify_files(csv_file_list)
    
    #CSVINTERP  NEEDS TO BE FIXED TO HANDLE MORE THAN ONE FILE 
    file1 = csv_file_list[0]

    CsvInterpreter.get_headers(file1.filename.split('.')[0] + "Classified.csv")
    headers = load(open("headers.json", "r"))
    return jsonify(headers)

    #def update_model(self, json):
        # Read tags and update model
        #
        # Tags:
        #  combine(h1, h2, h_new)
        #  create(hnew)
        #  move(h_old, h_new)
        #  remove(h)
        #  sensitive(h)

    #def visualize_date(self json):
        # Input data into newly structured header model

