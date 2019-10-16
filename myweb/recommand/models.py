from django.db import models

# Create your models here.
class input_beer(models.Model):
    first = models.CharField(max_length=20)
    second = models.CharField(max_length=20, null=True)
    third = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'recommand_input_beer'

class Beer(models.Model):
    feel = models.TextField(blank=True, null=True)
    look = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    smell = models.TextField(blank=True, null=True)
    taste = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'beer'
