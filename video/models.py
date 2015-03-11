from django.db import models

# 
class VideoDirectory(models.Model):
    name = models.CharField(max_length=200)
    # Location of apache video directory and base url for HTML5 video src attribute
    vid_dir = models.CharField(max_length=200)
    vid_url = models.CharField(max_length=200)

