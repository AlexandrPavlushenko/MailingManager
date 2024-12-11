from django.shortcuts import render,redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.utils import timezone

from users.models import User
from .models import Recipient, Message, Mailing, SendAttempt
from .forms import RecipientForm, MessageForm, MailingForm
from django.contrib.auth.mixins import LoginRequiredMixin


# CRUD для получателей (Recipient)

class RecipientListView(LoginRequiredMixin, generic.ListView):
    model = Recipient
    template_name = 'mailing/recipient_list.html'
    context_object_name = 'recipients'
    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user)


class RecipientCreateView(generic.CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipient_list')

    def form_valid(self, form):
        recipient = form.save(commit=False)
        recipient.owner = self.request.user
        recipient.save()
        return super().form_valid(form)


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

class MessageListView(LoginRequiredMixin, generic.ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(generic.CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        message = form.save(commit=False)
        message.owner = self.request.user
        message.save()
        return super().form_valid(form)


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

class MailingListView(LoginRequiredMixin, generic.ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='manager').exists():
            return Mailing.objects.all()
        else:
            return Mailing.objects.filter(owner=user)


class MailingCreateView(generic.CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        kwargs = super(MailingCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.owner = self.request.user
        mailing.save()
        return super().form_valid(form)

class MailingUpdateView(generic.UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        kwargs = super(MailingUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.owner = self.request.user
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
    def get_object(self, mailing_id):
        return get_object_or_404(Mailing, id=mailing_id)

    def post(self, request, mailing_id):
        mailing = self.get_object(mailing_id)
        recipients = mailing.recipients.all()

        total_sent = 0
        successful_sends = 0
        failed_sends = 0

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
                successful_sends += 1
            except Exception as e:
                status = 'Не успешно'
                server_response = str(e)
                failed_sends += 1

            total_sent += 1

            # Сохранение попытки рассылки
            SendAttempt.objects.create(
                mailing=mailing,
                status=status,
                server_response=server_response,
                recipient=recipient,
                owner=request.user,
                message=mailing.message
            )

        # Обновление статистики рассылки
        mailing.total_sent += total_sent
        mailing.successful_sends += successful_sends
        mailing.failed_sends += failed_sends
        mailing.save()

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


# Статистика для главной страницы

class HomeView(generic.TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if not user.is_authenticated or user.groups.filter(name='manager').exists():
            context['total_mailings'] = Mailing.objects.count()
            context['active_mailings'] = Mailing.objects.filter(status='Запущена').count()
            context['unique_recipients'] = Recipient.objects.values('email').distinct().count()
        else:
            context['successful_attempts'] = SendAttempt.objects.filter(owner=user, status='Успешно').count()
            context['failed_attempts'] = SendAttempt.objects.filter(owner=user, status='Не успешно').count()
            context['sent_messages'] = SendAttempt.objects.filter(owner=user).count()

        return context


class UsersView(generic.TemplateView):
    template_name = 'mailing/list_users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(groups__name='manager')
        return context

class UserActionView(generic.View):

    def post(self, request, user_id, action):
        user = get_object_or_404(User, id=user_id)
        if action == 'block':
            user.is_blocked = True
        elif action == 'unblock':
            user.is_blocked = False
        user.save()
        return redirect('mailing:list_users')