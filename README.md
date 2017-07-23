# Worldify
Spotify Music Generator from current events

This hack generates a list of songs from current tweets happening in real time in different continents, and use
sentiment analysis to generate the mood of that region and consider the genre listened by the user to generate new playlists
depending upon the `energy level` setting in Spotify.

# Config Requirements

Before you are able to run Worldly you need to have a config file located at `~/.worldify` with the following set up:

```
[twitter]
customer_key = TWITTER_CUSTOMER_KEY
customer_secret = TWITTER_CUSTOMER_SECRET
access_key = TWITTER_ACCESS_KEY
access_secret = TWITTER_ACCESS_SECRET

[recptiviti]
api_key = RECPTIVITI_API_LEY
api_secret = RECPTIVITI_API_SECRET


[spotify]
user_id = SPOTIFY_USER_ID
user_oath = SPOTIFY_USER_OAUTH_TOKEN
client_id = SPOTIFY_CLIENT_ID
client_secret = SPOTIFY_CLIENT_SECRET
```
