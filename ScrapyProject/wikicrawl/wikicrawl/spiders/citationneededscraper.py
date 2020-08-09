import scrapy    # adding scrapy to our file
from urllib.parse import urlparse
import os
from bs4 import BeautifulSoup
#import spacy
import re
import json
import pickle
#nlp = spacy.load("en")

class CitationNeededScraper(scrapy.Spider):   # our class inherits from scrapy.Spider
    name = "citationneeded"
    def start_requests(self):
        #urls = ['https://en.wikipedia.org/wiki/Quake_4',]  # list to enter our urls
        with open("Links.LIST", "rb") as tempfile:
            urls = pickle.load(tempfile)

        urls = urls[:50]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = urlparse(response.request.url).path
        with open(os.path.join("data", filename.replace("/", "_") + ".html"), 'w') as f:
            f.write(response.text)


    def parse1(self, response):
        Categories = response.xpath('//div[@id="mw-normal-catlinks"]/ul/li/a/text()').getall()
        Categories = list(set(Categories))
        Claims = []
        Normal_sentences = []
        regexp = re.compile(r'\[.*?\]')
        text = response.xpath('//p').getall()
        for tt in text:
            soup = BeautifulSoup(tt)
            text_to_study = soup.text
            ###############################
            #sentences = nlp(text_to_study)
            ################################
            for sent in sentences.sents:
                sentence = sent.string.strip()
                if ("[citation needed]" in sentence):
                    sentence = sentence.replace("[citation needed]", " ")
                    if (not regexp.search(sentence)):
                        sentence = re.sub(' +', ' ', sentence)
                        Claims.append(sentence)
                        # print("CLAIM: "+sentence)
                    else:
                        pass
                        # print("Error: "+sentence)
                elif (regexp.search(sentence)):
                    # There is some citation in the sentence
                    continue
                else:
                    sentence = re.sub(' +', ' ', sentence)
                    Normal_sentences.append(sentence)
        dic = {"url": response.request.url,
               "claims": list(filter(None, Claims)),
               "categories": list(filter(None, Categories)),
               "non_claims": list(filter(None, Normal_sentences))
               }
        filename = urlparse(response.request.url).path
        with open(os.path.join("data",filename.replace("/","_")+".json"), 'w') as f:
            json.dump(dic,f)