import logging.config
import os
import urllib
from urllib.parse import urlparse
from configparser import ConfigParser
from os.path import dirname
from pathlib import Path
import re

import requests


class BaseClass(object):

    project_path = Path(__file__).parents[2]
    print("PAth" + str(project_path))
    log_path = project_path / 'logs'
    if not (Path(log_path).exists()):
        Path(log_path).mkdir(mode=0o777, parents=False, exist_ok=False)
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)-50s [%(levelname)8s] %(message)s',
        datefmt='%m-%d %H:%M',
        filename=str(log_path) + '/app.log',
        filemode='w'
    )
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger().addHandler(console)
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
        link = re.sub(r'.mp4.*', ".mp4", res["extended_entities"]["media"][0]['video_info']['variants'][0]['url'])
        file_name = link.split('/')[-1]
        print("Downloading file:%s" % file_name)
        # create response object
        r = requests.get(link, stream=True)
        # download started
        with open(os.path.join(os.path.join(dirname(dirname(__file__)), filename) ,filename+'.mp4'), 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
        print("%s downloaded!\n" % file_name)
        print("All videos downloaded!")

    def verify_alphanumeric(self,tweet):
        tweet_list = tweet.split(" ")

        for index, word in enumerate(tweet_list):
            if not word.isalnum():
                tweet_list[index] = urllib.parse.quote(word)
        encoded_tweet = ' '.join(tweet_list)
        return encoded_tweet
