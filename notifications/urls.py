from django.urls import path, include
from rest_framework.routers import DefaultRouter
from notifications import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'notifications', views.NotificationViewSet, basename="notification")
router.register(r'clients', views.ClientViewSet, basename="client")
router.register(r'messages', views.MessageViewSet, basename="message")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('statistics/', views.Statistics.as_view()),
    path('statistics/<int:pk>', views.StatisticsDetail.as_view())
]
