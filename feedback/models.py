from django.db import models

class Feedback(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    recording_file = models.FileField()
    language = models.CharField(max_length=2)

    def __str__(self):
        return f'{self.language.upper()} - {self.created_at.strftime("%d-%m-%Y %H:%M:%S")}'
