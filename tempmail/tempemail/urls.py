from django.urls import path
from .views import GenerateRandomMailbox, CheckMessages, index

urlpatterns = [
    path('', index, name='index'),
    path('generate-mailbox/', GenerateRandomMailbox.as_view(), name='generate_mailbox'),
    path('check-messages/', CheckMessages.as_view(), name='check_messages'),
]
