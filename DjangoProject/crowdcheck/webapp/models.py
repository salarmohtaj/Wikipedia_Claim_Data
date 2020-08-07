from django.db import models

# Create your models here.


class sentences(models.Model):
    journal_id = models.IntegerField(null=True)
    sentence = models.TextField(null=True)
    wikilabel = models.IntegerField(null=True)
    crowdlabel = models.IntegerField(null=True)