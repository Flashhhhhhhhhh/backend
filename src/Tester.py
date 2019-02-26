#!/usr/bin/python3

from CsvInterpreter import *

def main():
   results = get_headers("dataTemp.csv")
   print(results)

if __name__ == '__main__':
   main()
