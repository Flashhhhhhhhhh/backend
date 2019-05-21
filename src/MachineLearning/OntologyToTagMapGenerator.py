import json
import os
from pprint import pprint

def create_tag_map(ont_list):
   #needs path to directory in S3 called "inputOntolgy"
   ontology_dir = '/Flash/inputOntology'
   #needs path to directory in S3 called "MLfiles"
   tag_map_dir = '/Flash/tag_map.json'

   #print("tag_map")
   #print(ont_list)   

   if not ont_list:
      for filename in os.listdir(ontology_dir):
         with open((ontology_dir+"/"+filename)) as ont_tag_map:
            loaded_json = json.load(ont_tag_map)
         make_tag_map(loaded_json, tag_map_dir)
   else: 
      j = json.load(ont_list)
      make_tag_map(j,tag_map_dir)

def make_tag_map(loaded_json,output_dir):
   #with open(ont_path) as ont_tag_map:
      #loaded_json = json.load(ont_tag_map)
   #print(loaded_json)
   with open(output_dir,'w') as tag_map:
      tag_map.write("{\n")
      for header in loaded_json:
         line = '\t"'+header.upper()+'" : {"pos": "X"},\n'
         tag_map.write(line)
      line = '\t"UNKNOWN": {"pos": "X"},\n'
      tag_map.write(line)
      line = '\t"NUMBER": {"pos": "NUM"},\n'
      tag_map.write(line)
      line = '\t"PROPERNOUN": {"pos": "PRON"},\n'
      tag_map.write(line)
      #LAST LINE NO COMMA
      line = '\t"N": {"pos": "NOUN"}\n'
      tag_map.write(line)
      tag_map.write("}")







