#!/usr/bin/python3

import pandas as pd
import uuid

def get_headers(csv_file):
    column_list = parse_file("../MachineLearning/MLOutputData/" + csv_file)
    json = generate_json(column_list)
    return json

def parse_file(csv_file):
    data_frame = pd.read_csv(csv_file);
    ml_headers = data_frame.columns.tolist();
    csv_headers = data_frame.values.tolist()[0];
    column_list = []

    for i in range(len(csv_headers)):
        example_list = []
        for ex in (data_frame[1:][ml_headers[i]]):
            if (ex not in example_list):
                example_list.append(ex)
        col = Column(ml_headers[i], csv_headers[i], csv_file, example_list)
        column_list.append(col)

    return column_list

def generate_json(column_list):
    file = open('headers.json', 'w')
    with file as json:
        isLast = len(column_list) - 1
        json.write("{");
        line = ""
        for col in column_list:
            line += col.print_header()
            if isLast == 0:
                json.write(line)
            line += ","
            isLast -= 1
        json.write("}")
    file.close()
    return file

class Column:
    def __init__(self, ml_name, csv_name, source, examples):
        self.csv_name = csv_name
        self.source = source
        self.examples = examples
        self.id = uuid.uuid4()

        if "UNKNOWN" in ml_name:
            #print("MAYBE: " + csv_name)
            self.ml_name = "MAYBE: " + csv_name
        else:
            self.ml_name = ml_name

    def print_header(self):
        start = '"%s":{' %(self.ml_name)
        examples_list = ""

        for i in range(min(len(self.examples), 10)):
            examples_list += '"%s":[],' %(self.examples[i])
        examples_list += '"tag":[{ "id":"%s" }]}' %(self.id)
        return start + examples_list