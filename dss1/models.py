from django.db import models

# Create your models here.
from django.forms import ModelForm

class Input(models.Model):
    total_rakes = models.IntegerField()
    demand = models.CharField(max_length=50)
    initial_stock_level = models.CharField(max_length=50)
    storage_capacity = models.CharField(max_length=50)
    terminal_capacity = models.CharField(max_length=50)
    max_allotment = models.CharField(max_length=50)
    weekly_penalty = models.CharField(max_length=100)
    comb_matrix = models.CharField(max_length=200)

class InputForm(ModelForm):
    class Meta:
        model = Input
        fields = '__all__'
