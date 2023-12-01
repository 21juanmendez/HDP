from django.db import models

# Create your models here.

class Registros(models.Model):
    id = models.AutoField(primary_key=True)
    discapacidad = models.CharField(max_length=50,null=False)
    universidad = models.CharField(max_length=50,null=False)
    sexo = models.CharField(max_length=50,null=False)
    cantidad = models.IntegerField(null=False)
    f_registro = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        db_table = 'registros'
