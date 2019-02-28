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
import pandas as pd


# In[2]:


TAG_MAP = {}


# In[3]:


TRAIN_DATA = [
    ("ID 25665 7845 218 789 12546 4856", {'tags': ['ID', 'NUMBER','NUMBER','NUMBER', 'NUMBER','NUMBER','NUMBER']}),
    ("ID Bob Phil James George Jorge Patty", {'tags': ['NAME', 'PROPERNOUN', 'PROPERNOUN','PROPERNOUN', 'PROPERNOUN','PROPERNOUN','PROPERNOUN']}),
    ("SEX male female m f Male Female M F", {'tags': ['GENDER','N','N','N','N', 'N','N','N','N']}),
    ("GENDER male female m f Male Female M F", {'tags': ['GENDER','N','N','N','N', 'N','N','N','N']}), 
    ("AGE", {'tags': ['AGE']}),
    ("DOB", {'tags': ['DOB']}),
    ("SDJFKHSAK Jill John Kate", {'tags': ['UNKNOWN', 'PROPERNOUN','PROPERNOUN','PROPERNOUN']}),
    ("DFSAD", {'tags': ['UNKNOWN']}),
    ("AWY 8 9.6 0.8", {'tags': ['UNKNOWN','NUMBER','NUMBER','NUMBER']}),
    ("ICQ", {'tags': ['UNKNOWN']}),
    ("1 29 576 .98 1.3 34.5 345.123", {'tags': ['NUMBER','NUMBER','NUMBER','NUMBER','NUMBER','NUMBER','NUMBER']}),
    ("MARRIED married single Yes No", {'tags': ['MARRIED',  'MARRIED','N','N','N']}),
    ("married married single yes no", {'tags': ['MARRIED',  'MARRIED','N','N','N']})
]


# In[4]:


@plac.annotations(
    lang=("ISO Code of language to use", "option", "l", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int))


def main(lang='en', output_dir=None, n_iter=25):
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
    tag_map_file = open("tag_map.json")
    tag_map = json.load(tag_map_file)
    TAG_MAP = tag_map
    
    
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
    
    
    #read and tag all column headers in cvs given_csv
    print("csv1")
    column_tags =[]
    df = pd.read_csv("dataTemp1.csv")
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
    with open("dataTemp1.csv",'rb') as old_file:
        reader = csv.reader(old_file)
        with open('tempWrite1.csv', mode='wb') as updated_file:
            writer = csv.writer(updated_file)
            writer.writerow(column_tags)
            writer.writerows(reader)
                 
    
    
    # save model to output directory
    if output_dir is not None:
        print("saving")
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the save model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)


# In[5]:


if __name__ == '__main__':
    main()

