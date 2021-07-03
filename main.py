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

songs = sp.playlist_items(polyurl)
results = songs['items']
print(f"Call {COUNT} returned {len(results)} number of tracks")

for i in range(1):
	#print(results[i])
	print(results[i].get('track').get('id'))
	print(results[i].get('track').get('name'))
	print(results[i].get('track').get('artists')[0].get('name'))


