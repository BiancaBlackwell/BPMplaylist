# if __name__ == '__main__':
# 	sp = spotify_init()
# 	results = sp.current_user_saved_tracks()
# 	for idx, item in enumerate(results['items']):
# 	    track = item['track']
# 	    print(idx, track['artists'][0]['name'], " – ", track['name'])


# # artist_name = []
# # track_name = []
# # popularity = []
# # track_id = []

# # track_results = sp.search(q='year:2018', type='track', limit=5)

# # track_dataframe = pd.DataFrame({'artist_name' : artist_name, 'track_name' : track_name, 'track_id' : track_id, 'popularity' : popularity})
# # print(track_dataframe.shape)
# # print(track_dataframe)
# # track_dataframe.head()


import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials

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


#MAIN
if __name__ == '__main__':
	getPlaylist(sp, polyurl)
	getPlaylistTempo(sp)
	print(f"Your playlist has {len(PLAYLIST)} songs.")
	



