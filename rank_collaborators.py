from operator import itemgetter
import math
from langdetect import detect
import random
import re
import pickle


dir_name = ''
persons_dict = {}
author_with_topics = []
topics_with_authors = {}

def load_datasets(dir_name):
	# LOAD DATASETS
	path = dir_name + '/author_profile_normalised'
	author_with_topics_file = open(path, 'rb')
	path = dir_name + '/topic_with_authors'
	topics_with_authors_file = open(path, 'rb')
	path = dir_name + '/person_dict'
	person_dict_file = open(path, 'rb')
	unpickler = pickle.Unpickler(author_with_topics_file)
	author_with_topics = unpickler.load()

	unpickler = pickle.Unpickler(topics_with_authors_file)
	topics_with_authors = unpickler.load()

	unpickler = pickle.Unpickler(person_dict_file)
	persons_dict = unpickler.load()

	return author_with_topics, topics_with_authors, persons_dict

def algorithm_first(matches, author_with_topics, topics_with_authors, persons_dict):
	suggested_authors = []
	result = dict()

	for topic_id in [match[0] for match in matches]:
		if topics_with_authors.get(topic_id):
			suggestions = [(author[0], author[1], topic_id) for author in topics_with_authors[topic_id]]
			suggestions.sort(key=itemgetter(1), reverse=True)
			suggested_authors.append(suggestions)

	for authors in suggested_authors:
		for author in authors:
			if result.get(author[0]):
				result[author[0]] = result[author[0]] + [(author[2], author[1])]
			else:
				result[author[0]] = [(author[2], author[1])]

	resolved_result = []

	for key in result:
		people = result[key]
		weight = 0
		topics = []

		for data in people:
			weight = weight + data[1]
			topics.append(data[0])

		resolved_result.append((key , weight, topics))

	resolved_result.sort(key=lambda tup:tup[1] + math.log(len(tup[2])), reverse=True)
	return resolved_result

def getRandomIndices(a, b):
	rand_A = random.randint(0, len(authors)-1)
	rand_B = random.randint(0, len(authors)-1)

	return rand_A, rand_B


def compareAuthors(A, i, j):
	A1 = persons_dict[A[i][0]]['experience']
	B1 = persons_dict[A[j][0]]['experience']

	if A[i][1] > A[j][1]: return i
	else: return j

def draw_sample(result, L, k):
	peoples = []

	while True:
		random_A = random.sample(L, k)
		random_A.sort(key=itemgetter(1), reverse=True)

		if random_A[0][0] not in [x[0] for x in peoples]:
			peoples.append(random_A[0])
		if len(peoples) > k-1: break

	return peoples

def algorith_second(matches, author_with_topics, topics_with_authors, persons_dict):
	suggested_authors = []
	result = []
	matches_found = len(matches)

	for topic_id in [match[0] for match in matches]:
		if topic_id in topics_with_authors.keys():
			suggestions = [(author[0], author[1], topic_id) for author in topics_with_authors[topic_id]]
			suggestions.sort(key=itemgetter(1), reverse=True)
			suggested_authors.append(suggestions)

	for index,authors in enumerate(suggested_authors):
		collabs = []
		match = matches[index]
		topic_id_chance = match[1]
		result_keys = [x[0] for x in result]

		if len(authors) > 15:
			authors = authors[0:15]

		N = math.ceil(match[1]*len(authors))
		if N < 1: N = 1
		if N > len(authors): N = len(authors)

		for i in range(N):
			rem = [author for author in authors if author[0] not in [x[0] for x in collabs]]
			M = 10
			if len(rem) < 10:
				M = len(rem)

			i = random.randint(0,M-1)
			j = random.randint(0,M-1)

			if i==j:
				collabs.append(rem[j] + (match[0],))
				continue

			if rem[i][1] < rem[j][1]: collabs.append(rem[j] + (match[0],))
			else: collabs.append(rem[i] + (match[0],))

		result = result + collabs

	return result

def suggest_people_first_algorithm(matches, dir_name):
	author_with_topics, topics_with_authors, persons_dict = load_datasets(dir_name)
	first_results = algorithm_first(matches, author_with_topics, topics_with_authors, persons_dict)

	return first_results

def suggest_people_second_algorithm(matches, dir_name):
	author_with_topics, topics_with_authors, persons_dict = load_datasets(dir_name)
	second_results = algorith_second(matches, author_with_topics, topics_with_authors, persons_dict)

	return second_results

