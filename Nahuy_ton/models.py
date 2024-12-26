from django.db import models

class UserProfile(models.Model):
    telegram_id = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    wallet_address = models.CharField(max_length=100, null=True, blank=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.username or f"User {self.telegram_id}"


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    points_reward = models.IntegerField(default=0)
    assigned_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.title
