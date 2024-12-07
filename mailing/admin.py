from django.contrib import admin
from mailing.models import Recipient, Message

@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "body")
