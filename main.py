import spotipy
import os
import math
import csv
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np

#ENVIRON SETUP + CONSTANTS
f = open("BPMkeys.txt", "r")
cid = f.readline().split('\n')[0]
secret = f.readline().split('\n')[0]
auth = f.readline().split('\n')[0]
f.close()

os.environ['SPOTIPY_CLIENT_ID'] = cid
os.environ['SPOTIPY_CLIENT_SECRET'] = secret

polyurl = 'spotify:playlist:61Pqpnx6Nz57snNE3mVnRH'
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

COUNT = 0
PLAYLIST = []
#Each entry in PLAYLIST should be a dict with {'name':,'artist':,'id':,'tempo':}

#FUNCTIONS
def getPlaylist(sp, polyurl):
	#Load the PLAYLIST variable with all songs name,artist, and id from the desired playlist polyurl 
	#Max limit is 100 per query, so loop the query and increase the offset each time
	offset = 0
	songdict = {}
	results = []
	while(len(results)<1427):
		songs = sp.playlist_items(polyurl,offset = offset)
		results_new = songs['items']
		for res in results_new:
			results.append(res)
		offset = offset + 100

	for i in range(len(results)):
		songname = results[i].get('track').get('name')
		songid = results[i].get('track').get('id')
		songfirstartist = results[i].get('track').get('artists')[0].get('name')

		songdict = {'name':songname,'artist':songfirstartist,'id':songid}
		print(songdict)
		PLAYLIST.append(songdict)

def getPlaylistTempo(sp):
	#Load PLAYLIST variable full of tempo data (i.e, BPMs)
	#MAX queries is 100, do in bulk to avoid a billion quieries to spotify.
	playlistids = [] #make as many lists of 100 ids as need be to cover PLAYLIST
	tempolist = []
	for n in range(math.ceil(len(PLAYLIST)/100)):
		newlist = []
		for m in range(100):
			if(len(PLAYLIST)-1 < n*100 + m):
				break
			nextid = PLAYLIST[n*100 + m].get('id')
			newlist.append(nextid)
		playlistids.append(newlist)
		
	for i in range(len(playlistids)):
		#Query in 100-batch
		songfeat = sp.audio_features(playlistids[i])
		for j in range(100):
			if(len(songfeat)-1 < j):
				break
			tempo = songfeat[j].get('tempo')
			tempolist.append(tempo)

	i = 0
	for tempo in tempolist:
		#now add it into PLAYLIST dict
		PLAYLIST[i]['tempo'] = tempo
		i = i + 1

def savePlaylist():
	with open('playlist.csv', 'w', encoding='utf8', newline='') as output_file:
	    fc = csv.DictWriter(output_file, 
	                        fieldnames=PLAYLIST[0].keys(),

	                       )
	    fc.writeheader()
	    fc.writerows(PLAYLIST)

def getTempo(sp,ident):
	songfeat = sp.audio_features(ident)
	tempo = songfeat[0].get('tempo')
	return tempo



#MAIN
if __name__ == '__main__':

	#Initialize DataFile playlist.csv
	#getPlaylist(sp, polyurl)
	#getPlaylistTempo(sp)
	#savePlaylist()
	#print(f"Your playlist has {len(PLAYLIST)} songs.")

	#Verify tempo correctness
	#testsong = "We Are the Winx"
	#ident = "62DhR27lWUHYHuD9A3zSrB"
	#print(f"song: {testsong} has {getTempo(sp,ident)} tempo")

	#Load playlist.csv Datafile
	df = pd.read_csv('playlist.csv')
	print(df.head())
	



