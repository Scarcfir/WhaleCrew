from django.db import models


class Newsletter(models.Model):
    email = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.email}'
