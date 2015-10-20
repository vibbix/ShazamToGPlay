__version__ = "0.0.1"
#For use with Python 2.7, as gmusicapi has no support for 3.0
#will eventually make 
from gmusicapi import Mobileclient
from bs4 import BeautifulSoup
import argparse
import os.path
api = Mobileclient()
#verify the file
#http://stackoverflow.com/questions/11540854/file-as-command-line-argument-for-argparse-error-message-if-argument-is-not-va
def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle

#argparser things
parser = argparse.ArgumentParser(description="Takes a users shazam download history" + \
                                 " and puts it into a Google Play Music All-Access playlist")
parser.add_argument("-email", dest="email",type=str,  required=True, help="Email to login to Google Play Music All-Access")
parser.add_argument("-password",dest="password", type=str, required=True, help="Password to Google account")
parser.add_argument("-file", dest="file", type=lambda x: is_valid_file(parser, x), required=True, metavar="FILE", help="location of download history file (HTML file)")

#playlist search
#returns "0" if nothing found
def searchforsong(title, artist):
	if len(artist) < 1 or len(title) < 1:
		print "Bad artist or song name"
		return "0"
	title = title.lower()
	artist = artist.lower()
	if artist == "various artists":
                if title == "unknown":
                        print 'Unknown Title and artist'
                        return "0"
                print "Various Artists is just a placeholder, skipping over song: " + title
                return "0"
	s1 = api.search_all_access(title + " " + artist, 10)
	for song in s1["song_hits"]:
		if (song["track"]["title"].lower() == title) and \
		(song["track"]["artist"].lower() == artist):
			return song["track"]["nid"]
	#attempt 2
	#Removes "feat" from artist and title
	aa = artist
	try:
		artist = artist.split("feat")[0]
	except:
		artist = aa
	tt = title
	try:
		title = title.split("feat")[0]
	except:
		title = tt
	s2 = api.search_all_access(title + " " + artist, 10)
	for song in s2["song_hits"]:
		if ((song["track"]["title"].lower() == title) and \
		(song["track"]["artist"].lower() == artist)) or \
		song["score"] > 100:
			return song["track"]["nid"]
	#attempt #3
	#removes, "edit", "remix" and parentheses
	artist = artist.replace("(", "").replace(")", "").replace("edit", "").replace("remix", "")
	title = title.replace("(", "").replace(")", "").replace("edit", "").replace("remix", "")
	s3 = api.search_all_access(title + " " + artist, 10)
	for song in s3["song_hits"]:
		if ((song["track"]["title"].lower() == title) and \
		(song["track"]["artist"].lower() == artist)) or \
		song["score"] > 100:
			return song["track"]["nid"]
	print "Couldn't find " + title + " by " + artist
	return "0"

def main():
        args = parser.parse_args()
        #print args
        loginresult = api.login(args.email, args.password, Mobileclient.FROM_MAC_ADDRESS)
        if not loginresult:
                print "Bad username or password"
                return
        shazamhtml = args.file
        htmltree = shazamhtml.read()
        soup = BeautifulSoup(htmltree, 'html.parser')
        table = soup.find('table')
        table_rows = table.findAll('tr')
        data = []
        for row in table_rows:
                #Empty row may break, catch exception
                try:
                        cols = row.find_all('td')
                        d = {}
                        d["Title"] = cols[0].text.strip()
                        d["TrackID"] = ""
                        d["Artist"] = cols[1].text
                        if not(d in data):
                                data.append(d)
                except Exception as ex:
                        print "Error parsing table row: " + ex.message
                        
        #now that we have everything
        playlists = api.get_all_user_playlist_contents()
        slist = 0
        shazamplaylist = ""
        isnew = False
        for i in range (0, len(playlists)-1):
                if playlists[i]["name"] == "Tagged by Shazam":
                        shazamplaylist = playlists[i]["id"]
                        slist = i
                        print "Found existing playlist"
                        break
        if shazamplaylist == "":
                shazamplaylist = api.create_playlist("Tagged by Shazam", "Songs tagged by Shazam", public = False)
                print "Creating new Playlist"
                isnew = True
        #Get all song id's
        songs = []
        for i in range (0, len(data)):
                try:
                        song = data[i]
                except Exception as ex:
                        print "Error at i = " + str(i) + ":" + ex.message
                        continue
                nid = searchforsong(song["Title"], song["Artist"])
                if nid == "0":
                        data.pop(i)
                else:
                        songs.append(nid)
        #Check for preexising songs
        if not isnew:
                xlists = playlists[slist]["tracks"]
                for track in xlists:
                        if track["trackId"] in songs:
                                songs.remove(track["trackId"])
                songs = filter(None, songs)
        #add songs to playlist
        print "Adding " + str(len(songs)) + " to playlist"
        response = api.add_songs_to_playlist(shazamplaylist, songs)
        
if __name__ == "__main__":
    main()
