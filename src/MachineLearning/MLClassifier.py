#!/usr/bin/env python
# coding: utf-8

# In[1]:


from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding
#util.path.append('/home/bonita/.env/lib/python3.6/site-packages/spacy')
import json
import csv
import os
import pandas as pd

TAG_MAP = {}

TRAIN_DATA = []


def classify_each_file(nlp, file):
    new_filename = file.name[0:-4]+"Classified"+".csv"
    column_tags =[]

    df = pd.read_csv(file)
    columns = list(df.head(0)) 
    column = ""
    for columnHeader in columns:
        column += str(columnHeader)
        column = column.upper()
        list_of_items = df[0:5][columnHeader]
        for item in list_of_items:
            column += " "+str(item)
        doc = nlp(column)
        column = ""
        #print('Tags', [(t.text, t.tag_, t.pos_) for t in doc])
        print('Tag', doc[0].text, doc[0].tag_)
        column_tags.append(doc[0].tag_)
        
    #write in new row 
    reader = csv.reader(file)
    with open("/Flash/"+new_filename, 'w') as updated_file:
        writer = csv.writer(updated_file)
        writer.writerow(column_tags)
        for row in reader:
            writer.writerow(row)


def run_on_files(nlp, file_list):
    for curr_file in file_list:
        classify_each_file(nlp,curr_file)



@plac.annotations(
    lang=("ISO Code of language to use", "option", "l", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int))

def main(file_list, lang='en', output_dir=None, n_iter=25):
    """Create a new model, set up the pipeline and train the tagger. In order to
    train the tagger with a custom tag map, we're creating a new Language
    instance with a custom vocab.
    """
    nlp = spacy.blank(lang)
    # add the tagger to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    tagger = nlp.create_pipe('tagger')
    # Add the tags. This needs to be done before you start training.

    
    #Open file to get tag map
    tag_map_file = open("/Flash/tag_map.json")
    tag_map = json.load(tag_map_file)
    TAG_MAP = tag_map
    
    #Open file to get training data 
    training_data_file = open("/Flash/curr_training_data.json")
    training_data = json.load(training_data_file)
    for key, value in training_data.items():
        temp = [key,value]
        TRAIN_DATA.append(temp)
    #TRAIN_DATA = training_data
    
    #reads in tags 
    for tag, values in TAG_MAP.items():
        tagger.add_label(tag, values)
    nlp.add_pipe(tagger)

    #trains the model 
    optimizer = nlp.begin_training()
    for i in range(n_iter):
        random.shuffle(TRAIN_DATA)
        losses = {}
        # batch up the examples using spaCy's minibatch
        batches = minibatch(TRAIN_DATA, size=compounding(4., 32., 1.001))
        for batch in batches:
            texts, annotations = zip(*batch)
            nlp.update(texts, annotations, sgd=optimizer, losses=losses)
        #print('Losses', losses)

    run_on_files(nlp, file_list)

    #input_csv_dir = "./inputData/"
    #output_csv_dir = "./MLOutputData/"
    #read and tag all column headers in cvs given_csv
    #i = 0
    #for filename in os.listdir(input_csv_dir):
        #i+=1
    
    # save model to output directory
    # if output_dir is not None:
    #     print("saving")
    #     output_dir = Path(output_dir)
    #     if not output_dir.exists():
    #         output_dir.mkdir()
    #     nlp.to_disk(output_dir)
    #     print("Saved model to", output_dir)
    #
    #     # test the save model
    #     print("Loading from", output_dir)
    #     nlp2 = spacy.load(output_dir)


if __name__ == '__main__':
    main()

