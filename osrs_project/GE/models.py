from django.db import models

# Create your models here.


class Item(models.Model):
    item_name = models.CharField(max_length=200, unique=True)
    item_id = models.IntegerField(unique=True, primary_key=True)

    def __str__(self):
        return self.item_name


class ItemValue(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.IntegerField()
    date = models.DateField()
    volume = models.IntegerField()

    def __str__(self):
        return f"{self.item_id} - {self.date}"
