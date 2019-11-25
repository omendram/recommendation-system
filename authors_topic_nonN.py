import json
from sklearn.preprocessing import normalize as n
import numpy as np

#Andreea, Sofia

with open('authorsretrieved.json', encoding="utf8") as json_clean:
    with open('author_topics_nonN.json', 'w', encoding="utf8") as json_arti:
        dictdump = json.load(json_clean)
        temp_dictionary = []
        keys = ['firstName', 'lastName', 'topicID', 'topicProb']
        for x in range(len(dictdump)):
            print(x, "     = ", dictdump[x]['topicid'])
            topic_id =  dictdump[x]['topicid']
            prob = dictdump[x]['topicprob']
            new_topic_id = []
            new_topic_prob = []
            for i in range(len(topic_id)):
                if topic_id[i] not in new_topic_id:
                    new_topic_id.append(topic_id[i])
                    new_topic_prob.append(float(prob[i]))
                else:
                    id_indx = new_topic_id.index(topic_id[i])
                    new_topic_prob[id_indx] += float(prob[i])
            print("Without norm:  ",new_topic_prob)
            firstName = dictdump[x]['firstName']
            lastName = dictdump[x]['lastName']
            topicID = new_topic_id
            l = [firstName, lastName, topicID, new_topic_prob]
            temp_dictionary.append(dict(zip(keys, l)))
        json_arti.write(json.dumps(temp_dictionary, indent=4, ensure_ascii=False))
