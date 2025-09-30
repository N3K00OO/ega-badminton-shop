# main/models.py
from django.db import models
from django.contrib.auth.models import User
import uuid

# single source of truth
CATEGORY_CHOICES = [
    ("jerseys", "Jerseys"),
    ("balls", "Balls"),
    ("trainers", "Trainers"),
    ("protectors", "Protectors"),
    ("clearance", "Clearance"),
    ("misc", "Misc / Others"),
]

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    thumbnails = models.URLField()

    # ↓ now this sees CATEGORY_CHOICES
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    is_featured = models.BooleanField(default=False)
    brand = models.CharField(max_length=50, default="Unknown")
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def increment_views(self):
        self.views = (self.views or 0) + 1
        self.save(update_fields=["views"])

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    @classmethod
    def categories(cls):
        return CATEGORY_CHOICES
