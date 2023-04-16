from django.contrib import admin

from .models import ItemCardapio, TipoItem


@admin.register(ItemCardapio)
class ItemCardapioAdmin(admin.ModelAdmin):
    ...


@admin.register(TipoItem)
class TipoItemAdmin(admin.ModelAdmin):
    ...