from django.db import models

class Language(models.Model):
    name = models.CharField(max_length=100)        # e.g. "English"
    code = models.CharField(max_length=10)         # e.g. "en"

    def __str__(self):
        return self.name


class MinimalPair(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='minimal_pairs')
    sound_1 = models.CharField(max_length=10)      # e.g. "b"
    sound_2 = models.CharField(max_length=10)      # e.g. "p"

    def __str__(self):
        return f"{self.language.name}: {self.sound_1} / {self.sound_2}"


class Word(models.Model):
    minimal_pair = models.ForeignKey(MinimalPair, on_delete=models.CASCADE, related_name='words')
    text         = models.CharField(max_length=100)
    sound        = models.CharField(max_length=10)
    partner      = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True)
    audio_file   = models.FileField(upload_to='audio/', blank=True, null=True)

    def __str__(self):
        return f"{self.text} ({self.sound})"