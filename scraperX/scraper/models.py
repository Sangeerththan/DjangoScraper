from django.db import models


class ScrapedOutput(models.Model):
    output = models.CharField(max_length=200)

    def __str__(self):
        return self.output

