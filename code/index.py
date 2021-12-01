from typing import Text
from flask import Flask, render_template, request
import pysolr
import urllib.request
from urllib.parse import quote
import json

app = Flask(__name__)

CORE_NAME = "final_proj"
AWS_IP = "3.144.182.191"

@app.route('/')
@app.route('/home')
def home():
    return render_template('first_page.html')


@app.route('/search')
def search():
    print('Inside')
    text =  request.args.get('query')
    # solr = pysolr.Solr('http://'+str(AWS_IP)+':8983/solr/'+str(CORE_NAME))
    print(text)
    query = text.replace(':',r'\:')
    query = quote(query)
    query = query.replace(' ','%20')
    print('query: ',query)
    # inurl = 'http://'+str(AWS_IP)+':8983/solr/'+str(CORE_NAME)+'/select?q='+str(query)+'&fl=id%2Cscore&wt=json&indent=true&defType=dismax&qf=tweet_hashtags^3%20text_en^6%20text_es^6%20text_hi^6%20text_en_copy%20text_es_copy%20text_hi_copy%20tweet_urls^0%20poi_name^100'
    inurl = 'http://'+str(AWS_IP)+':8983/solr/'+str(CORE_NAME)+'/select?q='+str(query)+'&rows=2147483647&defType=dismax&fq=poi_name%3A*&qf=tweet_hashtags^3%20text_en^6%20text_es^6%20text_hi^6%20text_en_copy%20text_es_copy%20text_hi_copy%20tweet_urls^0%20poi_name^100'
    #2147483647
    print(inurl)
    data = urllib.request.urlopen(inurl)
    print(data)
    docs = json.load(data)['response']
    # print('DOCS: ',docs)
    data = docs['docs']
    print('final docs: ',type(data))
    # print(len(docs))
    # for i in range(len(docs)):
    #     print(docs[i])
    return render_template('second_page_new.html', data = data, query = text)


@app.route('/language')
def language():
    print('Inside')
    text =  request.args.get('query')
    lang1 = request.args.get('language')
    lang = ""
    if(lang1 == "Hindi"):
        lang = "text_hi"
    elif(lang1 == "Spanish"):
        lang  = "text_es"
    else:
        lang =  "text_en"

    # solr = pysolr.Solr('http://'+str(AWS_IP)+':8983/solr/'+str(CORE_NAME))
    print(text)
    query = text.replace(':',r'\:')
    query = quote(query)
    query = query.replace(' ','%20')
    print('query: ',query)
    # inurl = 'http://'+str(AWS_IP)+':8983/solr/'+str(CORE_NAME)+'/select?q='+str(query)+'&fl=id%2Cscore&wt=json&indent=true&defType=dismax&qf=tweet_hashtags^3%20text_en^6%20text_es^6%20text_hi^6%20text_en_copy%20text_es_copy%20text_hi_copy%20tweet_urls^0%20poi_name^100'
    inurl = 'http://'+str(AWS_IP)+':8983/solr/'+str(CORE_NAME)+'/select?q='+str(query)+'&rows=2147483647&defType=dismax&fq=poi_name%3A*%20AND%20'+str(lang)+'%3A*&qf=tweet_hashtags^3%20text_en^6%20text_es^6%20text_hi^6%20text_en_copy%20text_es_copy%20text_hi_copy%20tweet_urls^0%20poi_name^100'
    print(inurl)
    data = urllib.request.urlopen(inurl)
    print(data)
    docs = json.load(data)['response']
    # print('DOCS: ',docs)
    data = docs['docs']
    print('final docs: ',type(data))
    # print(len(docs))
    # for i in range(len(docs)):
    #     print(docs[i])
    return render_template('second_page_new.html', data = data, query = text, lang = lang1)

if __name__ == '__main__':
    app.debug=True
    app.run()
