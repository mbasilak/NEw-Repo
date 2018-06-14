from django.db import models

# Create your models here.
class Warehouse(models.Model):
    name = models.CharField(max_length = 30)
    code = models.CharField(max_length = 10)
    storage_capacity = models.IntegerField()
    terminal_capacity = models.IntegerField()
    combinations = models.ManyToManyField("self",blank=True,null=True)
    date = models.DateTimeField()

    def __str__(self):
        return self.name
