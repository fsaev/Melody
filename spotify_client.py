#!/usr/bin/python3

import spotipy.util as util
import spotipy
from tinydb import TinyDB, Query

class Remote:

    def __init__(self, username):
        q = Query()
        self.token_db = TinyDB("./tokens.json")

        if not len(self.token_db.search(q.client_id)):
            self.client_id = input("Client ID: ")
            self.token_db.insert({'client_id': self.client_id})
        else:
            self.client_id = self.token_db.search(q.client_id)[0]['client_id']

        if not len(self.token_db.search(q.client_secret)):
            self.client_secret = input("Client Secret: ")
            self.token_db.insert({'client_secret': self.client_secret})
        else:
            self.client_id = self.token_db.search(q.client_secret)[0]['client_secret']

        if not len(self.token_db.search(q.devices_token)):
            self.devices_token = util.prompt_for_user_token(username,'user-read-playback-state',client_id=self.client_id,client_secret=self.client_secret, redirect_uri='http://localhost:8888/callback/')
            self.token_db.insert({'devices_token': self.devices_token})
        else:
            self.devices_token = self.token_db.search(q.devices_token)[0]['devices_token']

        if not len(self.token_db.search(q.playback_token)):
            self.playback_token = util.prompt_for_user_token(username,'user-modify-playback-state',client_id=self.client_id,client_secret=self.client_secret, redirect_uri='http://localhost:8888/callback/')
            self.token_db.insert({'playback_token': self.playback_token})
        else:
            self.playback_token = self.token_db.search(q.playback_token)[0]['playback_token']

    def poll_for_devices(self):
        return spotipy.Spotify(auth=self.devices_token).devices()

    def prompt_for_device_selection(self):
        q = Query()
        devices = self.poll_for_devices()
        dcount = 0
        for i in range(len(devices['devices'])):
            dcount = i
            d = devices['devices'][i]
            print(str(i) + ": " + d['name'] + " (" + d['id'] + ")")
        selection = input("Select from [0-"+dcount+"]: ")
        self.active_device = devices['devices'][selection]['id']

    def play_song(self, device_id, uris):
        s = spotipy.Spotify(auth=self.playback_token)
        s.start_playback(device_id=device_id, uris=uris)
    
    def pause(self, device_id):
        s = spotipy.Spotify(auth=self.playback_token)
        s.pause_playback(device_id=device_id)
    


r = Remote("username")
r.prompt_for_device_selection()
uris = []
uris.append('spotify:track:0S3gpZzlT9Hb7CCSV2owX7')
#r.pause(devices['devices'][1]['id'])
r.play_song(devices['devices'][1]['id'], uris)
print(devices)
