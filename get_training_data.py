import json
import os
from pprint import pprint



def make_training_data(tag_map,training_data,curr_training_data):
   #opens onotology
   with open(tag_map) as f:
      loaded_onotology = json.load(f)
   #opens all training data
   with open(training_data) as f:
      training_data_read = json.load(f)
   #creates file to add relevant training data
   with open(curr_training_data,'w') as training_data_write:
      training_data_write.write("{\n");
      for header in loaded_onotology:
         header = header.upper();
         if header in training_data_read: #looks for only training data from current headers
            data_dump = json.dumps(training_data_read[header])
            data_dump = data_dump[1:-1]
            training_data_write.write(data_dump+",\n")
      training_data_write.seek(training_data_write.tell() - 2, os.SEEK_SET)
      training_data_write.write('')
      training_data_write.write("\n}");


def main():
   #needs path to directory in S3 called "MLfiles" 
   tag_map_dir = './MLfiles/tag_map.json'  
   #needs path to directory in S3 called "MLfiles" 
   training_data_dir = './MLfiles/training_data.json'
   #needs path to directory in S3 called "MLfiles" 
   curr_training_data_dir = './MLfiles/curr_training_data.json'

   make_training_data(tag_map_dir,training_data_dir,curr_training_data_dir)


if __name__ == "__main__":
   main()






