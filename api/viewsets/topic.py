from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from api.models import Topic
from api.serializers import TopicSerializer
from rest_framework.response import Response
from rest_framework import status
from utils.templating import render_template



class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = []

    @action(detail=True, methods=['GET'], name='set_topic_order_up', url_path=r'set-topic-order-up')
    def set_topic_order_up(self, request, pk, *args, **kwargs):
        topic = get_object_or_404(Topic, pk=pk)
        prev_topic = Topic.objects.filter(subject=topic.subject, order=topic.order-1).first()
        if prev_topic:
            topic.order = 999
            topic.save()
            prev_topic.order = prev_topic.order + 1
            prev_topic.save()
            topic.order = prev_topic.order - 1
            topic.save()
            topics = Topic.objects.filter(subject=topic.subject).all()
            template = render_template('ajax/topic/topic_list.html', {'topics':topics})
            return Response({'template': template}, status=status.HTTP_200_OK)
        return Response({'message': 'Cannot cannot find previous topic'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], name='set_topic_order_down', url_path=r'set-topic-order-down')
    def set_topic_order_down(self, request, pk, *args, **kwargs):
        topic = get_object_or_404(Topic, pk=pk)
        next_topic = Topic.objects.filter(subject=topic.subject, order=topic.order+1).first()
        if next_topic:
            topic.order = 999
            topic.save()
            next_topic.order = next_topic.order - 1
            next_topic.save()
            topic.order = next_topic.order + 1
            topic.save()
            topics = Topic.objects.filter(subject=topic.subject).all()
            template = render_template('ajax/topic/topic_list.html', {'topics':topics})
            return Response({'template': template}, status=status.HTTP_200_OK)
        return Response({'message': 'Cannot find next topic'}, status=status.HTTP_400_BAD_REQUEST)
        
