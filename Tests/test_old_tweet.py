from os.path import dirname
import pytest
import logging
from Utils.utils_tweets import Tweets
import os



class Test_OldTweet(Tweets):
    logger_test = logging.getLogger(__name__)
    id = "1257326183101980673"

    parent_dir = dirname(dirname(__file__))
    path = os.path.join(parent_dir, id)
    filename = id + '.txt'

    @pytest.fixture(scope="module")
    def create_data(self):
        try:
            os.makedirs(self.path, exist_ok=True)

            url = str(self.get_config('Tweet Url','Url'))
            type(self).id = self.get_id_from_Url(url)

            response = self.get_tweet_status(self.id)
            res = response.json()
            self.save_media(res,self.id)

            response = self.get_retweeter_id(self.id)
            twitter_ids = response.json()

            with open(os.path.join(self.path, self.filename), 'w+') as tweetsfile:
                tweetsfile.write("Content: {}\n".format(res.get("full_text")))
                tweetsfile.write("RetweetCount: {} \n".format(res.get("retweet_count")))
                tweetsfile.write("ReTwittersids: {}".format(twitter_ids.get("ids")))

        except OSError as error:
            print(error)

    def test_tweet_content(self,create_data):
        response = self.get_tweet_status(self.id)
        res = response.json()
        assert response.status_code == 200 , self.logger_test.error(res.get("error"))

        assert res.get("id") == int(self.id), "Id in the response is not matching the Id of the query"
        with open(os.path.join(self.path,self.filename), 'r') as tweetsfile:
            contents = tweetsfile.read()
            content = contents.split('RetweetCount:', 1)[0]
        assert res.get("full_text") == (content.split(" ",1)[1]).rstrip("\n") , self.logger_test.error("Content stored and value in text does not match. check the id of the tweet")

    def test_retweet_count(self):
        response = self.get_tweet_status(self.id)
        res = response.json()
        assert response.status_code == 200, self.logger_test.error(res.get("error"))

        assert res.get("id") == int(self.id), self.logger_test.error("Id in the response is not matching the Id of the query")
        with open(os.path.join(self.path, self.filename), 'r') as tweetsfile:
            for line in tweetsfile:
                if 'RetweetCount' in line:
                    content = line.split(' ', 1)[1]
                    break
        Retweet_Count = str(res.get("retweet_count"))
        assert Retweet_Count == content.rstrip(" \t\n\r"), self.logger_test.error("Retweet Count is not matching with the response> check the ID of the tweet")

    def test_retweet_id(self):
        response = self.get_retweeter_id(self.id)
        twitter_ids = response.json()
        assert response.status_code == 200, self.logger_test.error(twitter_ids.get("error"))
        with open(os.path.join(self.path, self.filename), 'r') as tweetsfile:
            for line in tweetsfile:
                if 'Twittersids' in line:
                    content = line.split(' ', 1)[1]
                    break
        assert str(twitter_ids.get("ids")) == content.rstrip("\n"), self.logger_test.error("Retwiteeters ID's are not matching with the response> check the ID of the tweet")






