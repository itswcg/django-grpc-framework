from django.db import models


class Greet(models.Model):
    sender = models.CharField(verbose_name='sender', max_length=12)
    receiver = models.CharField(verbose_name='receiver', max_length=12)
    message = models.CharField(verbose_name='message', max_length=128)

    def __str__(self):
        return f'{self.sender}-{self.receiver}'
