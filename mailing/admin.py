from django.contrib import admin
from mailing.models import Recipient, Message

@admin.register(Recipient)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email")

@admin.register(Message)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "body")
