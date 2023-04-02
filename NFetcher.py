import requests
import os
import pickle
import json
import sys
from datetime import datetime

CACHE_FILE = '.cached_pages'

def _handle_api_req_err(data):
    code = data['code']
    if code == 'apiKeyExhausted':
        print('You have exhausted the number of requests for today with this API key', file=sys.stderr)
    if code == 'apiKeyInvalid':
        print('The API key you supplied is invalid', file=sys.stderr)
    if code == 'rateLimited':
        print('The server has rate limited this API key', file=sys.stderr)
    raise Exception('Failed to request to the API, Check your API Key')


class NFetch:
    NEWS_API_ENDPOINT = 'https://newsapi.org/v2/everything'
    NEWS_API_TRENDING = 'https://newsapi.org/v2/top-headlines'

    '''
        @load_cache: bool, decides if we should load from cache on initialization
    '''
    def __init__(self, load_cache=True):
        if 'GNEWS_API_KEY' not in os.environ:
            raise Exception('Unable to find the api key in the enviroment variable')
        self.key = os.environ['GNEWS_API_KEY']
        self.articles = {}
        if load_cache:
            self._load_cache()

    '''
        Use this function to properly exit after the object is used or encoutered an exception
    '''
    def graceful_exit(self):
        self._save_cache()

    '''
        Use this function to manually clear the cache, if you want fresh queries
    '''
    def clear_cache(self):
        if os.path.isfile(CACHE_FILE):
            os.remove(CACHE_FILE)
        self.articles = {}

    # Internal function
    def _load_cache(self):
        if os.path.isfile(CACHE_FILE):
            with open(CACHE_FILE, 'rb') as fd:
                self.articles = pickle.load(fd)

    # Internal function
    def _save_cache(self):
        with open(CACHE_FILE, 'wb') as fd:
            pickle.dump(self.articles, fd)


    # Internal function
    def _search_for_article(self, search, searchIn):
        params = {
            'apiKey': self.key,
            'q': search,
            'searchIn': searchIn
        }

        uniq_key = searchIn + search

        if uniq_key in self.articles and (datetime.now() - self.articles[uniq_key]['queriedAt']).days < 1:
            return self.articles[uniq_key]['articles']

        r = requests.get(NFetch.NEWS_API_ENDPOINT, params=params)
        data = r.json()
        if data['status'] != 'ok' or r.status_code != 200:
            _handle_api_req_err(data)
        
        with_meta = {}
        with_meta['queriedAt'] = datetime.now()
        with_meta['articles'] = data['articles']
        self.articles[uniq_key] = with_meta

        return data['articles']


    '''
        @country: str, 2-letter ISO 3166-1 code of the country
        @general: str, could be one of business, entertainment, general, health, science, sports, technology
    '''
    def fetch_top(self, country='us', category='general'):
        params = {
            'apiKey': self.key,
            'country': country,
            'category': category
        }

        # This checks to make sure the it only fetches from the api if the cache is older than a day.
        if 'top' in self.articles.keys() and (datetime.now() - self.articles['top']['queriedAt']).days < 1:
            return self.articles['top']['articles']

        r = requests.get(NFetch.NEWS_API_TRENDING, params=params)
        data = r.json()
        if data['status'] != 'ok' or r.status_code != 200:
            _handle_api_req_err(data)
        
        with_meta = {}
        with_meta['queriedAt'] = datetime.now()
        with_meta['articles'] = data['articles']
        self.articles['top'] = with_meta
        
        return data['articles']

    '''
        @title_search: str, the string to search for in the title
        @max_num: int, the maximum number of articles to return
    '''
    def search_by_title(self, title_search, max_num=5):
        return self._search_for_article(title_search, 'title')[:max_num]

    '''
        @author_search: str, the substring to look for in author's name from the top news
    '''
    def search_by_author(self, author_search):
        articles = self.fetch_top()
        return filter(lambda article: article['author'] and author_search.lower() in article['author'].lower(), articles)


    '''
        @search: str, the string to search for in the description of a news
        @max_num: int, the maximum number of articles to return
    '''
    def search_for_article(self, search, max_num=5):
        return self._search_for_article(search, 'description')[:max_num]

    '''
        @num: int, the maximum number of articles to return from the top news
    '''
    def fetch_n_top(self, max_num):
        return self.fetch_top()[:max_num]
