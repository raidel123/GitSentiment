# GitSentiment

Study based on [ Sentiment analysis of commit comments in GitHub: an empirical study ](https://dl.acm.org/citation.cfm?id=2597118)

## Requirements
* [ Python 2.x ](https://www.python.org/downloads/release/python-2714/)
* [ Virtualenv ](https://virtualenv.pypa.io/en/stable/installation/)
* [ MongoDB ](https://pypi.org/project/pymongo/)
* [ SQLite3 ]

## Description of directories
### docs
#### Holds the different documents that are related to our project.
### emotionsStats
#### Holds the manipulation of our SQL table to find the paper's research questions.
### repoAnalysis
#### Holds the analysis of repositories such as LINTing to answer our additional research question.
### sentimentAnalysis
#### Holds the sentiment analysis module and the creation of the SQL table to carry out the rest of the project.
### test
#### Holds our JSON objects for intermittent data changes.
### utils
#### Various tools for processing of data.

## Installation
#### Setting up the virtual environment
Creating and Activating
```
    $ virtualenv venv
    $ source venv/bin/activate
```
Deactivating (after executing program)
```
    $ deactivate
```
#### Installation Requirements
```
    $ pip install -r requirements.txt
```

## Database Setup/Download
[ MSR 2014 Mining Challenge Dataset ](http://ghtorrent.org/msr14.html)
* perform these operations within the main repo directory, it should create a dump directory
```
    $ wget http://ghtorrent-downloads.ewi.tudelft.nl/datasets/msr14-mongo.tar.gz
    $ tar zxvf msr14-mongo.tar.gz
```
[ MongoDB database dump ](http://ghtorrent-downloads.ewi.tudelft.nl/datasets/msr14-mysql.gz) (if wget command above doesn't work)

## Run
```
    $ python gitSentiment.py
```
## Other functionality
If you want to run the repoAnalysis, you must have the latest version of [node](https://nodejs.org/en/download/package-manager/), and you must install the JS linter via `npm install -g standard --save-devsour`. For all dependencies (assuming npm and pip on system), just run `./install.sh`

