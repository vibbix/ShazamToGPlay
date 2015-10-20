# ShazamToGplay
This utility helps turn your shazam tags into a play list on Google Play Music All-Access. To get your shazam download history, first login to your shazam account, navigate to shazam.com/myshazam, and then press the downward pointing arrow in the top left hand corner, next your account name. In the menu, press "Download History," and an html file should begin downloading it.

# Requirements
```
python --version
>>> Python 2.7.6 
python -m pip install BeautifulSoup4
>>> ...
python -m pip install gmusicapi
>>> ....
```

# Usage
```
python ShazamToGplay.py -h
>>> usage: ShazamToGplay.py [-h] -email EMAIL -password PASSWORD -file FILE
>>> 
>>> Takes a users shazam download history and puts it into a Google Play Music
>>> All-Access playlist
>>> 
>>> optional arguments:
>>>   -h, --help          show this help message and exit
>>>   -email EMAIL        Email to login to Google Play Music All-Access
>>>   -password PASSWORD  Password to Google account
>>>   -file FILE          location of download history file (HTML file)
>>>   
python ShazamToGplay.py -email="Mark@example.com" -password="PASSWORD" -file="C:\Users\Mark\Desktop\download_history.html"
>>> ...
```
# Bugs
* Running the program from Windows' cmd can cause the app to crash because CMD can't print out unicode variable in some cases.
* Multiple 'Tagged by Shazam' playlists may be created, because autodetection is a little finicky.
* An error for out-of-range index pops up at least once or twice.
* There is almost certainly more, just make a pull request with any additions and I'll try to merge them in!