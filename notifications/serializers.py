from rest_framework import serializers
from notifications.models import Notification, Client, Message


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    send = serializers.HyperlinkedIdentityField(view_name='notification-send', format='html')

    class Meta:
        model = Notification
        fields = ['id', 'send', 'send_time', 'text', 'filter', 'stop_sending_time']


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'phone', 'operator_code', 'tag', 'timezone']


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sent_time', 'delivery_status', 'notification_id', 'client_id']
