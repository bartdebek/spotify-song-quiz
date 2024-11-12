import requests
import random
import base64

from environs import Env

# from quiz.utils import TOP_100_ARTISTS

env = Env()
env.read_env()

TOP_100_ARTISTS = [
    "The Beatles", "Elvis Presley", "Michael Jackson", "Madonna", "The Rolling Stones",
    "Bob Dylan", "Led Zeppelin", "Prince", "Pink Floyd", "Aretha Franklin",
    "Stevie Wonder", "David Bowie", "Queen", "Marvin Gaye", "The Beach Boys",
    "Jimi Hendrix", "The Who", "Ray Charles", "Johnny Cash", "Elton John",
    "Nirvana", "Bruce Springsteen", "The Supremes", "Kanye West", "The Eagles",
    "Jay-Z", "Metallica", "Beyoncé", "The Doors", "Bob Marley",
    "U2", "Outkast", "R.E.M.", "Eminem", "Adele",
    "Patsy Cline", "Radiohead", "The Clash", "The Police", "Janet Jackson",
    "Otis Redding", "Whitney Houston", "Tupac Shakur", "James Brown", "Kendrick Lamar",
    "Fleetwood Mac", "Smokey Robinson", "The Temptations", "Paul Simon", "The Kinks",
    "Simon & Garfunkel", "Creedence Clearwater Revival", "Public Enemy", "The Velvet Underground", "Santana",
    "Billy Joel", "Green Day", "Eric Clapton", "LL Cool J", "The Allman Brothers Band",
    "George Michael", "Little Richard", "Aerosmith", "Rihanna", "Missy Elliott",
    "Neil Young", "Chuck Berry", "Van Halen", "The Jackson 5", "Joni Mitchell",
    "Sly & The Family Stone", "Frank Sinatra", "Guns N' Roses", "The Ramones", "Al Green",
    "Sam Cooke", "Louis Armstrong", "Dr. Dre", "Beastie Boys", "Curtis Mayfield",
    "Notorious B.I.G.", "Nine Inch Nails", "Johnny Cash", "Pearl Jam", "Tina Turner",
    "Diana Ross", "Dusty Springfield", "John Lennon", "Elvis Costello", "Bon Jovi",
    "Red Hot Chili Peppers", "Bee Gees", "Etta James", "The Byrds", "Patti Smith",
    "Bo Diddley", "Genesis", "Carole King", "Foo Fighters", "James Taylor",
    "Dolly Parton", "The Cure", "KISS", "B.B. King", "The Zombies"
]


class SpotifyGenerator:
    """
    Class that takes artist name to create an object and lets user get artist parameters from Spotify API
    """

    def __init__(self, limit=20):
        self.limit = limit
        self.client_id = env("CLIENT_ID")
        self.client_secret = env("CLIENT_SECRET")

    def get_artist_id(self, artist_name):
        try:
            params = {'q': artist_name, 'type': 'artist', 'limit': 1}
            headers = {'Authorization': self.get_bearer_token()}
            response = requests.get(
                'https://api.spotify.com/v1/search',
                params=params,
                headers=headers
            ).json()
            return response['artists']['items'][0]['id']
        except ValueError:
            print("Incorrect artist id query")

    def get_artist_name(self, artist_name):
        try:
            headers = {'Authorization': self.get_bearer_token()}
            response = requests.get(
                f'https://api.spotify.com/v1/artists/{self.get_artist_id(artist_name)}',
                headers=headers
            ).json()
            return response['name']
        except ValueError:
            print("Incorrect artist name query")

    def get_artist_picture(self, artist_name):
        try:
            headers = {'Authorization': self.get_bearer_token()}
            response = requests.get(
                f'https://api.spotify.com/v1/artists/{self.get_artist_id(artist_name)}',
                headers=headers
            ).json()
            return response['images'][0]['url']
        except ValueError:
            print("Incorrect artist picture query")

    def get_bearer_token(self):

        data = {
            "grant_type": "client_credentials"
        }

        auth_header = base64.b64encode((self.client_id + ":" + self.client_secret).encode('utf-8'))

        headers = {
            'Authorization': 'Basic ' + auth_header.decode('utf-8'),
            'Content-Type': 'application/x-www-form-urlencoded'
            }
        response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)

        if response.status_code == 200:
            bearer_token = f'Bearer {response.json()["access_token"]}'
            return bearer_token
        else:
            print(auth_header)
            print(response.status_code)
            print("Failed to receive bearer token")

    def get_random_album(self):
        try:
            artist_id = self.get_artist_id()
            id = artist_id
            url = f'https://api.spotify.com/v1/artists/{id}/albums'
            params = {'limit': self.limit}
            headers = {'Authorization': self.get_bearer_token()}
            response = requests.get(url=url, params=params, headers=headers).json()
            data = response['items']
            album_list = []
            for album in data:
                album_name = album['name']
                cover = album['images'][0]['url']
                spotify_link = album['external_urls']['spotify']
                album_list.append([album_name, cover, spotify_link])

            random_album = random.choice(album_list)
            print('Your random album:')
            print(f'Album: {random_album[0]} \nCover: {random_album[1]} \nSpotify Link: {random_album[2]}\n')
        except ValueError:
            print("Incorrect random album query")

    def generate_song_quiz(self, artist_name):
        try:
            artist_id = self.get_artist_id(artist_name)
            id = artist_id
            url = f'https://api.spotify.com/v1/artists/{id}/top-tracks'
            params = {'limit': self.limit, 'market': 'PL'}
            headers = {'Authorization': self.get_bearer_token()}
            response = requests.get(url=url, params=params, headers=headers).json()
            data = response['tracks']
        
        except len(data)<9:
            print("To little song to create 3 questions")

        try:
            songs_list = []
            # generation list of songs
            for song in data:
                if song.get('preview_url'):
                    song_name = song['name']
                    spotify_link = song['external_urls']['spotify']
                    preview = song['preview_url']
                    songs_list.append([song_name, spotify_link, preview])
            
            # creating 3 sets of 3 songs each
            i = 0
            question_dict = {}
            while i < 3:
                random_songs = random.sample(songs_list, k=3)
                song_list = []
                for song in random_songs:
                    song_dict = {
                        'title': song[0],
                        'link': song[1],
                        'sample': song[2],
                    }
                    song_list.append(song_dict)
                    songs_list.remove(song)
                # adding correct answer to song list
                correct_answer = random.choice(song_list)
                song_list.append(correct_answer)
                # creating answers dictionary for each iteration
                question_dict[i] = song_list
                i += 1
            return question_dict
        except ValueError:
            print("Incorrect random song query")

    def generate_top100_artists_quiz(self):

        artists_list = random.sample(TOP_100_ARTISTS, k=10)
        print(artists_list)
        # try:
            for i, artist in enumerate(artists_list):
                print(i)
                artist_id = self.get_artist_id(artist)
                id = artist_id
                url = f'https://api.spotify.com/v1/artists/{id}/top-tracks'
                params = {'limit': self.limit, 'market': 'PL'}
                headers = {'Authorization': self.get_bearer_token()}
                response = requests.get(url=url, params=params, headers=headers).json()
                data = response['tracks']

                songs_list = []
                # generation list of songs
                for song in data:
                    if song.get('preview_url'):
                        song_name = song['name']
                        spotify_link = song['external_urls']['spotify']
                        preview = song['preview_url']
                        songs_list.append([song_name, spotify_link, preview])
            
                # creating set of 3 songs each artist
                question_dict = {}
                random_songs = random.sample(songs_list, k=3)
                song_list = []
                for song in random_songs:
                    song_dict = {
                        'title': song[0],
                        'link': song[1],
                        'sample': song[2],
                    }
                    song_list.append(song_dict)
                    songs_list.remove(song)
                    # adding correct answer to song list
                    correct_answer = random.choice(song_list)
                    song_list.append(correct_answer)
                    # creating answers dictionary for each iteration
                    question_dict[i] = song_list
                    print(question_dict)
            return question_dict
        # except ValueError:
        #     print("Incorrect random song query")