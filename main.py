import csv
import sys
import os
import matplotlib.pyplot as plt

from plsa import Corpus, Pipeline, Visualize
from plsa.pipeline import DEFAULT_PIPELINE
from plsa.algorithms import PLSA

# Directory that contains the corpus data
directory = '../CourseProject/data/'

with open('plsa.csv', mode='w') as file:
    fieldnames = ['date', 'topic', 'probability']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    for subdir, dirs, files in os.walk(directory):
        # We should look for files in directories with format '../CourseProject/data/<month>/<day>'
        directory_name = subdir.split('/')
        if (len(directory_name) != 5):
            continue

        filenames = os.listdir(subdir)

        # Pre-processing pipeline
        pipeline = Pipeline(*DEFAULT_PIPELINE)

        # Load corpus
        corpus = Corpus.from_xml(subdir, pipeline, tag='body', max_files=len(filenames))

        # Run PLSA
        n_topics = 5
        plsa = PLSA(corpus, n_topics, True)

        # Fit a PLSA model
        result = plsa.fit()
        result = plsa.best_of(5)

        first_tuple = result.word_given_topic[0][:1]
        date = directory_name[3] + '/' + directory_name[4] + '/00'

        writer.writerow({'date': date, 'topic': first_tuple[0][0], 'probability': first_tuple[0][1]})

        print(subdir)
        print(result.word_given_topic[0][:1])

