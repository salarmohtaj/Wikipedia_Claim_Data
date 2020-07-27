import pickle
import random
import requests as RQ
from bs4 import BeautifulSoup
import spacy
nlp = spacy.load("en")
wiki_pages = pickle.load(open("Links.LIST",'rb'))
ll = random.sample(wiki_pages,25)
#url = "https://en.wikipedia.org/wiki/Karl_Christian_Erdmann_von_Le_Coq"

eliminated_because_of_pronoun = 0
URL_Dic = {}
Category_Dic = {}
list_of_sentences = []

for url in ll:
    r= RQ.get(url)
    soup = BeautifulSoup(r.content , features = "html.parser" )
    flag = 0
    for tag in soup.find_all("p"):
        if(".[citation needed]" in tag.text):
            text_to_study = tag.text
            count = text_to_study.count(".[citation needed]")
            for i in range(count):
                index = text_to_study.find(".[citation needed]")
                potential_sentence = text_to_study[:index+1]
                sentence = nlp(potential_sentence)
                for sent in sentence.sents:
                    citation_needed_sentence = sent.string.strip()
                doc = nlp(citation_needed_sentence)
                if(doc[0].tag_ == "PRP" or doc[0].tag_ == "PRP$"):
                    eliminated_because_of_pronoun+=1
                    #print("___________")
                #print(citation_needed_sentence)
                list_of_sentences.append(citation_needed_sentence)
                flag = 1
                try:
                    URL_Dic[url]+=1
                except:
                    URL_Dic[url]=1
                text_to_study = text_to_study[index+19:]
            #print(tag.text)
    if flag == 1:
        temp = soup.find("div",{"id":"mw-normal-catlinks"})
        for tagtemp in temp.find_all("li"):
            try:
                Category_Dic[tagtemp.text]+=1
            except:
                Category_Dic[tagtemp.text] = 1

print(list_of_sentences)
print(URL_Dic)
print(Category_Dic)
print("{} Sentecnes are scraped from {} URLs.".format(len(list_of_sentences),len(URL_Dic)))
print("{} sentences are removed because of having Pronouns in the beginning.".format(eliminated_because_of_pronoun))
