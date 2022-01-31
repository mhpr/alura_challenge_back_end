from dataclasses import fields
from rest_framework import serializers
from restAPI.models import Receita, Despesa

class ReceitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receita
        fields = ['descricao', 'valor', 'date']


class DespesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despesa
        exclude = []

    def validate(self, attrs):
        print("######################################################################")
        print(attrs['date'].month)
        print("######################################################################")
        if Despesa.objects.filter(descricao=attrs['descricao'], date__month=attrs['date'].month, date__year=attrs['date'].year).exists():
            raise serializers.ValidationError('Despesa já cadastrada para este mês e ano')
        return attrs