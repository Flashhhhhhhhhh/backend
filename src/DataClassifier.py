#!/usr/bin/python

from flask import jsonify
from src.CsvFileHandler import CsvInterpreter
from src.MachineLearning import OntologyToTagMapGenerator, TrainingDataGenerator, MLClassifier
from json import load

def classify_data(csv_file):
    # ML components
    OntologyToTagMapGenerator.create_tag_map()
    TrainingDataGenerator.create_training_data()
    MLClassifier.classify_files([csv_file])

    CsvInterpreter.get_headers(csv_file.name + "Classified.csv")
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

