from django.db import models
from django.utils import timezone


class Stock(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    data = models.TextField()

    def __str__(self):
        return str(self.created) + ' ' + str(self.name)
