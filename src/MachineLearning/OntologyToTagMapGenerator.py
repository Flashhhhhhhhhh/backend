import json
import os
from pprint import pprint

def create_tag_map():
   #needs path to directory in S3 called "inputOntolgy"
   ontology_dir = './inputOntology'
   #needs path to directory in S3 called "MLfiles"
   tag_map_dir = './MLfiles/tag_map.json'
   for filename in os.listdir(ontology_dir):
      make_tag_map((ontology_dir+"/"+filename), tag_map_dir)


def make_tag_map(filename,output_dir):
   with open(filename) as tag_map:
      loaded_json = json.load(tag_map)
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







