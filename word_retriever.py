import csv
import os

import xml.etree.ElementTree as ET


def retrieve_words_per_topic_and_frequency(plsa_filename):
	csv_dict = {}
	with open(plsa_filename) as f:
		reader = csv.reader(f)
		next(reader)

		for row in reader:
			if row[0] in csv_dict.keys():
				internal = csv_dict[row[0]]
				internal[row[1]] = row[2]
				csv_dict[row[0]] = internal
			else:
				internal = {row[1]: row[2]}
				csv_dict[row[0]] = internal

	topic_dict = {'bush': {}, 'gore': {}, 'campaign': {}, 'clinton': {}}

	for key, value in csv_dict.items():
		if 'bush' in value.keys():
			internal = topic_dict['bush']
			internal.update(value)
			topic_dict['bush'] = internal
		if 'gore' in value.keys():
			internal = topic_dict['gore']
			internal.update(value)
			topic_dict['gore'] = internal
		if 'campaign' in value.keys():
			internal = topic_dict['campaign']
			internal.update(value)
			topic_dict['campaign'] = internal
		if 'clinton' in value.keys():
			internal = topic_dict['clinton']
			internal.update(value)
			topic_dict['clinton'] = internal

	with open('words_per_topic.csv', mode='w') as file:
		fieldnames = ['topic', 'words']
		writer = csv.DictWriter(file, fieldnames=fieldnames)

		for key, value in topic_dict.items():
			print(key)
			sorted_words = sorted(value, key=value.get, reverse=True)[:20]
			print(sorted_words)
			sorted_words_string = ','.join([str(e) for e in sorted_words])
			print(sorted_words_string)

			writer.writerow({'topic': key, 'words': sorted_words_string})

	# Get frequency of each word for each day
	word_set = set()
	for key, value in topic_dict.items():
		sorted_words = sorted(value, key=value.get, reverse=True)[:20]
		for word in sorted_words:
			word_set.add(word)

	directory = '../CourseProject/data/'
	with open('word_frequency.csv', mode='w') as file:
		fieldnames = ['date', 'word', 'frequency']
		writer = csv.DictWriter(file, fieldnames=fieldnames)

		writer.writeheader()
		for subdir, dirs, files in os.walk(directory):
			# We should look for files in directories with format '../CourseProject/data/<month>/<day>'
			directory_name = subdir.split('/')
			if (len(directory_name) != 5):
				continue

			filenames = os.listdir(subdir)
			date = directory_name[3] + '/' + directory_name[4] + '/00'

			word_frequency = {}
			for word in word_set:
				word_frequency[word] = 0

			for filename in filenames:
				root = ET.parse(subdir + '/' + filename)
				for w in root.iter('p'):
					text = w.text
					if text is None:
						continue
					for word in word_set:
						freq = word_frequency[word]
						freq = freq + text.count(word)
						word_frequency[word] = freq

			for key, value in word_frequency.items():
				writer.writerow({'date': date, 'word': key, 'frequency': value})