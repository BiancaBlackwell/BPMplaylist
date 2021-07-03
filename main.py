# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
# from spotipy.oauth2 import SpotifyOAuth
# import pandas as pd


# def spotify_init():
# 	f = open("BPMkeys.txt", "r")
# 	cid = f.readline().split('\n')[0]
# 	secret = f.readline().split('\n')[0]
# 	auth = f.readline().split('\n')[0]
# 	f.close()

# 	# client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
# 	# sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
# 	scope = "user-library-read"

# 	sp = spotipy.Spotify(client_id = cid, client_secret = secret, auth_manager=SpotifyOAuth(scope=scope))
# 	#track_results = sp.search(q='year:2018', type='track', limit=50)
# 	#print(track_results)
# 	return sp



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

songs = sp.playlist_items(polyurl)
while songs:
    for i, playlist in enumerate(songs['items']):
        print("%4d %s %s" % (i + 1 + songs['offset'],  songs['name']))
    if songs['next']:
        songs = sp.next(songs)
    else:
        songs = None