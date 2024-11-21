from django import forms
from .models import Recipient, Message, Mailing

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['email', 'full_name', 'comment']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['end_at', 'message', 'recipients']

    recipients = forms.ModelMultipleChoiceField(
        queryset=Recipient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields['recipients'].queryset = Recipient.objects.all()