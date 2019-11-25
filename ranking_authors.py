import json, operator
from more_itertools import unique_everseen
from tabulate import tabulate
from statistics import mean, median

#top x taken from each list
topNum = 10

#4 sorting options in total: 2 methods with 2 variations each

#sort by number of topics (highest or lowest), topic order, probabilities
def rankSort1(authorTable, queryTopics, headerRow, favourHighestTopicCount=True):
    global topNum
    lastProb = len(queryTopics)+2  
    #add a last column with a number that indicates in what order
    #the topic probabilities of each row go when sorted descending
    for r in range(len(authorTable)):
        row = authorTable[r][2:lastProb]
        newRowField = [str(i[0]+1) for i in sorted(enumerate(row), key=lambda x: float(x[1]), reverse=True)]
        newRowField = ''.join(newRowField)
        authorTable[r].append(int(newRowField))
    #start sorting
    if favourHighestTopicCount:
        rev = True
    else:
        rev=False
    authorTable.sort(key=lambda x: float(max(x[2:-2])), reverse=True) #max topic
    authorTable.sort(key=lambda x: x[-1]) #topic order
    authorTable.sort(key=lambda x: x[-2], reverse=rev) #topic count
    #cut down on the number of entries: take top x of each topic count
    #except single
    cutAuthorTable = []
    if favourHighestTopicCount:
        loopRange = range(len(queryTopics),1,-1) #descending
    else:
        loopRange = range(2,len(queryTopics)+1,1) #ascending
    for tn in loopRange:
        subList = [row for row in authorTable if row[-2] == tn][:topNum]
        cutAuthorTable.extend(subList)
    #take for the single topics the highest probabilities
    subList = [row for row in authorTable if row[-2] == 1]
    subList.sort(key=lambda x: float(max(x[2:-2])),reverse = True) #max topic probability
    subList = subList[:topNum]
    if favourHighestTopicCount:
        cutAuthorTable.extend(subList)
    else:
        #insert at front
        cutAuthorTable[0:0] = subList
    #remove topic count and topic order columns
    cutAuthorTable = [row[:-2] for row in cutAuthorTable]
    #show table
    # print(tabulate(cutAuthorTable,headers=headerRow))
    return(cutAuthorTable)


#take top x for each topic and join using mean/median, break ties with highest propability
def rankSort2(authorTable, queryTopics, headerRow, useMean=True):
    global topNum
    lastProb = len(queryTopics)+2
    topicIndices = range(2,lastProb)
    #remove topic count column
    authorTable = [row[:-1] for row in authorTable]
    topList = {}
    #create the lists per topic
    for i in topicIndices:
        authorTable.sort(key=lambda x: float(x[i]), reverse=True)
        subList = authorTable[:topNum]
        #add a column that indicates rank
        subList = [row+[[i+1]] for i,row in enumerate(subList)]
        #use a dict to avoid duplication
        for row in subList:
            if (row[0], row[1]) in topList.keys():
                topList[(row[0], row[1])][-1].append(row[-1][0])
            else:
                topList[(row[0], row[1])] = row[2:]
    #use mean to calculate new rank
    if useMean:
        mergedList = [[[a[0],a[1]]+n[:-1]+[mean(n[-1])]][0] for a,n in topList.items()]
    else:
        mergedList = [[[a[0],a[1]]+n[:-1]+[median(n[-1])]][0] for a,n in topList.items()]
    #start sorting
    mergedList.sort(key=lambda x: float(max(x[2:-1])), reverse=True) #max topic probability
    mergedList.sort(key=lambda x: float(x[-1])) #rank
    #remove rank column
    mergedList = [row[:-1] for row in mergedList]
    #show table
    # print(tabulate(mergedList,headers=headerRow))
    return(mergedList)

#query must be always a list of Id and probabilities
def Lianne(query, SortingAlg_opt = "Generalised Partner Search"):
    queryTopics = [q for q, p in query]
    headerRow = ['First name', 'Last name'] + queryTopics
    with open('topic_authors.json', 'r', encoding="utf8") as json_A_per_T:
        with open('author_topics.json', 'r', encoding="utf8") as json_T_per_A:
            dict_A_per_T = json.load(json_A_per_T)
            dict_T_per_A = json.load(json_T_per_A)
            authors = []
            #get authors
            for q in range(len(queryTopics)):
                for i in range(len(dict_A_per_T)):
                    if dict_A_per_T[i]['TopicID'] == queryTopics[q]:
                        authors.extend(dict_A_per_T[i]['AuthorsNames'])
            #remove duplicates
            authors = list(unique_everseen(authors))
            authorTable = []
            #create author table
            for r in range(len(authors)):
                subList = []
                for entry in dict_T_per_A:
                    if ' '.join([entry['firstName'], entry['lastName']]) == authors[r]:
                        subList.append(entry['firstName'])
                        subList.append(entry['lastName'])
                        #for adding an topic count column
                        topicCount = 0
                        for t in queryTopics:
                            if t in entry['topicID']:
                                index = entry['topicID'].index(t)
                                subList.append(entry['topicProb'][index])
                                topicCount += 1
                            else:
                                subList.append(float(0))
                        subList.append(topicCount)
                        authorTable.append(subList)
                        break
            fullTable = [row[:-1] for row in authorTable]
            #set sorting method 1 or 2 and pick variation True or False
            if SortingAlg_opt =="Generalised Partner Search":
                authorList = rankSort1(authorTable, queryTopics, headerRow, True)
            elif SortingAlg_opt == "Specialised Partner Search":
                authorList = rankSort1(authorTable, queryTopics, headerRow, False)
            elif SortingAlg_opt == "Mean Ranking Search":
                authorList = rankSort2(authorTable, queryTopics, headerRow, True)
            else:
                authorList = rankSort2(authorTable, queryTopics, headerRow, False)
            return(authorList)

