from django.contrib import admin
from django.urls import path
from . import views
from .views import inbox_view

app_name = 'messaging'

urlpatterns = [
    path('start/<int:user_id>/', views.start_conversation, name='start_conversation'),
    path('messagerie/', views.inbox_view, name='inbox'),
    path('chat/<int:conversation_id>/', views.chat_view, name='chat_view'),
    path('get-messages/<int:conversation_id>/', views.get_messages, name='get_messages'),
    path('delete-conversation/<int:conversation_id>/', views.delete_conversation, name='delete_conversation'),
    path('export-conversation/<int:conversation_id>/', views.export_conversation_json, name='export_conversation_json'),
    path('set-typing-status/<int:conversation_id>/', views.set_typing_status, name='set_typing_status'),
    path('typing-status/<int:conversation_id>/', views.update_typing_status, name='update_typing_status'),
    path('unread-count/', views.get_unread_message_count, name='unread_message_count'),

]
