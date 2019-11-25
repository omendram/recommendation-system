from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from gensim import corpora
import spacy
spacy.load('en')
from spacy.lang.en import English
parser = English()
from operator import itemgetter

primary_location = 'scopus_primary'
secondary_location = 'scopus_topic_counts'

def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

# Download stopwords from nltk corpus
en_stop = stopwords.words('english')

# Convert to tokens
def getLDATokens(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 2]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

def get_topics(query):
    if len(query)<1: return (False, 'Please enter more words!')

    dictionary_first = corpora.Dictionary.load(primary_location + '/dictionary.gensim')
    ldamodel = gensim.models.ldamodel.LdaModel.load(primary_location + '/model.gensim')
    dir_name = 'scopus_primary'

    # To get the topic list for the query string
    query = getLDATokens(query)
    query_bow = dictionary_first.doc2bow(query)
    matches = ldamodel.get_document_topics(query_bow)

    if len(matches) < 1:
        dictionary_second = corpora.Dictionary.load(secondary_location + '/dictionary.gensim')
        ldamodel = gensim.models.ldamodel.LdaModel.load(secondary_location + '/model.gensim')
        query_bow = dictionary_second.doc2bow(query)
        matches = ldamodel.get_document_topics(query_bow)
        dir_name = 'scopus_topic_counts'

    if len(matches) < 1:
    	return (False, 'No matches found! Try different words!')

    matches.sort(key=itemgetter(1), reverse=True)
    return (ldamodel, matches, dir_name)
