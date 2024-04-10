from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    class Meta:
        db_table = 'api_genre'

    tmdb_id = models.IntegerField(null=True)
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.genre


class Keyword(models.Model):

    class Meta:
        db_table = 'api_keyword'
    tmdb_id = models.IntegerField(null=True)
    keyword = models.CharField(max_length=100)

    def __str__(self):
        return self.keyword


class Movie(models.Model):
    tmdb_id = models.IntegerField(null=True)
    title = models.CharField(max_length=100)
    overview = models.TextField()
    poster_path = models.URLField(max_length=255, null=True)
    year = models.IntegerField()
    vote_average = models.FloatField()
    genres = models.ManyToManyField( Genre, blank=True )
    keywords = models.ManyToManyField( Keyword, blank=True )
    trailer_link = models.URLField(max_length=255, null=True)

    def add_keywords(self, keywords):
        self.keywords.add(*keywords)
        self.save()

    def add_genres(self, genres):
        self.genres.add(*genres)
        self.save()

    class Meta:
        db_table = 'api_movie'

    def __str__(self):
        return self.title


class WatchLaterMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)