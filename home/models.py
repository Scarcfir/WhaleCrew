from django.db import models


class News(models.Model):
    title = models.CharField(max_length=255)
    short_desc = models.CharField(max_length=255)
    description = models.TextField(null=True)
    picture_file = models.ImageField(upload_to='static/images/article/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def get_detail_url(self):
        return f"/News/{self.id}"
