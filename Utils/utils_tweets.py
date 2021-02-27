import pytest
import requests
from requests_oauthlib import OAuth1
from Utils.BaseClass import BaseClass
import logging

class Tweets(BaseClass):
    loginfo = logging.getLogger(__name__)

    Base_url = 'https://api.twitter.com/1.1/statuses'
    def get_auth(self):
        return OAuth1(
                 self.get_config('Authorization','consumer_key'),self.get_config('Authorization','consumer_secret') ,
                 self.get_config('Authorization','access_token'),self.get_config('Authorization','token_secret')
                  )

    def create_tweet(self,tweets):
        try:
            url = self.Base_url +'/update.json?status=' + tweets
            response = requests.post(url, auth=self.get_auth())
            return response
        except Exception as e:
            self.loginfo.error(str(e))

    def retweet(self,id):
        try:
            url = self.Base_url +'/retweet/'+ id + '.json'
            response = requests.post(url, auth=self.get_auth())
            return response
        except Exception as e:
            self.loginfo.error(str(e))

    def unretweet(self,id):
        try:
            url = self.Base_url +'/unretweet/'+id+'.json'
            response = requests.post(url, auth=self.get_auth())
            return response
        except Exception as e:
            self.loginfo.error(str(e))

    def delete_tweet(self,id):
        try:
            url = self.Base_url +'/destroy/' + id + '.json'
            response = requests.post(url, auth=self.get_auth())
            return response
        except Exception as e:
            self.loginfo.error(str(e))

    def get_tweet_status(self,id):
        try:
            url = self.Base_url +'/show.json?id='+ id + '&include_entities=true&tweet_mode=extended'
            response = requests.get(url, auth=self.get_auth())
            return response
        except Exception as e:
            self.loginfo.error(str(e))

    def get_retweeter_id(self,id):
        try:
            url = self.Base_url +'/retweeters/ids.json?id='+ id
            response = requests.get(url, auth=self.get_auth())
            return response
        except Exception as e:
            self.loginfo.error(str(e))

