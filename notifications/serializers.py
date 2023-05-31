from rest_framework import serializers
from notifications.models import Notification, Client, Message
from timezone_field.rest_framework import TimeZoneSerializerField


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    send = serializers.HyperlinkedIdentityField(view_name='notification-send', format='html')

    class Meta:
        model = Notification
        fields = ['url', 'id', 'send', 'send_time', 'text', 'filter', 'stop_sending_time']


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    timezone = TimeZoneSerializerField()

    class Meta:
        model = Client
        fields = ['url', 'id', 'phone', 'operator_code', 'tag', 'timezone']

    def validate(self, data):
        """
        Check that the phone number is in the 7XXXXXXXXXX form and the client is not already in the database.
        """
        if data['phone'] < 70000000000 or data['phone'] > 79999999999:
            raise serializers.ValidationError("Enter phone in the 7XXXXXXXXXX form")
        return data


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ['url', 'id', 'delivery_init_time', 'delivered_time', 'delivery_status', 'notification_id', 'client_id']
