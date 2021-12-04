# from typing import Text
from flask import Flask, render_template, request
import pysolr
import urllib.request
from urllib.parse import quote
import json

app = Flask(__name__)

CORE_NAME = "final_proj"
AWS_IP = "3.138.141.215"

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
    poi_tweet_count = 0
    general_tweet_count = 0
    en_count = 0
    es_count = 0
    hi_count = 0
    us_count = 0
    india_count = 0
    mexico_count = 0
    poi_count = {}
    display = []
    display_poi = []
    display_general = []
    for i in data:
        # print(i)
        # print(type(i))
        tweet_of_poi = 0
        display_text = ''
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
            tweet_of_poi = 1
            poi_tweet_count += 1
            x = i.get("poi_name")
            if(x in poi_count.keys()):
                poi_count[x] += 1
            else:
                poi_count[x] = 1
            if(i["twitter_url"] != 'NaN'):
                display_text += '<a href=\"'
                display_text += i.get("twitter_url")
                display_text += '\">'
                display_text += x
                display_text += '</a>'
            else:
                display_text += x
        else:
            general_tweet_count += 1
            username = 'Twitter User'
            if("username" in i.keys()):
                username = i.get("username")
            if(i["twitter_url"] != 'NaN'):
                display_text += '<a href=\"'
                display_text += i.get("twitter_url")
                display_text += '\">'
                display_text += username
                display_text += '</a>'
            else:
                display_text += str(username)
        
        if(i.get("verified")):
            display_text += '''<img src=\"/static/verified.png\" height=\"15\"><br/>'''
        tweet_text = i.get("tweet_text")
        display_text += tweet_text
        display_text += '<br/>'
        if("tweet_urls" in i.keys()):
            urls = i.get("tweet_urls")
            for url in urls:
                if(url[-1] != '/'):
                    display_text += '<a href=\"'
                    display_text += url
                    display_text += '\">'
                    display_text += url
                    display_text += '</a>'
                    display_text += '<br/>'
        if("tweet_sentiment_sentiment" in i.keys() and "tweet_sentiment_proba" in i.keys()):
            display_text += 'Tweet Sentiment: '
            display_text += i.get("tweet_sentiment_sentiment")
            display_text += '<br/>'
            display_text += 'Sentiment Probability: '
            display_text += str(i.get("tweet_sentiment_proba"))
            display_text += '<br/>'
        if("reply_Positive_text" in i.keys()):
            display_text += 'Best Positive reply: '
            display_text += i.get("reply_Positive_text")
            display_text += '<br/>'
        if("reply_negative_text" in i.keys()):
            display_text += 'Best Negative reply: '
            display_text += i.get("reply_negative_text")
            display_text += '<br/>'
        if(tweet_of_poi):
            display_poi.append(display_text)
        else:
            display_general.append(display_text)
    
    if(len(display_poi)>30):
        display = display_poi
    else:
        n = 30 - len(display_poi)
        additional_data = display_general[:n]
        display = display_poi
        display.extend(additional_data)
    # print('final docs: ',type(display))
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

    return render_template('second_page_new.html', data = display, query = text, tweet_count_data = tweet_count_data, tweet_lang_data = tweet_lang_data, tweet_country_data = tweet_country_data, poi_tweet_count = poi_tweet_count)


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
    poi_tweet_count = 0
    general_tweet_count = 0
    en_count = 0
    es_count = 0
    hi_count = 0
    us_count = 0
    india_count = 0
    mexico_count = 0
    poi_count = {}
    display = []
    display_poi = []
    display_general = []
    for i in data:
        # print(i)
        # print(type(i))
        tweet_of_poi = 0
        display_text = ''
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
            tweet_of_poi = 1
            poi_tweet_count += 1
            x = i.get("poi_name")
            if(x in poi_count.keys()):
                poi_count[x] += 1
            else:
                poi_count[x] = 1
            if(i["twitter_url"] != 'NaN'):
                display_text += '<a href=\"'
                display_text += i.get("twitter_url")
                display_text += '\">'
                display_text += x
                display_text += '</a>'
            else:
                display_text += x
        else:
            general_tweet_count += 1
            username = 'Twitter User'
            if("username" in i.keys()):
                username = i.get("username")
            if(i["twitter_url"] != 'NaN'):
                display_text += '<a href=\"'
                display_text += i.get("twitter_url")
                display_text += '\">'
                display_text += username
                display_text += '</a>'
            else:
                display_text += str(username)
        
        if(i.get("verified")):
            display_text += '''<img src=\"/static/verified.png\" height=\"15\"><br/>'''
        tweet_text = i.get("tweet_text")
        display_text += tweet_text
        display_text += '<br/>'
        if("tweet_urls" in i.keys()):
            urls = i.get("tweet_urls")
            for url in urls:
                if(url[-1] != '/'):
                    display_text += '<a href=\"'
                    display_text += url
                    display_text += '\">'
                    display_text += url
                    display_text += '</a>'
                    display_text += '<br/>'
        if("tweet_sentiment_sentiment" in i.keys() and "tweet_sentiment_proba" in i.keys()):
            display_text += 'Tweet Sentiment: '
            display_text += i.get("tweet_sentiment_sentiment")
            display_text += '<br/>'
            display_text += 'Sentiment Probability: '
            display_text += str(i.get("tweet_sentiment_proba"))
            display_text += '<br/>'
        if("reply_Positive_text" in i.keys()):
            display_text += 'Best Positive reply: '
            display_text += i.get("reply_Positive_text")
            display_text += '<br/>'
        if("reply_negative_text" in i.keys()):
            display_text += 'Best Negative reply: '
            display_text += i.get("reply_negative_text")
            display_text += '<br/>'
        if(tweet_of_poi):
            display_poi.append(display_text)
        else:
            display_general.append(display_text)
    
    if(len(display_poi)>30):
        display = display_poi
    else:
        n = 30 - len(display_poi)
        additional_data = display_general[:n]
        display = display_poi
        display.extend(additional_data)
    # print(data)
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

    return render_template('second_page_new.html', data = display, query = text, lang = lang, poi_name = poi_name, country = country, tweet_count_data = tweet_count_data, tweet_lang_data = tweet_lang_data, tweet_country_data = tweet_country_data, poi_tweet_count = poi_tweet_count)

@app.route('/overview')
def overview():
    f = open('./graph_var.json')
    data = json.load(f)
    
    return render_template("overview.html",data=data)

@app.route('/poi_analysis')
def poi_analysis():
    f = open('./poi_graph.json')
    poi_data = json.load(f)

    f = open('./graph_var.json')
    graph_data = json.load(f)

    f = open('./country_poi.json')
    country_poi = json.load(f)
    
    return render_template("poi_analysis.html",poi_data=poi_data,graph_data=graph_data,country_poi=country_poi)

if __name__ == "__main__":
    app.debug=True
    app.run()
