from django.contrib.auth.models import AbstractUser
from django.db import models
import ast

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Add custom fields here, if needed

    def __str__(self):
        return self.username

class CSVFile(models.Model):
    AppID = models.IntegerField()
    Name = models.CharField(max_length=255)
    Release_date = models.DateTimeField()  # Use DateField if you don't have time information
    Required_age = models.IntegerField()
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    DLC_count = models.IntegerField()
    About_the_game = models.TextField()
    Supported_languages = models.TextField()
    Windows = models.BooleanField()
    Mac = models.BooleanField()
    Linux = models.BooleanField()
    Positive = models.IntegerField()
    Negative = models.IntegerField()
    Score_rank = models.IntegerField()
    Developers = models.CharField(max_length=255)
    Publishers = models.CharField(max_length=255)
    Categories = models.TextField()
    Genres = models.TextField()
    Tags = models.TextField()

    def __str__(self):
        return self.Name

    def get_supported_languages(self):
        return ast.literal_eval(self.Supported_languages)

    def get_tags_list(self):
        # Split Tags string into a list of tags
        return [tag.strip() for tag in self.Tags.split(',') if tag.strip()]

    def get_genres_list(self):
        # Split Genres string into a list of genres
        return [genre.strip() for genre in self.Genres.split(',') if genre.strip()]

    def get_categories_list(self):
        # Split Categories string into a list of categories
        return [category.strip() for category in self.Categories.split(',') if category.strip()]