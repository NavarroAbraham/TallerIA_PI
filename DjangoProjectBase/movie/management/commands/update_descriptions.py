from django.core.management.base import BaseCommand
from movie.models import Movie
from movie.utils import get_completion

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
