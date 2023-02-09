from environs import Env

from quiz.utils import SpotifyGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:3000', 'http://localhost:8080'],
    allow_methods = ['*'],
    allow_headers = ['*']
)

# This should be different database
redis = get_redis_connection(
    host = 'redis-16684.c293.eu-central-1-1.ec2.cloud.redislabs.com',
    port = 16684,
    password = 'BvvO31FmhvHBNyWqzOClffUPDZYf9uAz',
    decode_responses = True
)

@app.get('/questions/{artist}')
async def read_item(artist: str):
    my_generator = SpotifyGenerator(artist, limit=30)
    generated_questions = my_generator.generate_song_quiz()
    artist_name = my_generator.get_artist_name()
    atrist_picture = my_generator.get_artist_picture()
    answers_list = [generated_questions[x] for x in generated_questions]
    response = {
        'artist_name': artist_name,
        'artist_picture': atrist_picture,
        'questions': answers_list,
        }

    return response