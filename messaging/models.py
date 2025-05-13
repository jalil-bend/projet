from django.db import models
from django.conf import settings

class Conversation(models.Model):
    CONTEXT_CHOICES = (
        ('doctor_doctor', 'Docteur - Docteur'),
        ('doctor_patient', 'Docteur - Patient'),
    )

    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    context_type = models.CharField(max_length=20, choices=CONTEXT_CHOICES, default='doctor_patient')
    deleted_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='deleted_conversations', blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_encrypted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # 🔥 Nouveau champ
    context_type = models.CharField(max_length=20, choices=CONTEXT_CHOICES, default='doctor_patient')

    def __str__(self):
        return f"Conversation {self.id} ({self.context_type})"



class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        related_name='messages',
        on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)  # pour savoir si un message a été modifié
    edited_at = models.DateTimeField(null=True, blank=True)  # date de la modification
    deleted_by_sender = models.BooleanField(default=False)  # soft delete par l'envoyeur

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message de {self.sender} à {self.timestamp}"

class MessageReadReceipt(models.Model):
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='read_receipts'
    )
    reader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('message', 'reader')

    def __str__(self):
        return f"{self.reader} a lu {self.message} à {self.read_at}"






# Create your models here.
