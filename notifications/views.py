from ast import literal_eval

from django.http import HttpResponse, JsonResponse
import requests
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

from django.conf import settings
from notifications.models import Notification, Client, Message
from notifications.serializers import NotificationSerializer, ClientSerializer, MessageSerializer


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

    @action(detail=True)
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
            notify.delay(notification.id, client.id, client.phone, notification.text)
        return JsonResponse({'status': 'OK', 'details': 'Tasks initiated'})

        #     message = Message(notification_id=notification.id, client_id=client.id)
        #     message.save()
        #     request_body = {
        #         "id": message.id,
        #         "phone": client.phone,
        #         "text": notification.text
        #     }
        #     response = requests.post(f"https://probe.fbrq.cloud/v1/send/{message.id}",
        #                              headers={"Authorization": f"Bearer {settings.TOKEN}"},
        #                              json=request_body)
        #     responses[message.id] = response.json()
        # return JsonResponse(responses)


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
