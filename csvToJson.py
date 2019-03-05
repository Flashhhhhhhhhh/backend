#!/usr/bin/python

import csv
import json
import pandas as pd

combined_headers = []

class CsvInfo:                                     #Object that holds the filename(lineage?) and 10 examples for a given header 
   def __init__(self, file_name):
      self.file_name = file_name
      self.examples = []    

   def add_example(self, example):
      self.examples.append(example)


class Header:                                     #Object to represent a column header incldudes header name, list of cvs that included this header, and a tag 

   def __init__(self, name):
      self.name = name
      self.csv_files = []
      self.tag = []


   def add_csv_file(self, csv_file):              #adds a csv file that includes this header 
      self.csv_files.append(csv_file)

   def print_header(self):                        #IN PROGRESS prints this header in json format 
      start = '   "%s": {\n'%(self.name)
      examples_line = "   "
      for file in self.csv_files:                  #this will only be one on the first round 
         file_name_line = '      "%s":' %(file.file_name)
         examples_line = examples_line + "["
         for examples in file.examples:
            example_string = '"%s", ' %(examples)
            examples_line = examples_line + example_string
         examples_line = examples_line + "null],\n"
         full_file_info = file_name_line + examples_line
      tag = '      "tag": [null],\n'
      end = "   }"
      final_line = start +full_file_info+ tag + end
      return final_line

def readFile(csv_file_path):                            #meant to take in a cvs path (using a temp currently) in order to read all column headers and include first 10 examples from each
   df = pd.read_csv(csv_file_path)
   columns = list(df.head(0))                          #gets list of all coloumn headers 
   for columnHeader in columns:                        #goes through each column header in csv   
         columnHeader_temp = Header(columnHeader)      #creates a header object for each column in csv 
         #print(columnHeader);
         item_in_c = df[0:10][columnHeader]            #array of first 10 examples in column 
         csv_temp = CsvInfo(csv_file_path) 
         for item in item_in_c:                        #for each of ten examples add them to that csv file info object 
            csv_temp.add_example(item) 
            #print(item);
         columnHeader_temp.add_csv_file(csv_temp);     #add csv examples to header object 
         combined_headers.append(columnHeader_temp) #add header object to global group of headers 

def main():
   readFile('dataTemp.csv') 
   #readFile('dataTemp2.csv')
   with open('temp.json', 'w') as f:
      f.write("{\n")
      header_num =0
      while header_num < len(combined_headers):
         header = combined_headers[header_num]
         line = header.print_header()
         if header_num != len(combined_headers) - 1:
            line = line + ","
            f.write(line + "\n")
         header_num+=1
      f.write("}")

if __name__ == '__main__':
    main()
