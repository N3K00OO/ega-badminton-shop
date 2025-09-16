from django.db import models
import uuid



class Product(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    name =  models.CharField(max_length=100)
    price =  models.IntegerField()
    description =  models.TextField()
    thumbnails  = models.URLField()
    category =  models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    brand = models.CharField(max_length=50, default="Unknown")
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def increment_views(self):
        self.views = (self.views or 0) + 1
        self.save(update_fields=["views"])

    def __str__(self):
        return f"{self.name}({self.category})"


# Create your models here.
