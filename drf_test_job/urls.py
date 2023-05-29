from django.urls import path, include

urlpatterns = [
    path('', include('notifications.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
