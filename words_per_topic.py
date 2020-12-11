import csv
from operator import itemgetter

csv_dict = {}
with open('plsa.csv') as f:
	reader = csv.reader(f)
	next(reader)

	for row in reader:
		if row[0] in csv_dict.keys():
			internal = csv_dict[row[0]]
			internal[row[1]] = row[2]
			csv_dict[row[0]] = internal
		else:
			internal = {}
			internal[row[1]] = row[2]
			csv_dict[row[0]] = internal

# {date: {word: probability, word2: probability2, ...}}

topic_dict = {}
topic_dict['bush'] = {}
topic_dict['gore'] = {}
topic_dict['campaign'] = {}
topic_dict['clinton'] = {}

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



