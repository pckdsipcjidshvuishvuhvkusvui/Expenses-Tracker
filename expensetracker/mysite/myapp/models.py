from django.db import models

# Create your models here.
class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    category = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)
class Income(models.Model):
    income_name = models.CharField(max_length=100)
    income_amount = models.IntegerField()
    income_category = models.CharField(max_length=50)
    income_date = models.DateField(auto_now=True)

    
    def __str__(self):
        return self.name