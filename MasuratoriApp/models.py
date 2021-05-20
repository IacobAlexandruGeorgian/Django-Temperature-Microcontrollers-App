from django.db import models

# Create your models here.

class Tblmasuratori(models.Model):
    umiditate = models.IntegerField(db_column='Umiditate', blank=True, null=True)  # Field name made lowercase.
    temperatura = models.IntegerField(db_column='Temperatura', blank=True, null=True)  # Field name made lowercase.
    presiune = models.IntegerField(db_column='Presiune', blank=True, null=True)  # Field name made lowercase.
    altitudine = models.IntegerField(db_column='Altitudine', blank=True, null=True)  # Field name made lowercase.
    timp = models.IntegerField(db_column='Timp', blank=True, null=True)  # Field name made lowercase.
    data = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        db_table = 'tblmasuratori'
