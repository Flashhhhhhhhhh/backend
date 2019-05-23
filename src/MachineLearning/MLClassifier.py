#!/usr/bin/env python
# coding: utf-8

# In[1]:


from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding
import json
import csv
import os
import pandas as pd

TAG_MAP = {}

TRAIN_DATA = []

def classify_each_file(nlp, file):
    new_filename = file.filename[:-4]+"Classified.csv"
    column_tags =[]
    #df = pd.read_csv(file)
    column_tags = make_column_tags(nlp,file)
    file.seek(0)

    with open("/Flash/"+new_filename, 'w') as updated_file:
        writer = csv.writer(updated_file)
        writer.writerow(column_tags)

    with open("/Flash/"+new_filename, 'ab') as append_file:
        for row in file:
            append_file.write(row)

def run_on_files(nlp, file_list):
    for curr_file in file_list:
        print(curr_file.filename)
        classify_each_file(nlp,curr_file)



@plac.annotations(
    lang=("ISO Code of language to use", "option", "l", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int))

def classify_files(file_list, lang='en', output_dir=None, n_iter=25):
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
    # needs path to directory in S3 called "MLfiles"
    tag_map = json.load(tag_map_file)
    TAG_MAP = tag_map

    #Open file to get training data

    training_data_file = open("/Flash/curr_training_data.json")
    training_data = json.load(training_data_file)
    for key, value in training_data.items():
        temp = [key,value]
        TRAIN_DATA.append(temp)

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

    run_on_files(nlp, file_list)

def make_column_tags(nlp,file):
    df = pd.read_csv(file)
    column_tags =[]
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
    return column_tags

