from django.db import models
from user.models import UserModel


# Create your models here.
class Movie(models.Model):
    class Meta:
        db_table = "movie"

    title = models.CharField(max_length=100)
    year = models.CharField(max_length=4)
    genre = models.CharField(max_length=200)
    image = models.URLField(max_length=200, blank=True)
    video = models.URLField(max_length=200, blank=True)
    cast = models.CharField(max_length=200, blank=True)
    film_rating_system = models.CharField(max_length=20, blank=True)
    information = models.TextField(blank=True)
    information_url = models.URLField(max_length=200, blank=True)


class Rating(models.Model):
    class Meta:
        db_table = "rating"

    RATING1 = '0.5'
    RATING2 = '1'
    RATING3 = '1.5'
    RATING4 = '2'
    RATING5 = '2.5'
    RATING6 = '3'
    RATING7 = '3.5'
    RATING8 = '4'
    RATING9 = '4.5'
    RATING10 = '5'

    STAR_CHOICES = [
        (RATING1, 0.5),
        (RATING2, 1),
        (RATING3, 1.5),
        (RATING4, 2),
        (RATING5, 2.5),
        (RATING6, 3),
        (RATING7, 3.5),
        (RATING8, 4),
        (RATING9, 4.5),
        (RATING10, 5),
    ]

    user_id = models.ForeignKey('user.UserModel', related_name="user", on_delete=models.CASCADE, db_column="user_id")
    movie_id = models.ForeignKey('Movie', related_name="movie", on_delete=models.CASCADE, db_column="movie_id")
    rating = models.CharField(max_length=3, choices=STAR_CHOICES, default=RATING10)
    comment = models.CharField(max_length=500, default='', blank=True)