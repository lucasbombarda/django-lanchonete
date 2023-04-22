from django.db import models

class TipoItem(models.Model):
    ativo = models.BooleanField(null=False, blank=False, default=True)
    nome = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self) -> str:
        return self.nome

class ItemCardapio(models.Model):
    ativo = models.BooleanField(null=False, blank=False, default=True)
    numero = models.IntegerField(unique=True, null=False, blank=False)
    nome = models.CharField(max_length=100, null=False, blank=True, default='')
    descricao = models.TextField()
    preco_unitario = models.FloatField(null=False, blank=False, default=0.0)
    imagem = models.ImageField(upload_to='cardapio/covers', blank=True, default='')

    criado_em = models.DateTimeField(auto_created=True, auto_now_add=True)
    modificado_em = models.DateTimeField(auto_now=True)

    tipo = models.ForeignKey(TipoItem, on_delete=models.SET_NULL, null=True, blank=True, default='')

    def __str__(self) -> str:
        return self.nome