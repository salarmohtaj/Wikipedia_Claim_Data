import pickle
import random
import requests as RQ
from bs4 import BeautifulSoup
import re
import spacy
import os
#import neuralcoref
nlp = spacy.load('en')
#neuralcoref.add_to_pipe(nlp)
regexp = re.compile(r'\[.*?\]')

data_dir = "Data"
input_list_name = "Links.LIST"
input_list_name_reminded = "Links_reminded.LIST"
json_filename = "Claims_JSON.LIST"
ID_file = "last_ID.PICKLE"
nlp = spacy.load("en")

try:
    with open(os.path.join(data_dir, input_list_name_reminded), "rb") as tempfile:
        wiki_pages = pickle.load(tempfile)
except:
    with open(os.path.join(data_dir, input_list_name), "rb") as tempfile:
        wiki_pages = pickle.load(tempfile)
#wiki_pages = random.sample(wiki_pages,200)
LEN = len(wiki_pages)

limit = 100

try:
    with open(os.path.join(data_dir, ID_file) , 'rb') as tempfile:
        ID = pickle.load(tempfile)
except:
    ID = 10001

try:
    with open(os.path.join(data_dir, json_filename), "rb") as tempfile:
        MAIN_LIST = pickle.load(tempfile)
except:
    MAIN_LIST = []



for i in range(limit):
    url = wiki_pages.pop(0)
    if(i % 10 == 0):
        print("{} URLs crawled out of {}".format(i,LEN))
        with open(os.path.join(data_dir, json_filename) , 'wb') as file:
            pickle.dump(MAIN_LIST,file)
        with open(os.path.join(data_dir, input_list_name_reminded) , 'wb') as file:
            pickle.dump(wiki_pages,file)
    try:
        r= RQ.get(url)
        soup = BeautifulSoup(r.content , features = "html.parser" )
    except:
        continue
    Categories = []
    try:

        temp = soup.find("div", {"id": "mw-normal-catlinks"})
        for tagtemp in temp.find_all("li"):
            Categories.append(tagtemp.text)
        Categories = list(set(Categories))
    except:
        pass
    Claims = []
    Normal_sentences = []
    try:
        for tag in soup.find_all("p"):
            text_to_study = tag.text
            sentences = nlp(text_to_study)
            for sent in sentences.sents:
                sentence = sent.string.strip()
                if ("[citation needed]" in sentence):
                    sentence = sentence.replace("[citation needed]", " ")
                    if (not regexp.search(sentence)):
                        sentence = re.sub(' +', ' ', sentence)
                        Claims.append(sentence)
                        #print("CLAIM: "+sentence)
                    else:
                        pass
                        #print("Error: "+sentence)
                elif (regexp.search(sentence)):
                    # There is some citation in the sentence
                    continue
                else:
                    sentence = re.sub(' +', ' ', sentence)
                    Normal_sentences.append(sentence)
                    #print("Normal: " + sentence)
    except:
        pass
    dic = {"id" : ID ,
           "url" : url ,
           "claims" : list(filter(None, Claims)) ,
           "categories" : list(filter(None, Categories)) ,
           "non_claims" : list(filter(None, Normal_sentences))
           }
    ID += 1
    MAIN_LIST.append(dic)
with open(os.path.join(data_dir, json_filename) , 'wb') as file:
    pickle.dump(MAIN_LIST, file)
with open(os.path.join(data_dir, ID_file) , 'wb') as file:
    pickle.dump(ID, file)
with open(os.path.join(data_dir, input_list_name_reminded), 'wb') as file:
    pickle.dump(wiki_pages, file)

print("{} URLs should be scraped".format(len(wiki_pages)))
print("Our current ID is {}".format(ID))
print("Length of crawled data is {} items.".format(len(MAIN_LIST)))





#url = "https://en.wikipedia.org/wiki/Karl_Christian_Erdmann_von_Le_Coq"
#eliminated_because_of_pronoun = 0
#eliminated_because_of_length = 0
#URL_Dic = {}
#Category_Dic = {}
#list_of_sentences = []
#NOT_Crawled_URLs = 0
#length_threshould = 20 # Minimum length for sentences in character

"""if(".[citation needed]" in tag.text):
    text_to_study = tag.text
    count = text_to_study.count(".[citation needed]")
    for i in range(count):
        index = text_to_study.find(".[citation needed]")
        potential_sentence = text_to_study[:index+1]
        sentence = nlp(potential_sentence)
        for sent in sentence.sents:
            citation_needed_sentence = sent.string.strip()
        Claims.append(citation_needed_sentence)
        text_to_study = text_to_study[index + 19:]
doc = nlp(citation_needed_sentence)
if(doc[0].tag_ == "PRP" or doc[0].tag_ == "PRP$"):
    # Remove sentence in begin with Pronouns
    eliminated_because_of_pronoun += 1
elif(len(citation_needed_sentence) < length_threshould):
    eliminated_because_of_length += 1
else:
    list_of_sentences.append(citation_needed_sentence)
    flag = 1
    try:
        URL_Dic[url] += 1
    except:
        URL_Dic[url] = 12

print(list_of_sentences)
print(URL_Dic)
print(Category_Dic)
print("{} Sentecnes are scraped from {} URLs.".format(len(list_of_sentences),len(URL_Dic)))
print("{} sentences are removed because of having Pronouns in the beginning and {} sentences are removed because of short length.".format(eliminated_because_of_pronoun,eliminated_because_of_length))
print("There was no usable Citation needed tag in {} URLs.".format(NOT_Crawled_URLs))"""


