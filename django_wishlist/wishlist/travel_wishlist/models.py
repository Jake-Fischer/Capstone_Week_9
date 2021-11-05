from django.db import models
from django.contrib.auth.models import User

# Contains models for place objects
class Place(models.Model):
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    date_vistied = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def __str__(self):
        photo_str = self.photo.url if self.photo else 'no photo'
        notes_str = self.notes[100:] if self.notes else 'no notes'
        return f'{self.name} visited? {self.visited} on {self.date_vistied}. Notes: {notes_str} Photo {photo_str}'
