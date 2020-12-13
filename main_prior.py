import csv
import sys
import os
import matplotlib.pyplot as plt

from prior_plsa import Corpus, Pipeline, Visualize
from prior_plsa.pipeline import DEFAULT_PIPELINE
from prior_plsa.algorithms import PriorPLSA

# Directory that contains the corpus data
directory = 'data'

with open('plsa_new.csv', mode='w') as file:
    fieldnames = ['date', 'topic', 'probability']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()

    for subdir, dirs, files in os.walk(directory):
        # We should look for files in directories with format '../CourseProject/data/<month>/<day>'
        directory_name = subdir.split('\\')
        if (len(directory_name) != 3 or int(directory_name[2])>3):
            continue

        filenames = os.listdir(subdir)

        # Pre-processing pipeline
        pipeline = Pipeline(*DEFAULT_PIPELINE)

        # Load corpus
        corpus = Corpus.from_xml(subdir, pipeline, tag='body', max_files=min(10,len(filenames)))

        # Run PriorPLSA
        n_topics = 3
        prior_plsa = PriorPLSA(corpus, n_topics, True)

        # Fit a PLSA model
        result = prior_plsa.fit()
        #result = prior_plsa.best_of(5)

        tuples = result.word_given_topic[0][:n_topics]
        date = directory_name[1] + '/' + directory_name[2] + '/00'

        for t in tuples:
            writer.writerow({'date': date, 'topic': t[0], 'probability': t[1]})

        print(result.topic)
        print(subdir)
        print(tuples)

