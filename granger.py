import pandas as pd
import word_retriever
import operator
import math

from scipy.stats import pearsonr
from statsmodels.tsa.stattools import grangercausalitytests


def granger_run(plsa_file, df_all_normalized):

    min_probability = 1.0
    df_plsa = pd.read_csv(plsa_file, error_bad_lines=False)
    # df_plsa = df_plsa.drop(df_plsa.columns[3], axis=1)
    # df_plsa = df_plsa.drop(df_plsa.columns[3], axis=1)

    # We find all unique topics and adds each topic as a key to a dictionary: df_topics_collection.
    # The value for each key in this topic is a dataframe containing the dates and probabilities for that topic/
    topics = df_plsa.topic.unique()
    df_topics_collection = {}
    for topic in topics:
        df_topics_collection[topic] = df_plsa.loc[df_plsa['topic'] == topic]

    # This method iterates through each topic and creates stationary time series for the probabilities
    # And the stock data. This is then used in a granger test, who's results are manually inspected to find
    # Relevent topics. These topics are added to a dictionary, relevent_topic
    relevent_topic = {}
    for topic in topics:
        df = df_topics_collection[topic]
        df = df.rename(columns={"date": "Date"})
        df = pd.merge(df, df_all_normalized, on="Date")
        temp_df = df.loc[(df['Contract'] == 'Dem')]
        temp_df['Probablity_stationary'] = temp_df['probability'] - temp_df['probability'].shift(1)
        temp_df['NormalizedPrice_stationary'] = temp_df['NormalizedPrice'] - temp_df['NormalizedPrice'].shift(1)
        temp_df = temp_df.dropna()
        try:
            res = grangercausalitytests(temp_df[['Probablity_stationary', 'NormalizedPrice_stationary']], maxlag=5)
            relevent_topic[topic] = res
            print(res)
        except:
            continue

    # We find relevant words for each topic, and create a new CSV 'words_per_topic.csv'.
    # We also create a new CSV 'word_frequency.csv' with each word and its frequency throughout each day's files.
    # These files are loaded into a data frame.
    word_retriever.retrieve_words_per_topic_and_frequency('plsa_without_prior.csv')
    df_word_per_topic = pd.read_csv('words_per_topic.csv', error_bad_lines=False, header=None)
    df_word_frequency = pd.read_csv('word_frequency.csv', error_bad_lines=False)

    # We find the positive and negatively correlated words for each topic.
    # We run a pearson coefficient test on these topics and then find all topics that add up to our probability mass.
    # This then creates two new topics which are reported in two new CSVs '[topic]_[positive/negative].csv'
    # which are written to disk.
    for index, row in df_word_per_topic.iterrows():
        topic = row[0]
        words = row[1].split(",")
        pearson_results = {}
        prob_mass = 0.75
        for word in words:
            df_word_freq = df_word_frequency[df_word_frequency.word == word]
            df_word_freq = df_word_freq.rename(columns={"date": "Date"})
            df_word_freq = pd.merge(df_word_freq, df_all_normalized, on="Date")
            df_word_freq = df_word_freq.loc[(df_word_freq['Contract'] == 'Dem')]
            # df_word_freq['frequency_stationary'] = df_word_freq['frequency']-df_word_freq['frequency'].shift(1)
            df_word_freq['NormalizedPrice_stationary'] = df_word_freq['NormalizedPrice'] - df_word_freq[
                'NormalizedPrice'].shift(1)
            # print(df_word_freq)
            df_word_freq = df_word_freq.dropna()
            corr, _ = pearsonr(df_word_freq['frequency'], df_word_freq['NormalizedPrice'])
            if not math.isnan(corr):
                pearson_results[word] = corr

        sorted_ascending = sorted(pearson_results.items(), key=operator.itemgetter(1))
        temp_mass = prob_mass
        negative_words = []
        for key in sorted_ascending:
            if key[1] > 0:
                break
            elif temp_mass + key[1] > 0:
                negative_words.append([key[0], key[1]])
                temp_mass = temp_mass + key[1]
        df_neg = pd.DataFrame(negative_words, columns=['Word', 'Probability'])
        file_name = "../CourseProject/prior_csvs/" + topic + "_negative.csv"
        df_neg.to_csv(file_name)

        sorted_descending = sorted(pearson_results.items(), key=operator.itemgetter(1), reverse=True)
        temp_mass = prob_mass
        positive_words = []
        min_probability = 1.0
        for key in sorted_descending:
            if key[1] < 0:
                break
            elif temp_mass - key[1] > 0:
                positive_words.append([key[0], key[1]])
                temp_mass = temp_mass - key[1]
                min_probability = min(min_probability, key[1])
                print(temp_mass)
        df_pos = pd.DataFrame(positive_words, columns=['Word', 'Probability'])
        file_name = "../CourseProject/prior_csvs/" + topic + "_positive.csv"
        df_pos.to_csv(file_name)

    return min_probability
