from django.db import models

# Media server, with type, base url, and location on disk
class MediaServer(models.Model):
    MEDIA_TYPES = (
        ('A','Audio'),
        ('V','Video'),
    )
    name = models.CharField(max_length=200)
    media_type = models.CharField(max_length=1, choices=MEDIA_TYPES)
    directory_path = models.CharField(max_length=200)
    server_url = models.CharField(max_length=200)
