from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
import os
from dotenv import load_dotenv
import requests

load_dotenv('openAI.env')
client = OpenAI(api_key=os.environ.get('openai_apikey'))

def generate_and_download_image(self, client, movie_title, save_folder):
    prompt = f"Movie poster of {movie_title}"
    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        size="256x256",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url

    image_filename = f"m_{movie_title}.png"
    image_path_full = os.path.join(save_folder, image_filename)

    image_response = requests.get(image_url)
    image_response.raise_for_status()
    with open(image_path_full, 'wb') as f:
        f.write(image_response.content)

    return os.path.join('movie/images', image_filename)

class Command(BaseCommand):
    help = 'Generate and update movie images using OpenAI'

    def handle(self, *args, **kwargs):
        images_folder = 'media/movie/images/'
        os.makedirs(images_folder, exist_ok=True)

        movies = Movie.objects.all()
        for movie in movies:
            image_relative_path = self.generate_and_download_image(client, movie.title, images_folder)
            movie.image = image_relative_path
            movie.save()
            self.stdout.write(self.style.SUCCESS(f"Saved and updated image for: {movie.title}"))