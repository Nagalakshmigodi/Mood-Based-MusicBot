import requests
from spotify_auth import get_spotify_token

def get_song_recommendations(mood, language="english", limit=5):
    access_token = get_spotify_token()
    if not access_token:
        return []

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    query = f"{mood} {language}"

    params = {
        "q": query,
        "type": "track",
        "limit": limit
    }

    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)

    if response.status_code != 200:
        print("❌ Spotify API error:", response.status_code, response.text)
        return []

    items = response.json().get("tracks", {}).get("items", [])

    songs = []
    for item in items:
        songs.append({
            "title": item["name"],
            "artist": item["artists"][0]["name"],
            "link": item["external_urls"]["spotify"]
        })

    return songs
