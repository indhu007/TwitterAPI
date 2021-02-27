import pytest
import logging
from Utils.utils_tweets import Tweets
from Data import tweet_data


class TestTweet(Tweets):
    logger_test = logging.getLogger(__name__)
    tweet_id = "1365180241799303171"
    retweet_id = "1365179165247344642"
    retweetcount = 1
    retweeter_id = 1260894064603467777
    tweet_text = ""


    @pytest.mark.parametrize("Tweet",tweet_data.Tweet)
    @pytest.mark.dependency(name="tweet")
    def test_create_tweet(self, Tweet):
        tweets = self.verify_alphanumeric(Tweet)
        response = self.create_tweet(tweets)
        res = response.json()
        assert response.status_code == 200 , self.logger_test.error(res.get("errors"))
        self.logger_test.info(res)

        type(self).tweet_id = str(res.get("id"))
        assert res.get("text") == Tweet, self.logger_test.error("Tweeted value is not text inputted")
        type(self).tweet_text = res.get("text")

    @pytest.mark.dependency(depends=["tweet"])
    @pytest.mark.dependency(name="retweet")
    def test_retweet(self):
        response = self.retweet(self.tweet_id)
        res = response.json()
        assert response.status_code == 200, self.logger_test.error(res.get("errors"))

        assert res.get("retweeted_status").get("text") == self.tweet_text
        assert res.get("retweeted_status").get("id") == self.tweet_id
        type(self).retweet_id = str(res.get("id"))
        type(self).retweetcount = res.get("retweet_count")
        type(self).retweeter_id = res.get("user").get("id")
        print(type(self).retweet_id)

    @pytest.mark.dependency(depends=["retweet"])
    def test_count_retweet(self):
        response = self.get_tweet_status(self.tweet_id)
        res = response.json()
        assert response.status_code == 200, self.logger_test.error(res.get("errors"))

        assert self.retweetcount == res.get("retweet_count")

    @pytest.mark.dependency(depends=["retweet"])
    def test_retweeter_id(self):
        response = self.get_retweeter_id(self.tweet_id)
        res = response.json()
        assert response.status_code == 200, self.logger_test.error(res.get("errors"))

        assert self.retweeter_id in res.get("ids")

    @pytest.mark.dependency(depends=["retweet"])
    def test_unretweet(self):

        #Delete the retweet
        response = self.unretweet(self.retweet_id)
        res = response.json()
        assert response.status_code == 200, self.logger_test.error(res.get("errors"))

        #Check the retweet count after deleting the retweet
        response = self.get_tweet_status(self.tweet_id)
        res = response.json()
        assert response.status_code == 200, self.logger_test.error(res.get("errors"))
        assert (self.retweetcount - 1) == res.get("retweet_count")

        #Check the re-twitter id is removed
        response = self.get_retweeter_id(self.tweet_id)
        res = response.json()
        assert response.status_code == 200, self.logger_test.error(res.get("errors"))
        assert self.retweeter_id not in res.get("ids")

    @pytest.mark.dependency(depends=["tweet"])
    def test_delete_tweet(self):
        response = self.delete_tweet(self.tweet_id)
        res = response.json()
        assert response.status_code == 200, self.logger_test.error(res.get("errors"))


