from django.db import models
from django.utils import timezone

"""
CONTATOS
id: INT (automático)
nome: STR * (obrigatório)
sobrenome: STR (opcional)
telefone: STR * (obrigatório)
email: STR (opcional)
data_criacao: DATETIME (automático)
descricao: texto
categoria: CATEGORIA (outro model)

 CATEGORIA
 id: INT
 nome: STR * (obrigatório)
"""


class Category(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=255)


class Contact(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    show = models.BooleanField(default=True)
    photo = models.ImageField(blank=True, upload_to='pictures/%Y/%m/')
