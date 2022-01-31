from django.db import models

# Create your models here.
class Receita(models.Model):
    descricao = models.CharField(max_length=100, null=False)
    valor = models.FloatField(null=False)
    date = models.DateField(null=False)

class Despesa(models.Model):
    descricao = models.CharField(max_length=100, null=False)
    valor = models.FloatField(null=False)
    date = models.DateField(null=False)
    CATEGORIAS = (
        ("ALIMENTACAO", "Alimentação"),
        ("SAUDE", "Saúde"),
        ("MORADIA", "Moradia"),
        ("TRANSPORTE", "Transporte"),
        ("EDUCACAO", "Educação"),
        ("LAZER", "Lazer"),
        ("IMPREVISTOS", "Imprevistos"),
        ("OUTRAS", "Outras"),
    )
    categoria = models.CharField(max_length=15, choices=CATEGORIAS, default='OUTRAS')