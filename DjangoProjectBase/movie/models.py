from django.db import models
from django.core.management.base import BaseCommand
from movie.utils import get_completion
from django.db import models
import numpy as np

# create your models here


def get_default_array():
    default_arr = np.random.rand(1536)
    return default_arr.tobytes()

from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1500)
    image = models.ImageField(upload_to='movie/images/', default='movie/images/default.jpg')
    url = models.URLField(blank=True)
    genre = models.CharField(blank=True, max_length=250)
    year = models.IntegerField(blank=True, null=True)
    emb = models.BinaryField(default=get_default_array())

    def __str__(self):
        return self.title


# Review model for movie reviews
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.movie.title}"

class Command(BaseCommand):
    help = 'Update movie descriptions using OpenAI'

    def handle(self, *args, **kwargs):
        movies = Movie.objects.all()
        for movie in movies:
            prompt = f"Actualiza la descripción '{movie.description}' de la película '{movie.title}'"
            response = get_completion(prompt)
            movie.description = response
            movie.save()
            self.stdout.write(self.style.SUCCESS(f"Updated: {movie.title}"))