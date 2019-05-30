#!/usr/bin/python3

import spotipy.util as util
import spotipy
from tinydb import TinyDB, Query

def exists_in_db(database, query):
    return len(database.search(query))

class Remote:

    def __init__(self):
        q = Query()
        self.config_db = TinyDB("./config.json")

        if not exists_in_db(self.config_db, q.username):
            self.username = input("Spotify Username: ")
            self.config_db.insert({'username': self.username})
        else:
            self.username = self.config_db.search(q.username)[0]['username']

        if not exists_in_db(self.config_db, q.client_id):
            self.client_id = input("Client ID: ")
            self.config_db.insert({'client_id': self.client_id})
        else:
            self.client_id = self.config_db.search(q.client_id)[0]['client_id']

        if not exists_in_db(self.config_db, q.client_secret):
            self.client_secret = input("Client Secret: ")
            self.config_db.insert({'client_secret': self.client_secret})
        else:
            self.client_id = self.config_db.search(q.client_secret)[0]['client_secret']

        if not exists_in_db(self.config_db, q.devices_token):
            self.devices_token = util.prompt_for_user_token(self.username,'user-read-playback-state',client_id=self.client_id,client_secret=self.client_secret, redirect_uri='http://localhost:8888/callback/')
            self.config_db.insert({'devices_token': self.devices_token})
        else:
            self.devices_token = self.config_db.search(q.devices_token)[0]['devices_token']

        if not exists_in_db(self.config_db, q.playback_token):
            self.playback_token = util.prompt_for_user_token(self.username,'user-modify-playback-state',client_id=self.client_id,client_secret=self.client_secret, redirect_uri='http://localhost:8888/callback/')
            self.config_db.insert({'playback_token': self.playback_token})
        else:
            self.playback_token = self.config_db.search(q.playback_token)[0]['playback_token']

        self.playback_session = spotipy.Spotify(auth=self.playback_token)
        self.devices_session = spotipy.Spotify(auth=self.devices_token)

    def poll_for_devices(self):
        return spotipy.Spotify(auth=self.devices_token).devices()

    def prompt_for_device_selection(self, update):
        q = Query()
        if not exists_in_db(self.config_db, q.last_active_device) or update is True:
            devices = self.poll_for_devices()
            dcount = 0
            for i in range(len(devices['devices'])):
                dcount = i
                d = devices['devices'][i]
                print(str(i) + ": " + d['name'] + " (" + d['id'] + ")")
            selection = input("Select from [0-"+str(dcount)+"]: ")
            self.active_device = devices['devices'][int(selection)]['id']
            if update is True:
                self.config_db.update({'last_active_device': self.active_device}, q.last_active_device)
            else:
                self.config_db.insert({'last_active_device': self.active_device})
        else:
            self.active_device = self.config_db.search(q.last_active_device)[0]['last_active_device']

    def set_shuffle(self, device_id, shuffle):
        self.playback_session.shuffle(device_id=device_id, state=shuffle)

    def skip_track(self, device_id):
        self.playback_session.next_track(device_id)

    def play_song(self, device_id, uris):
        self.playback_session.start_playback(device_id=device_id, uris=uris)

    def play_playlist(self, device_id, uri):
        self.playback_session.start_playback(device_id=device_id, context_uri=uri)
    
    def pause(self, device_id):
        self.playback_session.pause_playback(device_id=device_id)
    


r = Remote()
r.prompt_for_device_selection(False)
uris = []
uris.append('spotify:track:0S3gpZzlT9Hb7CCSV2owX7')
#r.pause(r.active_device)
r.play_song(r.active_device, uris)
