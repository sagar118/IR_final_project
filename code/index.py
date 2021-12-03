# from typing import Text
from flask import Flask, render_template, request
import pysolr
import urllib.request
from urllib.parse import quote
import json

app = Flask(__name__)

CORE_NAME = "final_proj"
AWS_IP = "18.191.164.75"

@app.route('/')
@app.route('/home')
def home():
    return render_template('first_page.html')

@app.route('/search')
def search():
    print('Inside')
    text =  request.args.get('query')
    print(text)
    query = text.replace(':','\:')
    query = quote(query)
    query = query.replace(' ','%20')
    print('query: ',query)
    # inurl = 'http://'+str(AWS_IP)+':8983/solr/'+str(CORE_NAME)+'/select?q='+str(query)+'&fl=id%2Cscore&wt=json&indent=true&defType=dismax&qf=tweet_hashtags^3%20text_en^6%20text_es^6%20text_hi^6%20text_en_copy%20text_es_copy%20text_hi_copy%20tweet_urls^0%20poi_name^100'
    # inurl = 'http://'+str(AWS_IP)+':8983/solr/'+str(CORE_NAME)+'/select?q='+str(query)+'&rows=2147483647&defType=dismax&fq=poi_name%3A*&qf=tweet_hashtags^3%20text_en^6%20text_es^6%20text_hi^6%20text_en_copy%20text_es_copy%20text_hi_copy%20tweet_urls^0%20poi_name^100'
    inurl = 'http://'+str(AWS_IP)+':8983/solr/'+str(CORE_NAME)+'/select?q='+str(query)+'&rows=2147483647&defType=dismax&qf=tweet_hashtags^3%20text_en^6%20text_es^6%20text_hi^6%20text_en_copy%20text_es_copy%20text_hi_copy%20tweet_urls^0'
    #2147483647
    print(inurl)
    data = urllib.request.urlopen(inurl)
    print(data)
    docs = json.load(data)['response']
    # print('DOCS: ',docs)
    data = docs['docs']
    poi_data = []
    general_data = []
    poi_tweet_count = 0
    general_tweet_count = 0
    en_count = 0
    es_count = 0
    hi_count = 0
    us_count = 0
    india_count = 0
    mexico_count = 0
    poi_count = {}
    for i in data:
        # print(i)
        # print(type(i))
        if(i["tweet_lang"] == 'es'):
            es_count += 1
        elif(i["tweet_lang"] == 'hi'):
            hi_count += 1
        else:
            en_count += 1
        
        if(i["new_country"] == 'MEXICO'):
            mexico_count += 1
        elif(i["new_country"] == 'INDIA'):
            india_count += 1
        else:
            us_count += 1

        if("poi_name" in i.keys()):
            poi_data.append(i)
            poi_tweet_count += 1
            x = i.get("poi_name")
            if(x in poi_count.keys()):
                poi_count[x] += 1
            else:
                poi_count[x] = 1
        else:
            general_data.append(i)
            general_tweet_count += 1
    if(len(poi_data)>30):
        data = poi_data
    else:
        n = 30 - len(poi_data)
        additional_data = general_data[:n]
        data = poi_data
        data.extend(additional_data)
    print('final docs: ',type(data))
    # print(len(docs))
    # for i in range(len(docs)):
    #     print(docs[i])

    tweet_count_data = [{
        'x': ['POI tweets', 'General population tweets'],
        'y': [poi_tweet_count, general_tweet_count],
        'type': 'bar',
        'marker':{
            'color': ['rgba(185, 30, 32, 1)', 'rgba(78, 94, 248, 1)']
        },
    }]
    
    tweet_lang_data = [{
        'x': ['English', 'Spanish', 'Hindi'],
        'y': [en_count, es_count, hi_count],
        'type': 'bar',
        'marker':{
            'color': ['rgba(185, 30, 32, 1)', 'rgba(78, 94, 248, 1)', 'rgba(27, 171, 35, 0.8)']
        },
    }]

    tweet_country_data = [{
        'x': ['USA', 'Mexico', 'India'],
        'y': [us_count, mexico_count, india_count],
        'type': 'bar',
        'marker':{
            'color': ['rgba(185, 30, 32, 1)', 'rgba(78, 94, 248, 1)', 'rgba(27, 171, 35, 0.8)']
        },
    }]

    poi_name = []
    name_count = []
    for name in poi_count.keys():
        poi_name.append(name)
        c = poi_count.get(name)
        name_count.append(c)
    
    poi_tweet_count = [{
        'x': poi_name,
        'y': name_count,
        'type': 'bar'
    }]

    return render_template('second_page_new.html', data = data, query = text, tweet_count_data = tweet_count_data, tweet_lang_data = tweet_lang_data, tweet_country_data = tweet_country_data, poi_tweet_count = poi_tweet_count)


@app.route('/filtered')
def filtered():
    print('Inside language')
    text =  request.args.get('query')
    lang = request.args.get('language')
    poi_name = request.args.get('POI NAME')
    country = request.args.get('country')
    country_copy = country.upper()
    lang_copy = lang
    poi_name_copy = poi_name

    if(country_copy == 'COUNTRY'or country_copy == None):
        country_copy = ""
    if(poi_name_copy == 'POI name' or poi_name_copy == None):
        poi_name_copy = ""
    if(lang_copy == 'Language' or lang_copy == None):
        lang_copy = ""

    fq = '&fq='
    lang_text = ''
    country_text = ''
    poi_name_text = ''

    if(lang_copy == 'Hindi'):
        lang_copy = 'text_hi'
    elif(lang_copy == 'Spanish'):
        lang_copy  = 'text_es'
    elif(lang_copy == 'English'):
        lang_copy =  'text_en'
    else:
        lang_copy = ''
    
    if(len(lang_copy)):
        lang_text = lang_copy+'%3A*'
    
    if(len(country_copy)):
        country_text = 'new_country%3A'+ country_copy
    
    if(len(poi_name_copy)):
        poi_name_text = 'poi_name%3A' + poi_name_copy
    
    if(lang_text):
        fq += lang_text
    
    if(country_text):
        if(len(fq) > 4):
            fq += '%20AND%20'
        fq += country_text
    
    if(poi_name_text):
        if(len(fq) > 4):
            fq += '%20AND%20'
        fq += poi_name_text
    
    if(len(fq) > 4):
        fq += '&'
    else:
        fq = ''
    print('fq: ',fq)

    # solr = pysolr.Solr('http://'+str(AWS_IP)+':8983/solr/'+str(CORE_NAME))
    print(text)
    query = text.replace(':','\:')
    query = quote(query)
    query = query.replace(' ','%20')
    print('query: ',query)
    # inurl = 'http://'+str(AWS_IP)+':8983/solr/'+str(CORE_NAME)+'/select?q='+str(query)+'&fl=id%2Cscore&wt=json&indent=true&defType=dismax&qf=tweet_hashtags^3%20text_en^6%20text_es^6%20text_hi^6%20text_en_copy%20text_es_copy%20text_hi_copy%20tweet_urls^0%20poi_name^100'
    inurl = 'http://'+str(AWS_IP)+':8983/solr/'+str(CORE_NAME)+'/select?q='+str(query)+'&rows=2147483647&defType=dismax&'+fq+'qf=tweet_hashtags^3%20text_en^6%20text_es^6%20text_hi^6%20text_en_copy%20text_es_copy%20text_hi_copy%20tweet_urls^0%20poi_name^100'
    print(inurl)
    data = urllib.request.urlopen(inurl)
    print(data)
    docs = json.load(data)['response']
    # print('DOCS: ',docs)
    data = docs['docs']
    poi_data = []
    general_data = []
    poi_tweet_count = 0
    general_tweet_count = 0
    en_count = 0
    es_count = 0
    hi_count = 0
    us_count = 0
    india_count = 0
    mexico_count = 0
    poi_count = {}
    for i in data:
        # print(i)
        # print(type(i))
        if(i["tweet_lang"] == 'es'):
            es_count += 1
        elif(i["tweet_lang"] == 'hi'):
            hi_count += 1
        else:
            en_count += 1

        if(i["new_country"] == 'MEXICO'):
            mexico_count += 1
        elif(i["new_country"] == 'INDIA'):
            india_count += 1
        else:
            us_count += 1
        
        if("poi_name" in i.keys()):
            poi_data.append(i)
            poi_tweet_count += 1
            x = i.get("poi_name")
            if(x in poi_count.keys()):
                poi_count[x] += 1
            else:
                poi_count[x] = 1
        else:
            general_data.append(i)
            general_tweet_count += 1
    if(len(poi_data)>30):
        data = poi_data
    else:
        n = 30 - len(poi_data)
        additional_data = general_data[:n]
        data = poi_data
        data.extend(additional_data)
    print('final docs: ',type(data), len(data))
    # print(data)
    # print(len(docs))
    # for i in range(len(docs)):
    #     print(docs[i])

    tweet_count_data = [{
        'x': ['POI tweets', 'General population tweets'],
        'y': [poi_tweet_count, general_tweet_count],
        'type': 'bar',
        'marker':{
            'color': ['rgba(204,204,204,1)', 'rgba(222,45,38,1)']
        },
    }]

    tweet_lang_data = [{
        'x': ['English', 'Spanish', 'Hindi'],
        'y': [en_count, es_count, hi_count],
        'type': 'bar'
    }]

    tweet_country_data = [{
        'x': ['USA', 'Mexico', 'India'],
        'y': [us_count, mexico_count, india_count],
        'type': 'bar'
    }]

    poi_names = []
    name_count = []
    for name in poi_count.keys():
        poi_names.append(name)
        c = poi_count.get(name)
        name_count.append(c)
    
    poi_tweet_count = [{
        'x': poi_names,
        'y': name_count,
        'type': 'bar'
    }]

    return render_template('second_page_new.html', data = data, query = text, lang = lang, poi_name = poi_name, country = country, tweet_count_data = tweet_count_data, tweet_lang_data = tweet_lang_data, tweet_country_data = tweet_country_data, poi_tweet_count = poi_tweet_count)

@app.route('/overview')
def overview():
    f = open('graph_var.json')
    data = json.load(f)
    
    return render_template("overview.html",data=data)

if __name__ == "__main__":
    app.debug=True
    app.run()
