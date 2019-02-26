#!/usr/bin/python3

import json


def move(tag):
   #print tag
   for field in tag:
      if field == 'dest':
         dest = tag[field]
      elif field == 'src':
         src = tag[field]
   print "(\""+src+"\", {\'tags\': [\'"+dest+"\']})"


def parseChange(change):
   #print change
   for tag in change:
      if tag != None:
         if tag == 'move':
            move(change[tag])
         #else:
         #   print 'no such tag'
         #   print tag
   #print change['tag']


def main():
  changeFile = open("headers.json")
  tagMap = open("tagMap.json")
  changes = json.load(changeFile)
  #tags = json.load(tagMap)
  for obj in changes:
     parseChange(changes[obj]['tag'])



if __name__ == "__main__":
   main()
