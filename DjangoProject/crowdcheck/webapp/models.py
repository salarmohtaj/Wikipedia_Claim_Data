from django.db import models

# Create your models here.
class sentences(models.Model):
    journal_id = models.IntegerField(null=True)
    sentence = models.TextField(null=True)
    wikilable = models.IntegerField(null=True)
    crowdlable = models.IntegerField(null=True)