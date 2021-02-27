import logging.config
import os
import urllib
from urllib.parse import urlparse
from configparser import ConfigParser
from os.path import dirname
import re

import requests


class BaseClass(object):
    logconfig = logging.getLogger(__name__)

    def get_path(self, path_param):
        try:
            requiredpath = os.path.join(dirname(dirname(__file__)), path_param)
            return requiredpath
        except IOError as e:
            self.logconfig.error("Required Directory / File not found")
            self.logconfig.error(e)

    def parser_object(self):
        # Parse object to read parser data from config.ini
        parser = ConfigParser()
        parser.read(self.get_path('Data.ini'))
        return parser

    def get_config(self, section, key):
        # Get parser configurations
        parser = self.parser_object()
        data = parser.get(section, key)
        return data

    def save_media(self,res,filename):
        if "extended_entities" in res:
            link = re.sub(r'.mp4.*', ".mp4", res["extended_entities"]["media"][0]['video_info']['variants'][0]['url'])
            file_name = link.split('/')[-1]
            self.logconfig.info("Downloading file:%s" % file_name)
            # create response object
            r = requests.get(link, stream=True)
            # download started
            with open(os.path.join(os.path.join(dirname(dirname(__file__)), filename) ,filename+'.mp4'), 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            self.logconfig.info("%s downloaded!\n" % file_name)
        else:
            self.logconfig.error("There is no video file to download")

    def verify_alphanumeric(self,tweet):
        tweet_list = tweet.split(" ")

        for index, word in enumerate(tweet_list):
            if not word.isalnum():
                tweet_list[index] = urllib.parse.quote(word)
        encoded_tweet = ' '.join(tweet_list)
        return encoded_tweet

    def get_id_from_Url(self,url):
        id = url.split("/")[-1]
        return id
