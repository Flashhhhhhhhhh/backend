#!/usr/bin/env python
# coding: utf-8

# In[1]:


from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding


# In[2]:


TAG_MAP = {
    'Gender': {'pos': 'NOUN'},
    'ProperNoun': {'pos': 'PRON'},
    'Number': {'pos': 'NUM'},
    'Name': {'pos': 'Noun'},
    'ID': {'pos': 'Noun'},
    'V': {'pos': 'VERB'},
    'unknown': {'pos': 'X'},
    'J': {'pos': 'ADJ'}
}


# In[3]:


TRAIN_DATA = [
    ("ID 25665 7845 218 789 12546 4856", {'tags': ['ID', 'Number','Number','Number', 'Number','Number','Number']}),
    ("ID 546346 37546 12433 8796 342523 1234123", {'tags': ['ID', 'Number','Number','Number', 'Number','Number','Number']}),
    ("ID bob phil james george jorge patty", {'tags': ['Name', 'ProperNoun', 'ProperNoun','ProperNoun', 'ProperNoun','ProperNoun','ProperNoun']}),
    ("sex I like green eggs bonita", {'tags': ['Gender','V', 'V', 'J', 'V', 'ProperNoun']}),
    ("Eat blue ham", {'tags': ['V', 'J', 'V']})
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
    for tag, values in TAG_MAP.items():
        tagger.add_label(tag, values)
    nlp.add_pipe(tagger)

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

    # test the trained model
    test_text = "ID jack jim veronica jill"
    doc = nlp(test_text)
    print('Tags', [(t.text, t.tag_, t.pos_) for t in doc])
    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the save model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        doc = nlp2(test_text)
        print('Tags', [(t.text, t.tag_, t.pos_) for t in doc])




if __name__ == '__main__':
    main()
