from django.db import models
from django.contrib.auth.models import User

class Recomendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Beauty = models.IntegerField(default=0)
    Clothes = models.IntegerField(default=0)
    Electronics = models.IntegerField(default=0)
    Furnitures = models.IntegerField(default=0)
    Sport = models.IntegerField(default=0)
    Toys = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
