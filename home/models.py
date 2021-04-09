from django.db import models
from django.contrib.auth.models import User


class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    short_desc = models.CharField(max_length=255)
    description = models.TextField(null=True)
    picture_file = models.ImageField(upload_to='static/images/article/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ("add_article", "Can publish articles"),
        )

    def get_detail_url(self):
        """
        Return the url of article.
        """
        return f"/News/{self.id}"

    def __str__(self):
        return f'{self.title}'


