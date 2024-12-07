from django.core.mail import send_mail
from django.views.generic import CreateView
from django.urls import reverse_lazy

from users.forms import UserRegistrationForm
from users.models import User
from django.conf import settings


class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register_form.html'
