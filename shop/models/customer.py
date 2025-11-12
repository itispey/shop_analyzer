from django.contrib.auth import get_user_model
from django.db import models

user = get_user_model()


class Customer(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Customer"
