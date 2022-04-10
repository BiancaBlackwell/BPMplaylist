import spotipy
import fitbit
import os
import math
import csv
from datetime import datetime, timedelta
from fitbit import gather_keys_oauth2 as Oauth2 #Had to copy/paste the gather_keys_oauth2.py into the fitbit folder
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#ENVIRON SETUP + CONSTANTS
f = open("BPMkeys.txt", "r")
#Spotify First
cid_sp = f.readline().split('\n')[0]
secret_sp = f.readline().split('\n')[0]
auth_sp = f.readline().split('\n')[0]

#Fitbit Second
cid_fb = f.readline().split('\n')[0]
secret_fb = f.readline().split('\n')[0]

f.close()

os.environ['SPOTIPY_CLIENT_ID'] = cid_sp
os.environ['SPOTIPY_CLIENT_SECRET'] = secret_sp

polyurl = 'spotify:playlist:61Pqpnx6Nz57snNE3mVnRH' #Master Playlist URL
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
	with open('playlist_master.csv', 'w', encoding='utf8', newline='') as output_file:
	    fc = csv.DictWriter(output_file, 
	                        fieldnames=PLAYLIST[0].keys(),

	                       )
	    fc.writeheader()
	    fc.writerows(PLAYLIST)

def getTempo(sp,ident):
	songfeat = sp.audio_features(ident)
	tempo = songfeat[0].get('tempo')
	return tempo

def playlistAnalysis(df):
	#Graph BPM Information about given playlist
	temp = df[['name','tempo']]
	temp = temp.sort_values('tempo',ignore_index=True)
	temp['row_no'] = temp.index
	temp.plot(x = 'tempo', y = 'row_no', kind = 'scatter')
	plt.show()
	print(temp)
	temp.to_csv('sorted.csv',index=False)	

def fitbitAuthorize():
	#Check: Do we need to do this every time we run, or when?
	server = Oauth2.OAuth2Server(cid_fb, secret_fb)
	server.browser_authorize()
	ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
	REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
	auth2_client = fitbit.Fitbit(cid_fb, secret_fb, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)
	return auth2_client

def fitbitWeekData(auth2_client):
	#WIP: Figure out calling the activities list API properly
	#Collect Activity Data from the Last Week
	#endDate = datetime.now()
	#startDate = endDate + timedelta(days=-7)
	#print(endDate, startDate)

	#print(auth2_client.activities_list(beforeDate=endDate, afterDate=startDate, sort='asc', limit=100, offset=0))


#MAIN
if __name__ == '__main__':

	#Initialize DataFile playlist.csv
	#getPlaylist(sp, polyurl)
	#getPlaylistTempo(sp)
	#savePlaylist()
	#print(f"Your playlist has {len(PLAYLIST)} songs.")

	#Collect Full Fitbit HR & Exercise Data from last Week
	auth2_client = fitbitAuthorize()
	fitbitWeekData(auth2_client)

	#Verify tempo correctness
	#testsong = "We Are the Winx"
	#ident = "62DhR27lWUHYHuD9A3zSrB"
	#print(f"song: {testsong} has {getTempo(sp,ident)} tempo")

	#Run BPM analysis on given playlist
	#df = pd.read_csv('playlist_master.csv')
	#playlistAnalysis(df)

	print("Finished :)")