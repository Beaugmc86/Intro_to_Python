from django.db import models

# Create your models here.
genre_choices = (
    ('classic', 'Classic'),
    ('romantic', 'Romantic'),
    ('comic', 'Comic'),
    ('fantasy', 'Fantasy'),
    ('horror', 'Horror'),
    ('educational', 'Educational')
)

book_type_choices = (
    ('hardcover', 'Hardcover'),
    ('ebook', 'E-book'),
    ('audiobook', 'Audiobook')
)

class Book(models.Model):
    name = models.CharField(max_length=120)

    # Dropdown list of genre
    genre = models.CharField(
        max_length=12,
        choices=genre_choices,
        default='classic'
    )

    # Dropdown list of book type
    book_type = models.CharField(
        max_length=12,
        choices=book_type_choices,
        default='hardcover'
    )
    price = models.FloatField(help_text= 'in US dollars $')
    author_name = models.CharField(max_length=120) #Author's name

    def __str__(self):
        return str(self.name)