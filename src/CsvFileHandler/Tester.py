#!/usr/bin/python3

from src.CsvFileHandler.CsvInterpreter import *

def main():
   results = get_headers("dataTemp.csv")
   print(results)

if __name__ == '__main__':
   main()
