from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, action
from account.filters import BaseFilter
from api.models import Subtopic, Topic
from api.serializers import SubtopicSerializer
from rest_framework.response import Response
from rest_framework import status


class SubtopicViewSet(viewsets.ModelViewSet):
    queryset = Subtopic.objects.all()
    serializer_class = SubtopicSerializer
    permission_classes = []

    def get_queryset(self):
        params = self.request.query_params
        f = BaseFilter(self.queryset, params)
        queryset = f.filter()
        return queryset
    
    @action(detail=True, methods=['GET'], name='set_subtopic_order_up', url_path=r'set-subtopic-order-up')
    def set_subtopic_order_up(self, request, pk, *args, **kwargs):
        subtopic = get_object_or_404(Subtopic, pk=pk)
        prev_subtopic = Subtopic.objects.filter(topic=subtopic.topic, order=subtopic.order-1).first()
        if prev_subtopic:
            subtopic.order = 999
            subtopic.save()
            prev_subtopic.order = prev_subtopic.order + 1
            prev_subtopic.save()
            subtopic.order = prev_subtopic.order - 1
            subtopic.save()
            return Response({'message': 'success'}, status=status.HTTP_200_OK)
        return Response({'message': 'Cannot cannot find previous subtopic'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], name='set_subtopic_order_down', url_path=r'set-subtopic-order-down')
    def set_subtopic_order_down(self, request, pk, *args, **kwargs):
        subtopic = get_object_or_404(Subtopic, pk=pk)
        next_subtopic = Subtopic.objects.filter(topic=subtopic.topic, order=subtopic.order+1).first()
        if next_subtopic:
            subtopic.order = 999
            subtopic.save()
            next_subtopic.order = next_subtopic.order - 1
            next_subtopic.save()
            subtopic.order = next_subtopic.order + 1
            subtopic.save()
            return Response({'message': 'success'}, status=status.HTTP_200_OK)
        return Response({'message': 'Cannot find next subtopic'}, status=status.HTTP_400_BAD_REQUEST)
        