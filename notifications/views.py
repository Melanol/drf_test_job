from ast import literal_eval

from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.serializers import *


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'notifications': reverse('notifications-list', request=request, format=format)
    })


class NotificationViewSet(viewsets.ModelViewSet):
    """
    List all notifications, create a new notification and send messages.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    @action(detail=True, methods=['post'])
    def send(self, request, *args, **kwargs):  # TODO: Uses GET instead of POST
        from notifications.tasks import add, notify
        # add.delay(23, 2)
        notification = self.get_object()
        clients = Client.objects.all()

        # Filtering
        if notification.filter:
            filter = literal_eval(notification.filter)  # Safe version of eval
            operator_codes, tags = filter
            out_clients = []
            for client in clients:
                if str(client.phone)[1:4] in operator_codes or client.tag in tags:
                    out_clients.append(client)
            clients = out_clients

        # Send messages
        responses = {}
        for client in clients:
            notify.delay(notification.id,
                         client.id,
                         client.phone,
                         notification.text,
                         notification.send_time,
                         notification.stop_sending_time)
        return JsonResponse({'status': 'OK', 'details': 'Tasks initiated'})


class ClientViewSet(viewsets.ModelViewSet):
    """
    List all clients, or create a new client.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
    List all messages, or create a new message.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class Statistics(APIView):
    def get(self, request, format=None):
        messages = Message.objects.all().values('delivery_status').annotate(total=Count('delivery_status'))
        arr = []
        for el in messages:
            arr.append(el)
        return JsonResponse(arr, safe=False)


class StatisticsDetail(APIView):
    def get(self, request, pk, format=None):
        message_agg = Message.objects.filter(notification_id=pk).values('delivery_status').annotate(total=Count('delivery_status'))
        arr = []
        for el in message_agg:
            message_ids = Message.objects.filter(notification_id=pk).filter(delivery_status=el['delivery_status']).values('id')
            message_ids = [el['id'] for el in list(message_ids)]
            el['message_ids'] = str(message_ids)
            arr.append(el)
        return JsonResponse(arr, safe=False)
