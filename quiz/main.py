from utils import SpotifyGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from environs import Env

app = FastAPI()
env = Env()
env.read_env()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'http://localhost:8080', 'https://spotify-quiz-app.netlify.app', 'http://192.168.1.7:8080'],
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get('/questions/{artist}')
async def read_item(artist: str):
    my_generator = SpotifyGenerator(artist, limit=30)
    generated_questions = my_generator.generate_song_quiz()
    artist_name = my_generator.get_artist_name()
    artist_picture = my_generator.get_artist_picture()
    answers_list = [generated_questions[x] for x in generated_questions]
    response = {
        'artist_name': artist_name,
        'artist_picture': artist_picture,
        'questions': answers_list,
        }

    return response
