from notifications.models import Notification, Client, Message


Notification(text="1st notif").save()
Notification(text="A message for all hippies!", filter="([], [hippie])").save()

Client(phone=79245678941).save()
Client(phone=79768989000).save()
Client(phone=79174545678, tag="hippie").save()
