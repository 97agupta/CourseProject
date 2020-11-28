import sys
import os
import matplotlib.pyplot as plt

from plsa import Corpus, Pipeline, Visualize
from plsa.pipeline import DEFAULT_PIPELINE
from plsa.algorithms import PLSA

# Directory that contains the corpus data
directory = '../CourseProject/data/test/'
# if we want to loop through all subdirectories
#for subdir, dirs, files in os.walk(directory):
#    filenames = os.listdir(subdir)


# Pre-processing pipeline
pipeline = Pipeline(*DEFAULT_PIPELINE)
pipeline

# Load corpus
filenames = os.listdir(directory)
corpus = Corpus.from_xml(directory, pipeline, tag='body', max_files=len(filenames))
#corpus

# Run PLSA
n_topics = 5
plsa = PLSA(corpus, n_topics, True)
plsa

# Fit a PLSA model
result = plsa.fit()
result = plsa.best_of(5)

# examine result
#print(result.topic) # relative prevalence of individual topics found
#print(result.word_given_topic) # for individual topics, see how important each word is for the topics

# Visualize the results
visualize = Visualize(result)

# convergence
fig, ax = plt.subplots()
_ = visualize.convergence(ax)
fig.tight_layout()

# relative topic importance
fig, ax = plt.subplots()
_ = visualize.topics(ax)
fig.tight_layout()

# topics
fig = plt.figure(figsize=(9.4, 10))
_ = visualize.wordclouds(fig)
fig.tight_layout()

# topic importance in a doc
fig, ax = plt.subplots()
_ = visualize.topics_in_doc(0, ax)
fig.tight_layout()

plt.show()
