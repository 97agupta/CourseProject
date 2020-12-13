import csv
import os
import numpy as np

from prior_plsa import Corpus, Pipeline
from prior_plsa.pipeline import DEFAULT_PIPELINE
from prior_plsa.algorithms import PriorPLSA

from numpy import ndarray

def plsa_with_prior_run():
    # Directory that contains the corpus data
    directory = 'data'

    with open('plsa_with_prior.csv', mode='w') as file:
        fieldnames = ['date', 'topic', 'probability']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for subdir, dirs, files in os.walk(directory):
            # We should look for files in directories with format '../CourseProject/data/<month>/<day>'
            directory_name = subdir.split('\\')
            if len(directory_name) != 3:
                continue

            filenames = os.listdir(subdir)

            # Pre-processing pipeline
            pipeline = Pipeline(*DEFAULT_PIPELINE)

            # Load corpus
            # Add max_files=min(10, len(filenames)) to limit number of files read
            corpus = Corpus.from_xml(subdir, pipeline, tag='body', max_files=min(10, len(filenames)))

            # Run PriorPLSA
            n_topics = 5

            prior: ndarray = load_priors(n_topics, corpus)

            prior_plsa = PriorPLSA(corpus, n_topics, True, mu=30, prior_topic=prior)

            # Fit a PLSA model
            # result = prior_plsa.fit()
            result = prior_plsa.best_of(5)

            tuples = result.word_given_topic[0][:n_topics]
            date = directory_name[1] + '/' + directory_name[2] + '/00'

            for t in tuples:
                writer.writerow({'date': date, 'topic': t[0], 'probability': t[1]})

            print(result.topic)
            print(subdir)
            print(tuples)

def load_priors(n_topics: int, corpus: Corpus) -> ndarray:
    prior: ndarray = np.zeros((n_topics, corpus.n_words))
    prev_topic: str = None
    topic_id: int = -1

    with open('prior_csvs\\combined_priors.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader) # skip header

        for row in csv_reader:
            topic = row[3]
            if prev_topic != topic:
                prev_topic = topic
                topic_id += 1

            word = row[1]
            probability = row[2]
            if word in corpus.index:
                wordIndex = corpus.index[word]
                prior[topic_id][wordIndex] = float(probability)

    #print(prior)

# plsa_with_prior_run()