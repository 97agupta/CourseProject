import csv
import os

from plsa import Corpus, Pipeline, Visualize
from plsa.pipeline import DEFAULT_PIPELINE
from plsa.algorithms import PLSA


# Directory that contains the corpus data
def plsa_without_prior_run():
    directory = 'data'

    with open('plsa_without_prior.csv', mode='w') as file:
        fieldnames = ['date', 'topic', 'probability']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for subdir, dirs, files in os.walk(directory):
            # We should look for files in directories with format '../CourseProject/data/<month>/<day>'
            directory_name = subdir.split('/')
            print(directory_name)
            if len(directory_name) != 3:
                continue

            filenames = os.listdir(subdir)

            # Pre-processing pipeline
            pipeline = Pipeline(*DEFAULT_PIPELINE)

            # Load corpus
            # Add max_files=min(10, len(filenames)) to limit number of files read
            corpus = Corpus.from_xml(subdir, pipeline, tag='body', max_files=min(10, len(filenames)))

            # Run PLSA
            n_topics = 5
            plsa = PLSA(corpus, n_topics, True)

            # Fit a PLSA model
            # result = plsa.fit()
            result = plsa.best_of(5)

            tuples = result.word_given_topic[0][:n_topics]
            date = directory_name[1] + '/' + directory_name[2] + '/00'

            for t in tuples:
                writer.writerow({'date': date, 'topic': t[0], 'probability': t[1]})

            print(result.topic)
            print(subdir)
            print(tuples)

