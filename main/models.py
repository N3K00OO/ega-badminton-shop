from django.db import models


class Product(models.Model):
    name =  models.CharField(max_length=100)
    price =  models.IntegerField()
    description =  models.TextField()
    thumbnails  = models.URLField()
    category =  models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    brand = models.CharField(max_length=50, default="Unknown")

def __str__(self):
    return f"{self.name}({self.category})"


# Create your models here.
