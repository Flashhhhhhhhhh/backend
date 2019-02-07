#!/usr/bin/python3

import pandas as pd

def get_headers(csv):
    header_list = parse_file(csv)
    json = generate_json(header_list)
    return json

def parse_file(csv):
    data_frame = pd.read_csv(csv)
    header_list = []
    column_headers = list(data_frame.head(0))

    for header in column_headers:
        example_list = []
        for ex in data_frame[0:10][header]:
            example_list.append(Example(ex, csv))
        header_temp = Header(header, csv, example_list)
        header_list.append(header_temp)

    return header_list

def generate_json(header_list):
    with open('headers.json', 'w') as json:
        isLast = len(header_list) - 1
        json.write("{");
        line = ""
        for header in header_list:
            line += header.print_header()
            if isLast == 0:
                json.write(line)
            line += ","
            isLast -= 1
        json.write("}")

class Header:
    def __init__(self, name, from_csv, examples):
        self.name = name
        self.from_csv = from_csv
        self.examples = examples

    def print_header(self):
        start = '"%s":{' %(self.name)
        examples_list = '"examples":['

        for ex in  self.examples:
            examples_list += '%s,' %(ex.print_example())
        examples_list += 'null],"tag":[null]}'
        return start + examples_list

class Example:
    def __init__(self, name, source):
        self.name = name
        self.source = source

    def print_example(self):
        return '{"value":"%s","source":"%s"}' %(self.name, self.source)

