from django.db import models
from django.contrib.auth.models import User
from apps.content.models import MinimalPair

class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    minimal_pair = models.ForeignKey(MinimalPair, on_delete=models.CASCADE, related_name='scores')
    correct = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    duration_chosen = models.IntegerField()        # in seconds: 60/300/600/1200
    session_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_label = self.user.username if self.user else 'Guest'
        return f"{user_label} — {self.minimal_pair} — {self.correct}/{self.total}"