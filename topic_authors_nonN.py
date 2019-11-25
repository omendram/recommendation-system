import json

#Sofia

data = []
mini = 0
maxi = 0

topic_authors = []
with open('authorsretrieved.json',encoding="utf8") as json_clean:
    with open('topic_authors_nonN.json', 'w', encoding="utf8") as json_topic:
        dictdump = json.load(json_clean)
        temp_dictionary = []
        keys = ['firstName','lastName','topicid','topicprob']
        keys2 = ['TopicID','AuthorsNames','topicProb']
        for x in range(len(dictdump)):
            firstName = dictdump[x]['firstName']
            lastName =  dictdump[x]['lastName']
            topicID = dictdump[x]['topicid']
            topicProb = dictdump[x]['topicprob']
            if max(topicID)>maxi:
                maxi = topicID[topicID.index(max(topicID))]
            if min(topicID)<mini:
                mini = topicID[topicID.index(min(topicID))]
            l = [firstName, lastName, topicID, topicProb]
            temp_dictionary.append(dict(zip(keys, l)))
        print(mini)
        print(maxi)
        c=0
        for i in range(mini,maxi+1,1):
            c = 0
            listtt = []
            probb = []
            for x in temp_dictionary:
                if i in x['topicid']:
                    c+=1
                    listtt.append(' '.join([x['firstName'], x['lastName']]))
                    probb.append(float(x['topicprob'][x['topicid'].index(i)]))
            # for k in range(len(probb)):
            #     probb[k]= probb[k]/sum(probb)
            l2 = [i, listtt, probb]
            topic_authors.append(dict(zip(keys2, l2)))
        json_topic.write(json.dumps(topic_authors, indent=4, ensure_ascii=True))
