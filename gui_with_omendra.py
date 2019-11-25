from tkinter import *
import topic_modelling
import get_collaborators as get_collabs_omendra
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy

top = Tk()
top.title("Recommender System")
L1 = Label(top, text = "Insert Title")
L1.grid(row=0, column=0, columnspan=2, sticky=W, pady=50, padx=14)
E1 = Entry(top, bd = 2)
E1.grid(row=0, column=3, columnspan=2, sticky=W, pady=50, padx=14)
top.geometry("750x550")

variable = StringVar(top)
variable.set("Generalised Partner Search") # default value
w = OptionMenu(top, variable, "Generalised Partner Search", "Specialised Partner Search", "Mean Ranking Search","Median Ranking Search", "Overall Weights Author Search", "Individual Topic Weights Author Search")
w.grid(row=0, column=6, columnspan=2, sticky=W, pady=50, padx=14)

number_of_iterations = 0
number_of_iterations2 = 0

def open_name(name,i,d):
    print(name, i , d)
    wordcloud = WordCloud(background_color='white', width=1600, height=800, max_words=100, relative_scaling=0.5, normalize_plurals=False).generate_from_frequencies(d[i])
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()

label = []
label2 = []
list_tofilter = []
max3dictlist = []

label_ = []
label_2 = []
dict_authors = []

def helloCallBack():
    global number_of_iterations
    global number_of_iterations2 
    query = E1.get()

    if number_of_iterations2 != 0:
        for ll in range(len(label_)):
            label_[ll].pack_forget()
            label_[ll].destroy()
        for l2 in range(len(label_2)):
            label_2[l2].pack_forget()
            label_2[l2].destroy() 

        label_[:] = []
        label_2[:] = []

    if number_of_iterations != 0:
        for ll in range(len(label)):
            label[ll].pack_forget()
            label[ll].destroy()
        for l2 in range(len(label2)):
            label2[l2].pack_forget()
            label2[l2].destroy() 
        label[:] = []
        label2[:] = []
        max3dictlist[:] = []

    #Omendra code
    if variable.get() == 'Overall Weights Author Search' or  variable.get() == 'Individual Topic Weights Author Search':
        results_ranks = get_collabs_omendra.get_authors(query, variable.get())
        index = 1

        for key in results_ranks:
            dict_authors = {}
            for word_prob in results_ranks[key]['words']:
                if  dict_authors.get(word_prob[0]):
                    dict_authors[word_prob[1]] = dict_authors[word_prob[1]] + float(word_prob[0])*results_ranks[key]['weight']
                else:
                    dict_authors[word_prob[1]] = float(word_prob[0])*results_ranks[key]['weight']

            label_.append(Label(top, text=" ".join([str(index), key])))
            label_[index-1].grid(row=index, column=1, sticky=W)
            label_[index-1].bind("<Button-1>", lambda e, url=key: open_name(url,0,[dict_authors]))
            label_2.append(Label(top, text=dict_authors))
            label_2[index-1].grid(row=index, column=2, columnspan=10, sticky=W)
            index = index + 1
        number_of_iterations2+=1
    else:
        words_prob, real_words, authorList = topic_modelling.runQuery(query, variable.get())
        word_list = []
        list_tofilter[:] = []
        for i in range(len(real_words)):
            word_list.append(real_words[i][0])
            word_list.append(real_words[i][1])
        print(word_list)
        word_authors = []
        for authors in range(len(authorList)):
            for probbbs in range(len(words_prob)):
                for probs in range(len(words_prob[0])):
                    var = authorList[authors][probbbs+2]*words_prob[probbbs][probs]
                    word_authors.append(var)
        if word_authors:
            authors_prob = numpy.reshape(word_authors, (len(authorList), len(words_prob[0])*len(words_prob)))
            authors_listdict = []
            for prob1 in range(len(authors_prob)):
                temp_dict = {}
                for prob2 in range(len(authors_prob[0])):
                    if real_words[int(prob2/4)][prob2%4] not in temp_dict:
                        temp_dict[real_words[int(prob2/4)][prob2%4]] = authors_prob[prob1][prob2]
                    else:
                        temp_dict[real_words[int(prob2/4)][prob2%4]] += authors_prob[prob1][prob2]
                authors_listdict.append(temp_dict)
            sum = [0 for i in range(len(authors_listdict))]
            for item in range(len(authors_listdict)):
                for itt in authors_listdict[item]:
                    sum[item] += authors_listdict[item][itt]
            for itt2 in range(len(authors_listdict)):
                for it in authors_listdict[itt2]:
                    authors_listdict[itt2][it] = authors_listdict[itt2][it]/sum[itt2]
            new_authorslistdict = []
            for ii in range(len(authors_listdict)):
                new_authorslistdict.append({x: y for x, y in authors_listdict[ii].items() if y != 0})
        for vals in range(len(new_authorslistdict)):
            dict_hishest = {}
            for valss in range(len(word_list)):
                if word_list[valss] in new_authorslistdict[vals]:
                    dict_hishest[word_list[valss]] = new_authorslistdict[vals][word_list[valss]]
            list_tofilter.append(dict_hishest)

        # if number_of_iterations != 0:
        #     for ll in range(len(label)):
        #         label[ll].pack_forget()
        #         label[ll].destroy()
        #     for l2 in range(len(label2)):
        #         label2[l2].pack_forget()
        #         label2[l2].destroy() 
        label[:] = []
        label2[:] = []
        max3dictlist[:] = []

        if len(authorList)<25:
            authors_to_beprinted = len(authorList)
        else:
            authors_to_beprinted = 25

        for i in range(authors_to_beprinted):
            dict3maxs = {}
            dict3maxs2 = {}
            dict4maxs3 = {}
            dict4maxs4 = {}
            v_max = 0
            k_max = ""
            v_max2 = 0
            k_max2 = ""
            v_max3 = 0
            k_max3 = ""
            v_max4 = 0
            k_max4 = ""
            v_max5 = 0
            k_max5 = ""
            max3dict = {}
            if len(list_tofilter[i]) >= 5:
                for key, value in list_tofilter[i].items():
                    if value > v_max:
                        v_max = value
                        k_max = key
                for key1, value1 in list_tofilter[i].items():
                    if value1 != v_max:
                        dict3maxs[key1] = value1
                for key2, value2 in dict3maxs.items():
                    if value2 > v_max2:
                        v_max2 = value2
                        k_max2 = key2
                for key3, value3 in dict3maxs.items():
                    if value3 != v_max2:
                        dict3maxs2[key3] = value3
                for key4, value4 in dict3maxs2.items():
                    if value4 > v_max3:
                        v_max3 = value4
                        k_max3 = key4

                for k, v in dict3maxs2.items():
                    if v != v_max3:
                        dict4maxs3[k] = v
                for k1, v1 in dict4maxs3.items():
                    if v1 > v_max4:
                        v_max4 = v1
                        k_max4 = k1

                for k2, v2 in dict4maxs3.items():
                    if v2 != v_max4:
                        dict4maxs4[k2] = v2
                for k3, v3 in dict4maxs4.items():
                    if v3 > v_max5:
                        v_max5 = v3
                        k_max5 = k3
            elif len(list_tofilter[i]) == 4:
                for key, value in list_tofilter[i].items():
                    if value > v_max:
                        v_max = value
                        k_max = key
                for key1, value1 in list_tofilter[i].items():
                    if value1 != v_max:
                        dict3maxs[key1] = value1
                for key2, value2 in dict3maxs.items():
                    if value2 > v_max2:
                        v_max2 = value2
                        k_max2 = key2
                for key3, value3 in dict3maxs.items():
                    if value3 != v_max2:
                        dict3maxs2[key3] = value3
                for key4, value4 in dict3maxs2.items():
                    if value4 > v_max3:
                        v_max3 = value4
                        k_max3 = key4
                for k, v in dict3maxs2.items():
                    if v != v_max3:
                        dict4maxs3[k] = v
                for k1, v1 in dict4maxs3.items():
                    if v1 > v_max4:
                        v_max4 = v1
                        k_max4 = k1
                v_max5 = 0
                k_max5 = ""
            elif len(list_tofilter[i]) == 3:
                for key, value in list_tofilter[i].items():
                    if value > v_max:
                        v_max = value
                        k_max = key
                for key1, value1 in list_tofilter[i].items():
                    if value1 != v_max:
                        dict3maxs[key1] = value1
                for key2, value2 in dict3maxs.items():
                    if value2 > v_max2:
                        v_max2 = value2
                        k_max2 = key2
                for key3, value3 in dict3maxs.items():
                    if value3 != v_max2:
                        dict3maxs2[key3] = value3
                for key4, value4 in dict3maxs2.items():
                    if value4 > v_max3:
                        v_max3 = value4
                        k_max3 = key4
                v_max4 = 0
                k_max4 = ""
                v_max5 = 0
                k_max5 = ""
            elif len(list_tofilter[i]) == 2:
                for key, value in list_tofilter[i].items():
                    if value > v_max:
                        v_max = value
                        k_max = key
                for key1, value1 in list_tofilter[i].items():
                    if value1 != v_max:
                        dict3maxs[key1] = value1
                for key2, value2 in dict3maxs.items():
                    if value2 > v_max2:
                        v_max2 = value2
                        k_max2 = key2
                v_max3 = 0
                k_max3 = ""
                v_max4 = 0
                k_max4 = ""
                v_max5 = 0
                k_max5 = ""
            elif len(list_tofilter[i]) == 1:
                for key, value in list_tofilter[i].items():
                    if value > v_max:
                        v_max = value
                        k_max = key
                v_max2 = 0
                k_max2 = ""
                v_max3 = 0
                k_max3 = ""
                v_max4 = 0
                k_max4 = ""
                v_max5 = 0
                k_max5 = ""
            else:
                v_max = 0
                k_max = ""
                v_max2 = 0
                k_max2 = ""
                v_max3 = 0
                k_max3 = ""
                v_max4 = 0
                k_max4 = ""
                v_max5 = 0
                k_max5 = ""
            if v_max != 0:
                max3dict[k_max] = v_max
            if v_max2 != 0:
                max3dict[k_max2] = v_max2
            if v_max3 != 0:
                max3dict[k_max3] = v_max3
            if v_max4 != 0:
                max3dict[k_max4] = v_max4
            if v_max5 != 0:
                max3dict[k_max5] = v_max5
            max3dictlist.append(max3dict)
        name = ['' for i in range(len(authorList))]
        for i in range(authors_to_beprinted):
            firstName = authorList[i][0]
            lastName = authorList[i][1]
            name[i] = " ".join([firstName, lastName])
            nn = str(i+1)+". " + name[i]
            label.append(Label(top, text=nn))
            label[i].grid(row=i+1, column=1, sticky=W)
            label[i].bind("<Button-1>", lambda e, url=name[i]: open_name(url,name.index(url),new_authorslistdict))
            label2.append(Label(top, text=max3dictlist[i]))
            label2[i].grid(row=i+1, column=2, columnspan=10, sticky=W)
        number_of_iterations+=1

B = Button(top, text ="Submit", width=10, command = helloCallBack)
B.grid(row=0, column=9, columnspan=2, sticky=W, pady=50, padx=14)

def func(event):
    helloCallBack()
top.bind('<Return>', func)

top.mainloop()