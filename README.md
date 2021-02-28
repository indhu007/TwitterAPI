# Twitter API Automation using Pytest



## Setup & installation

If you run into any issues with the steps below, please let me know at [indhumathimohanraj07@gmail.com](mailto:indhumathimohanraj07@gmail.com).

**Prerequisite**

1. Install Python 3.6 or higher

2. Download this repository by Clone or download button at the top.

3. Change directory to the downloaded folder and install requirements.txt (`pip install -r requirements.txt`)

4. If Pycharm is the choice of IDE, 

   ​	a. Mac users navigate to Preferences->Tools->Python Integrated Tools  and set Default test runner to pytest

   ​    b. Windows users navigate to File->Settings->Tools->Python Integrated Tools  and set Default test runner to pytest
   
   
## Framework Setup

Twitter -> utils->BaseClass - Contains generic methods to be used

Twitter -> utils->email_pytest_report - Contains methods for test report which will be emailed after the execution

Twitter -> utils->utils_tweet - Contains API methods 

Twitter -> Tests ->test_tweet - Contains testcase to create/destroy a tweet or retweet

Twitter -> Tests ->test_old_tweet - Contains testcases to store the info of given tweet and verify the store info
Twitter -> Data ->email_config - Contains username and password to set up email host (https://support.google.com/mail/answer/7126229?p=BadCredentials&visit_id=637500974502836932-3731741576&rd=2#cantsignin) and to email to which report has to be sent

Twitter -> Data ->Tweet_Data - Contains Tweet message for test_tweet
Twitter -> conftest - Contains functions for logging and email test report

Twitter -> Data.ini - Contains Authorization data and existing tweet’s url for `test_old_tweet`

Twitter -> Pytest.ini - Contains logging level and format



## **Running tests**

After setup and installations,

Run a test using this command 

```
pytest --capture=no --verbose --html=pytest_report.html --email_pytest_report Y --self-contained-html --capture=sys
```

**Note** : The **pytest**-**dependency** module is  applied to tests. So, if the creation of tweet tests fails, the remaining tests dependent on this test will not be executed and marked as skipped in test report




## **Test Reports**

Verify test reports after the execution from Twitter/pytest_report.html. Th same report willed be emailed as per the configuration values for recipient emails in Twitter/Data/email_config file. 



## Logging

While execution, the logs will be shown in the console with the date and time. And, at the end of execution, the same log information will also be stored as a text file with date and time in the name of the file. The log will be stored even if the test fail and the execution is terminated.
