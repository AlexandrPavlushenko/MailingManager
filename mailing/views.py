from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.utils import timezone
from .models import Recipient, Message, Mailing, SendAttempt
from .forms import RecipientForm, MessageForm, MailingForm


# CRUD для получателей (Recipient)

class RecipientListView(generic.ListView):
    model = Recipient
    template_name = 'mailing/recipient_list.html'
    context_object_name = 'recipients'


class RecipientCreateView(generic.CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')


class RecipientUpdateView(generic.UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')


class RecipientDeleteView(generic.DeleteView):
    model = Recipient
    template_name = 'mailing/recipient_confirm_delete.html'
    success_url = reverse_lazy('mailing:recipient_list')


# CRUD для сообщений (Message)

class MessageListView(generic.ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'


class MessageCreateView(generic.CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')


class MessageUpdateView(generic.UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(generic.DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')


# CRUD для рассылок (Mailing)

class MailingListView(generic.ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'


class MailingCreateView(generic.CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingUpdateView(generic.UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        mailing = form.save(commit=False)
        existing_end_at = self.get_object().end_at
        new_end_at = form.cleaned_data.get('end_at')

        if existing_end_at != new_end_at:
            mailing.status = 'Запущена'

        mailing.save()
        return super().form_valid(form)


class MailingDeleteView(generic.DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')


# Генерация отчета и отправка рассылки

class SendMailingView(generic.View):
    def post(self, request, mailing_id):
        mailing = self.get_object(mailing_id)
        recipients = mailing.recipients.all()

        # Инициализация отправки
        for recipient in recipients:
            try:
                send_mail(
                    mailing.message.subject,
                    mailing.message.body,
                    'taborr@yandex.ru',
                    [recipient.email],
                    fail_silently=False,
                )
                status = 'Успешно'
                server_response = 'Письмо отправлено успешно.'
            except Exception as e:
                status = 'Не успешно'
                server_response = str(e)

            # Сохранение попытки рассылки
            SendAttempt.objects.create(
                mailing=mailing,
                status=status,
                server_response=server_response
            )

        # Обновление статуса рассылки
        if mailing.status == 'Создана':
            mailing.status = 'Запущена'
            mailing.first_sent_at = timezone.now()
            mailing.save()

        # Проверка, закончилось ли время рассылки
        if mailing.end_at and timezone.now() > mailing.end_at:
            mailing.status = 'Завершена'
            mailing.save()

        return render(request, 'mailing/mailing_status.html', {'mailing': mailing})


    def get_object(self, mailing_id):
        return Mailing.objects.get(id=mailing_id)


# Статистика для главной страницы

class HomeView(generic.TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status='Запущена').count()
        context['unique_recipients'] = Recipient.objects.values('email').distinct().count()
        return context