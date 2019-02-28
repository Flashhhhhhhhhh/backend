import json
from pprint import pprint

data= {}
data[''] = [] 

with open('ontology.json') as f:
    loaded_json = json.load(f)


with open('tag_map.json','w') as f:
      f.write("{\n")
      for header in loaded_json:

         line = '\t"'+header.upper()+'" : {"pos": "X"},\n'
         f.write(line)
      line = '\t"UNKNOWN": {"pos": "X"},\n'
      f.write(line)
      line = '\t"NUMBER": {"pos": "NUM"},\n'
      f.write(line)
      line = '\t"PROPERNOUN": {"pos": "PRON"},\n'
      f.write(line)
      #LAST LINE NO COMMA
      line = '\t"N": {"pos": "NOUN"}\n'
      f.write(line)
      f.write("}")

