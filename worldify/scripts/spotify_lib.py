'''Containing functions to interact with spotify web api wrapper'''

import datetime
import os
import requests
import urlparse

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotipy.util as util

# Constants
SPOTIFY_USER_ID = os.getenv("SPOTIFY_USER_ID")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SCOPE = "user-library-read playlist-modify-public playlist-modify-private playlist-read-private"

SPOTIFY_USER_OAUTH = os.getenv("SPOTIFY_USER_OAUTH")

def _get_request_session_object_with_oauth():
    '''Return a session object with oauth header.'''
    headers = {"Authorization": "Bearer {0}".format(SPOTIFY_USER_OAUTH),
               "Content-Type": "application/json"}
    session_obj = requests.Session()
    session_obj.headers.update(headers)
    return session_obj

def _get_spotify_api_url(endpoint=''):
    '''Return a Spotify API url with an optional custom endpoint.'''
    return urlparse.urljoin("https://api.spotify.com/v1/", endpoint)


def _get_generated_recommendation_tracks(country_code, genre_seed_list, energy_level=0.5, songs_limit=10):
    '''Returns a list of recommended track ids based on query values.'''
    queries = {"seed_genres":genre_seed_list, "valence":energy_level,
             "market":country_code, "limit":songs_limit}
    api_url = _get_spotify_api_url("recommendations")
    session_obj = _get_request_session_object_with_oauth()
    response = session_obj.get(api_url, params=queries)
    json_tracks_list = response.json()['tracks']
    recommended_tracks_id_list = [track['id'] for track in
                                  json_tracks_list]
    return recommended_tracks_id_list


def _generate_recommended_playlist(tracks_id_list):
    '''Create a public playilist and add tracks to it.'''
    playlist_url = _create_public_playlist()
    response = _add_tracks_to_playlist(playlist_url, tracks_id_list)
    return response

def _create_public_playlist():
    '''Return playlist url after creating it publicly on user's page'''
    endpoint = "users/{0}/playlists".format(SPOTIFY_USER_ID)
    api_url = _get_spotify_api_url(endpoint)
    playlist_name = datetime.datetime.now().strftime("%H-%M-%S")
    post_body = {"name": playlist_name}
    session_obj = _get_request_session_object_with_oauth()
    response = session_obj.post(api_url, json=post_body)
    return response.json()['href']

def _add_tracks_to_playlist(playlist_url, tracks_id_list):
    '''Add a list of tracks to a given playlist.'''
    uri_list_query = {"uris": tracks_id_list}
    session_obj = _get_request_session_object_with_oauth()
    response = session_obj(playlist_url, params=uri_list_query)
    return response




def generate_playlist(list_of_genres, country_code, energy_value):
    '''Public function to generate a public playlist'''
    track_id_list = _get_generated_recommendation_tracks(country_code,
                                                         list_of_genres,
                                                         energy_value)
    return _generate_recommended_playlist(track_id_list)


if __name__ == "__main__":
    generate_playlist(['classical', 'rock'], "GB", 0.506)
