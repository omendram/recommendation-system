import lda_model as LDA
import rank_collaborators as COLLAB
import show_figures as FIG
from operator import itemgetter
import pickle
from prettytable import PrettyTable
import re

def handleError(matches, dir_name):
	print('Error occurred!')
	print(dir_name)
	exit()

def recommend(query, alg_id):
	LDA_Model,matches,dir_name = LDA.get_topics(query)

	if matches != False:
		path = dir_name + '/person_dict'
		person_dict_file = open(path, 'rb')
		unpickler = pickle.Unpickler(person_dict_file)
		persons_dict = unpickler.load()

		if alg_id == 'first':
			first_suggestions = COLLAB.suggest_people_first_algorithm(matches, dir_name)
			first_suggestions.sort(key=itemgetter(1), reverse=True)
			result = {}
			for idx,author in enumerate(first_suggestions):
				author_name = persons_dict[author[0]]['name']
				author_words = []

				for topic_id in author[2]:
					author_detail = LDA_Model.print_topic(topic_id, topn=2)
					words = [[w.replace('"', '') for w in word.split('*')] for word in author_detail.split('+')]
					author_words = author_words + words
				result[author_name] =  {'words': author_words, 'weight': author[1]}

				if idx > 19:
					break
		if alg_id == 'second':
			second_suggestions = COLLAB.suggest_people_second_algorithm(matches, dir_name)
			result = {}

			for idx,author in enumerate(second_suggestions):
				author_name =  persons_dict[author[0]]['name']
				author_detail = LDA_Model.print_topic(author[2], topn=2)
				author_words = [[w.replace('"', '') for w in word.split('*')] for word in author_detail.split('+')]
				result[author_name] =  { 'words': author_words, 'weight': author[1]}

				if idx > 19:
					break
			
		return result
	else:
		handleError(matches, dir_name)

def test():
	queries = ['cancer research and big data algorithms']
	for query in queries:
		print(recommend(query, 'first'))
		print('----END----')

def get_authors(query, alg_id):
	if alg_id == 'Overall Weights Author Search':
		return recommend(query, 'first')

	if alg_id == 'Individual Topic Weights Author Search':
		return recommend(query, 'second')