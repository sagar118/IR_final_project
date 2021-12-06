import os
import pysolr
import requests
import json
import pandas as pd

CORE_NAME = "final_proj"
AWS_IP = "18.191.108.186"

def delete_core(core=CORE_NAME):
    print(os.system('sudo su - solr -c "/opt/solr/bin/solr delete -c {core}"'.format(core=core)))

def create_core(core=CORE_NAME):
    # print('hello')
    print(os.system(
        'sudo su - solr -c "/opt/solr/bin/solr create -c {core} -n data_driven_schema_configs"'.format(
            core=core)))
    # print('done')

class Indexer:
    def __init__(self):
        self.solr_url = f'http://{AWS_IP}:8983/solr/'
        self.connection = pysolr.Solr(self.solr_url + CORE_NAME, always_commit=True, timeout=5000000)

    def do_initial_setup(self):
        delete_core()
        create_core()

    def create_documents(self, docs):
        print(self.connection.add(docs))

    def add_fields(self):
        data = {
            "add-field": [
                {
                    "name": "country",
                    "type": "string",
                    "multiValued": False
                }, 
                {
                    "name": "tweet_lang",
                    "type": "string",
                    "required":"true",
                    "multiValued": False
                },
                {
                    "name": "tweet_text",
                    "type": "text_general",
                    "required":"true",
                    "multiValued": False
                },
                {
                    "name": "tweet_date",
                    "type": "pdate",
                    "required":"true",
                    "multiValued": False
                },
                {
                    "name": "text_hi",
                    "type": "text_general",
                    "multiValued": False
                },
                {
                    "name": "text_es",
                    "type": "text_general",
                    "multiValued": False
                },
                {
                    "name": "text_en",
                    "type": "text_general",
                    "multiValued": False
                },
                {
                    "name": "verified",
                    "type": "pfloat",
                    "multiValued": False
                },
                {
                    "name": "poi_id",
                    "type": "plong",
                    "multiValued": False
                },
                {
                    "name": "poi_name",
                    "type": "string",
                    "multiValued": False
                },
                {
                    "name": "replied_to_tweet_id",
                    "type": "plong",
                    "multiValued": False
                },
                {
                    "name": "replied_to_user_id",
                    "type": "plong",
                    "multiValued": False
                },
                {
                    "name": "reply_text",
                    "type": "text_general",
                    "multiValued": False
                },
                {
                    "name": "hashtags",
                    "type": "string",
                    "multiValued": True
                },
                {
                    "name": "mentions",
                    "type": "string",
                    "multiValued": True
                },
                {
                    "name": "tweet_urls",
                    "type": "string",
                    "multiValued": True
                },
                {
                    "name": "tweet_emoticons",
                    "type": "string",
                    "multiValued": True
                },
                {
                    "name": "username",
                    "type": "string",
                    "multiValued": False
                },
                {
                    "name": "new_country",
                    "type": "string",
                    "multiValued": False
                },
                {
                    "name": "vaccine/covid classification",
                    "type": "string",
                    "multiValued": False
                }           
            ]
        }

        print(requests.post(self.solr_url + CORE_NAME + "/schema", json=data).json())


    # def replace_fields(self):
    #     data = {
    #         "replace-field": [
    #             {
    #                 "name": "age",
    #                 "type": "string",
    #                 "multiValued": False
    #             }
    #         ]
    #     }

    #     print(requests.post(self.solr_url + CORE_NAME + "/schema", json=data).json())


    def replace_BM25(self, b=None, k1=None):
        data = {
            "replace-field-type": [
                {
                    'name': 'text_en',
                    'class': 'solr.TextField',
                    'positionIncrementGap': '100',
                    'indexAnalyzer': {
                        'tokenizer': {
                            'class': 'solr.StandardTokenizerFactory'
                        },
                        'filters': [{
                            'class': 'solr.StopFilterFactory',
                            'words': 'lang/stopwords_en.txt',
                            'ignoreCase': 'true'
                        }, {
                            'class': 'solr.LowerCaseFilterFactory'
                        }, {
                            'class': 'solr.EnglishPossessiveFilterFactory'
                        }, {
                            'class': 'solr.KeywordMarkerFilterFactory',
                            'protected': 'protwords.txt'
                        }, {
                            'class': 'solr.PorterStemFilterFactory'
                        }]
                    },
                    'similarity': {
                        'class': 'solr.BM25SimilarityFactory',
                        'b': str(b),
                        'k1': str(k1)
                    },
                    'queryAnalyzer': {
                        'tokenizer': {
                            'class': 'solr.StandardTokenizerFactory'
                        },
                        'filters': [{
                            'class': 'solr.SynonymGraphFilterFactory',
                            'expand': 'true',
                            'ignoreCase': 'true',
                            'synonyms': 'synonyms.txt'
                        }, {
                            'class': 'solr.StopFilterFactory',
                            'words': 'lang/stopwords_en.txt',
                            'ignoreCase': 'true'
                        }, {
                            'class': 'solr.LowerCaseFilterFactory'
                        }, {
                            'class': 'solr.EnglishPossessiveFilterFactory'
                        }, {
                            'class': 'solr.KeywordMarkerFilterFactory',
                            'protected': 'protwords.txt'
                        }, {
                            'class': 'solr.PorterStemFilterFactory'
                        }]
                    }
                }, {
                    'name': 'text_ru',
                    'class': 'solr.TextField',
                    'positionIncrementGap': '100',
                    'analyzer': {
                        'tokenizer': {
                            'class': 'solr.StandardTokenizerFactory'
                        },
                        'filters': [{
                            'class': 'solr.LowerCaseFilterFactory'
                        }, {
                            'class': 'solr.StopFilterFactory',
                            'format': 'snowball',
                            'words': 'lang/stopwords_ru.txt',
                            'ignoreCase': 'true'
                        }, {
                            'class': 'solr.SnowballPorterFilterFactory',
                            'language': 'Russian'
                        }]
                    },
                    'similarity': {
                        'class': 'solr.BM25SimilarityFactory',
                        'b': str(b),
                        'k1': str(k1)
                    },
                }, {
                    'name': 'text_de',
                    'class': 'solr.TextField',
                    'positionIncrementGap': '100',
                    'analyzer': {
                        'tokenizer': {
                            'class': 'solr.StandardTokenizerFactory'
                        },
                        'filters': [{
                            'class': 'solr.LowerCaseFilterFactory'
                        }, {
                            'class': 'solr.StopFilterFactory',
                            'format': 'snowball',
                            'words': 'lang/stopwords_de.txt',
                            'ignoreCase': 'true'
                        }, {
                            'class': 'solr.GermanNormalizationFilterFactory'
                        }, {
                            'class': 'solr.GermanLightStemFilterFactory'
                        }]
                    },
                    'similarity': {
                        'class': 'solr.BM25SimilarityFactory',
                        'b': str(b),
                        'k1': str(k1)
                    },
                }
            ]
        }

        print(requests.post(self.solr_url + CORE_NAME + "/schema", json=data).json())


if __name__ == "__main__":
    i = Indexer()
    # i.do_initial_setup()

    # print('Core created')
    # i.add_fields()
    # print('Fields added')

    f = open("final_data5.json","r", encoding='utf8')
    # print('opening file')
    data = json.load(f)
    # print('Data loaded')
    i.create_documents(data)
    # print('Done')