from rest_framework import viewsets
from api.serializers import TransactionSerializer
from api.models import Transaction

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = []