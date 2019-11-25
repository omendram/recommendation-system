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
import json
import copy
from langdetect import detect

spacy.load('en')
from spacy.lang.en import English
parser = English()

#Omendra, Andreea, Sofia

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

data = []
with open('data/profiles_with_titles.json',encoding="utf8") as handle:
    with open('authorsretrieved.json', 'w', encoding="utf8") as json_clean:
        dictdump = json.load(handle)
        for x in range(len(dictdump)):
            print(x)
            if dictdump[x]['publicationTitles']:
                id = []
                prob = []
                for i in range(len(dictdump[x]['publicationTitles'])):
                    if detect(dictdump[x]['publicationTitles'][i]) == "en":
                        query = str(dictdump[x]['publicationTitles'][i])
                        query = getLDATokens(query)
                        query_bow = dictionary.doc2bow(query)
                        # Need to decide the min prob and check which is the best to do
                        matches = ldamodel.get_document_topics(query_bow)
                        printer = pprint.PrettyPrinter(indent=2)
                        matches.sort(key=itemgetter(1), reverse=True);
                        i=0
                        for match in matches:
                            id.append(match[0])
                            prob.append(str(match[1]))
                            i+=1
                if len(id)!=0:
                    info = []
                    print(type(prob))
                    del dictdump[x]["uuid"]
                    del dictdump[x]["portalUrl"]
                    dictdump[x]["topicid"] = copy.deepcopy(id)
                    dictdump[x]["topicprob"] = copy.deepcopy(prob)
                    print(type(dictdump[x]))
                    data.append(dictdump[x])
        json_clean.write(json.dumps(data,indent=4,ensure_ascii=False))