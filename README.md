# GitSentiment

Study based on [ Sentiment analysis of commit comments in GitHub: an empirical study ](https://dl.acm.org/citation.cfm?id=2597118)

## Requirements
* [ Python 2.x ](https://www.python.org/downloads/release/python-2714/)
* [ Virtualenv ](https://virtualenv.pypa.io/en/stable/installation/)
* [ MongoDB ](https://pypi.org/project/pymongo/)

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
#### Installing Requirements
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
[ MongoDB database dump ](http://ghtorrent-downloads.ewi.tudelft.nl/datasets/msr14-mysql.gz) (if commands above do not work)

## Run
```
    $ python bsonparser.py
```
