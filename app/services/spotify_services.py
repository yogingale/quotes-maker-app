from bs4 import BeautifulSoup
import requests
from collections import namedtuple

SpotifyTop30 = namedtuple("SpotifyTop30", "artist album song duration")


def get_top_30(spotify_url):
    res = requests.get(spotify_url)
    page = res.content
    soup = BeautifulSoup(page, "html.parser")
    top_30 = []

    #    track_list = soup.find('li', attrs={'class': "tracklist-row js-track-row tracklist-row--track track-has-preview preview-strategy track-playback-enabled"})
    track_list = soup.findAll("li", attrs={"class": "tracklist-row"})
    for track in track_list:
        # print(track)
        track_name = track.find("span", attrs={"class": "track-name"}).text.strip()
        # print(track_name)
        artists_albums = track.find("span", attrs={"class": "artists-albums"}).findAll(
            "a"
        )
        artist = artists_albums[0].text
        album = artists_albums[1].text
        duration = track.find("span", attrs={"total-duration"}).text
        # print(artist, album, duration)
        top_30.append(
            SpotifyTop30(artist=artist, album=album, song=track_name, duration=duration)
        )

    return top_30


if __name__ == "__main__":
    url = "https://open.spotify.com/user/thesoundsofspotify/playlist/1z1LfuAoQQDRKLOyVQvaRa"

    t30 = get_top_30(url)

    for t in t30:
        print(t)
