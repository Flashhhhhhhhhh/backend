#!/usr/bin/python3

import pandas as pd
import uuid

def get_headers(csv_files):
    data_dict = parse_files(csv_files)
    json = generate_json(data_dict)
    return json

def parse_files(csv_files):
    data_dict = {}
    #print(csv_files)
    for csv_file in csv_files:
        print(csv_file)
        data_frame = pd.read_csv("/Flash/" + csv_file.filename.split('.')[0] + "Classified.csv");
        ml_headers = data_frame.columns.tolist();
        csv_headers = data_frame.values.tolist()[0];

        for i in range(len(csv_headers)):
            example_list = []
            for ex in (data_frame[1:][ml_headers[i]]):
                if (ex not in example_list):
                    example_list.append(ex)
            col = Column(ml_headers[i], csv_headers[i], csv_file.filename, example_list)

            key = col.get_name()
            if key in data_dict:
                data_dict[key].append(col)
            else:
                data_dict[key] = [col]

    return data_dict

def generate_json(data_dict):
    file = open('headers.json', 'w')
    with file as json:
        json.write("{");
        isLastKey = len(data_dict.keys()) - 1
        for key in data_dict.keys():
            json.write('"%s":{' %(key))
            col_list = data_dict[key]
            isLastCol = len(col_list) - 1
            line = ""
            for col in col_list:
                line += col.print_examples()
                if isLastCol == 0:
                    json.write(line)
                line += ","
                isLastCol -= 1

            if isLastKey > 0:
               json.write("},")
            else:
               json.write("}")
            isLastKey -= 1

        json.write("}")
    file.close()
    return file

class Column:
    def __init__(self, ml_name, csv_name, source, examples):
        self.csv_name = csv_name
        self.source = source
        self.examples = examples
        self.id = uuid.uuid4()

        self.confidence = "UNKNOWN" if "UNKNOWN" in ml_name else "MAYBE"
        self.ml_name = ml_name if self.confidence == "MAYBE" else csv_name

    def get_name(self):
        return self.ml_name

    def print_column(self):
        if "UNKOWN" in ml_name:
            classified_name = "MAYBE: " + csv_name
        else:
            classified_name = ml_name

        start = '"%s":{' %(classified_name)
        examples_list = ""
        exported_filename = self.source.split('Classified.csv')[0] + ".csv"

        for i in range(min(len(self.examples), 10)):
           examples_list += '"%s":[{"source":"%s", "confidence":"%s"}],' %(self.examples[i], exported_filename, self.confidence)
        examples_list += '"tag":[{ "id":"%s" }]}' %(self.id)
        return start + examples_list

    def print_examples(self):
        examples_list = ""
        #exported_filename = self.source.split('Classified.csv.')[0] + ".csv"
        isLast = len(self.examples) - 1

        for ex in self.examples:
           examples_list += '"%s":[{"source":"%s", "confidence":"%s"}]' %(ex, self.source, self.confidence)
           if isLast > 0:
               examples_list += ','
           isLast -= 1
        return examples_list
