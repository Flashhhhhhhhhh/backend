#!/usr/bin/python3

import json


def move(tag):
   for field in tag:
      if field == 'dest':
         dest = tag[field]
      elif field == 'src':
         src = tag[field]
   print "(\""+src+"\", {\'tags\': [\'"+dest+"\']})"


def parseChange(change):
   for tag in change:
      if tag != None:
         if tag == 'move':
            move(change[tag])

def openFiles():
   # use myHeaders.json since headers.json has no tags for now
  changeFile = open("myHeaders.json")
  tagMap = open("tagMap.json")
  changes = json.load(changeFile)

  for obj in changes:
     parseChange(changes[obj]['tag'])

def main():
   openFiles()

if __name__ == "__main__":
   main()
