# LightOJ Code Downloader

By this code, you can download your all accepted solutions from lightoj overnight.

### Prerequisites

python 3, selenium, urllib

### Installing

First install python 3.6  
Install [pip](https://pip.pypa.io/en/stable/installing/)  
git clone this repository  
Then go the folder from command line  

```
sudo pip install -r requirements.txt
```

It will install all of the library needed.  
Then run this command to give permission to chrome driver (Linux & Mac only)  

```
sudo chmod 777 chromedriver_linux [for Linux]
sudo chmod 777 chromedriver_mac [for Mac]
```
Then,  

```
1. Just run "python lightoj-downloader.py" file on your terminal
2. Give your username and password
```

And,

```
3. Go for a coffee or workout
4. Coming home you will see all your accepted codes in a structerd way :) 
```
## Features:

* Download all your accepted codes from lightoj
* You can solve more, and the next time you run this, it will just resume the download
* All solutions will be arranged in a structured way 

## Built With

* [Python](http://www.dropwizard.io/1.0.2/docs/) - The main platform
* [urllib](https://docs.python.org/2/library/urllib.html) - To get data from Codeforces API
* [Selenium](http://selenium-python.readthedocs.io/installation.html) - Used to get the source code

## Authors

* **Shubhashis Roy Dipta** - *Initial work* - [dipta007](https://github.com/dipta007)
