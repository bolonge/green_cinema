from django.db import models
# from user.models import User


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.CharField(max_length=4)
    genre = models.CharField(max_length=200)
    image = models.URLField(max_length=200, blank=True)
    video = models.URLField(max_length=200, blank=True)
    cast = models.CharField(max_length=200, blank=True)
    film_rating_system = models.CharField(max_length=20, blank=True)
    information = models.TextField(blank=True)

    class Meta:
        db_table = "movie"


class Rating(models.Model):
    class Meta:
        db_table = "rating"

    movie_id = models.ForeignKey('Movie', related_name="movie", on_delete=models.CASCADE, db_column="movie_id")
    # average_rating = models.tinyint(range=5)

# class genre