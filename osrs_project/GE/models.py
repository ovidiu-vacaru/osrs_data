from django.db import models

# Create your models here.


class Item(models.Model):
    item_name = models.CharField(max_length=200, unique=True)
    item_id = models.IntegerField(unique=True, primary_key=True)

    def __str__(self):
        return self.item_name
