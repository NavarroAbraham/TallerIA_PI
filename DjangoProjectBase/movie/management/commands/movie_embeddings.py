from django.core.management.base import BaseCommand
from movie.models import Movie
from movie.utils import get_embedding

class Command(BaseCommand):
    help = 'Generate and store movie embeddings using OpenAI'

    def handle(self, *args, **kwargs):
        movies = Movie.objects.all()
        for movie in movies:
            embedding = get_embedding(movie.description)
            movie.emb = embedding.tobytes()
            movie.save()
            self.stdout.write(self.style.SUCCESS(f"Embedding stored for: {movie.title}"))