from crypt import methods
from django.template import context
from rest_framework import viewsets, filters, status
from restAPI.models import Receita, Despesa
from restAPI.serializer import ReceitaSerializer, DespesaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class ReceitasViewSet(viewsets.ModelViewSet):
    """Exibindo todas as receitas recebidas"""
    queryset = Receita.objects.all()
    serializer_class = ReceitaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['descricao']
    filterset_fields = ['descricao']
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path=r'(?P<ano>\d{4})/(?P<mes>\d{1,2})')
    def getReceitaPorMes(self, request, ano, mes):
        receitas = Receita.objects.filter(date__year=ano, date__month=mes)
        if not receitas:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(receitas, many=True, context={'request': request})
        return Response(serializer.data)

class DespesasViewSet(viewsets.ModelViewSet):
    """Exibindo todas as despesas"""
    queryset = Despesa.objects.all()
    serializer_class = DespesaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['descricao']
    filterset_fields = ['descricao']
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path=r'(?P<ano>\d{4})/(?P<mes>\d{1,2})')
    def getDespesaPorMes(self, request, ano, mes):
        """Pega as despesas do mes e ano passado"""
        despesas = Despesa.objects.filter(date__year=ano, date__month=mes)
        if not despesas:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(despesas, many=True, context={'request': request})
        return Response(serializer.data)

class ResumoViewSet(APIView):
    """Mostra o resumo do mes"""
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, ano, mes):
        receitas = Receita.objects.filter(date__year = ano, date__month = mes).aggregate(Sum('valor'))['valor__sum'] or 0
        despesas = Despesa.objects.filter(date__year = ano, date__month = mes).aggregate(Sum('valor'))['valor__sum'] or 0
        saldo_final = receitas-despesas

        despesa_categoria = Despesa.objects.filter(date__year = ano, date__month = mes).values('categoria').annotate(Sum('valor'))

        return Response({
            "receita":receitas,
            "despesas":despesas,
            "saldo":saldo_final,
            "despesa_mensal":despesa_categoria
        })