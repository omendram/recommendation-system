import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.corpus import wordnet as wn
import spacy
from nltk.stem.wordnet import WordNetLemmatizer
import pprint
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora
import gensim
from operator import itemgetter
import ranking_authors

spacy.load('en')
from spacy.lang.en import English
parser = English()

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

def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

# Download stopwords from nltk corpus
en_stop = stopwords.words('english')

# Convert to tokens
def getLDATokens(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 2]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

dictionary = corpora.Dictionary.load('data/dictionary_1.2.gensim')
ldamodel = gensim.models.ldamodel.LdaModel.load('data/model_1.2.gensim')

# To get the topic list for the query string
#query = str(input("Query: ->"))

def runQuery(query, SortingAlg_opt):
    topic_ids = []
    words = []
    query = getLDATokens(query)
    query_bow = dictionary.doc2bow(query)

    # Need to decide the min prob and check which is the best do
    matches = ldamodel.get_document_topics(query_bow)
    printer = pprint.PrettyPrinter(indent=2)
    matches.sort(key=itemgetter(1), reverse=True);

    for match in matches:
        # print(match)
        topic_ids.append(match)
        words.append(ldamodel.print_topic(match[0], topn=4))
        printer.pprint(ldamodel.print_topic(match[0], topn=4))
    query1 = topic_ids
    # print(query1)
    authorList = ranking_authors.Lianne(query1, SortingAlg_opt)
    # print(authorList)
    words_prob = []
    topic_prob = []
    real_words = []
    for k in range(len(words)):
        mpla = words[k].split('+')
        prob = []
        t_words = []
        for j in range(len(mpla)):
            numbers = mpla[j].split('*')
            t_words.append((numbers[1].replace('\"', '')).replace(" ",""))
            prob.append(float(numbers[0]))
        words_prob.append(prob)
        real_words.append(t_words)
        topic_prob.append(topic_ids[k][1])

    for i in range(len(topic_prob)):
        for j in range(len(words_prob[0])):
            words_prob[i][j] = topic_prob[i]*words_prob[i][j]
    # print(words_prob)
    return(words_prob, real_words, authorList)

