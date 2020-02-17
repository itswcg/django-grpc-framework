from django.db import models


class Greet(models.Model):
    name = models.CharField(verbose_name='name', max_length=12)

    def __str__(self):
        return f'{self.name}'
