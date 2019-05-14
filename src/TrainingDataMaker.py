#!/usr/bin/python3

import json

class TrainingDataMaker:
   def appendMove(out_json, move):
      tag_string = "{\"tags\": [\"" + move[0] + "\"]}"
      tag_json = json.loads(tag_string)
      out_json[move[1]][move[0]] = tag_json
      return out_json

   def getMove(tag):
      for field in tag:
         if field == 'dest':
            dest = tag[field]
         elif field == 'src':
            src = tag[field]
      return (src.upper(), dest.upper())

   def makeTrainingData(in_file):
      changeFile = open(in_file)
      out = open(backend/MLFiles/training_data.json)
      changes = json.load(changeFile)
      training = json.load(out)

      for obj in changes:
         for tag in changes[obj]['tag']:
            if tag != None and tag == 'move':
               move = getMove(changes[obj]['tag'][tag])
               training = appendMove(training, move)
      out.close()
      out = open(out_file, 'w')
      json.dump(training, out)

#def main():
#   makeTrainingData("myHeaders.json", "my_training_data.json")
#
#if __name__ == "__main__":
#   main()
