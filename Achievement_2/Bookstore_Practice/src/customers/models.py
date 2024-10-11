from django.db import models

# Create your models here.

# Create a table "Customer" and attributes "name and notes" as columns within the table.
class Customer(models.Model):
    name = models.CharField(max_length=120)
    notes = models.TextField()
    pic = models.ImageField(upload_to='customers', default='no_picture.png')

    # Specify the string representation of the object allowing customer to be specified name (as opposed to ID [1])
    def __str__(self):
        return str(self.name)