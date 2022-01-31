from django.contrib import admin
from restAPI.models import Receita, Despesa

class Receitas(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'valor', 'date')
    list_display_links = ('id', 'descricao')
    search_fields = ('id', 'descricao', 'date')

admin.site.register(Receita, Receitas)

class Despesas(admin.ModelAdmin):
    list_display = ('id', 'descricao', 'valor', 'date')
    list_display_links = ('id', 'descricao')
    search_fields = ('id', 'descricao', 'date')
# Register your models here.
admin.site.register(Despesa, Despesas)
