from django.db import models
from books.models import Book # To connect sales with books

# Create your models here.

class Sale(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE) #CASCADE for when a book is deleted, all positions related to the book will be deleted.
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"id: {self.id}, book: {self.book.name}, quanity: {self.quantity}"