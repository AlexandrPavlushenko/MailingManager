from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import UpdateView

from users.forms import UserRegistrationForm, UserProfileForm
from users.models import User

class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register_form.html'

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        user = form.get_user()

        # Проверка, является ли пользователь заблокированным
        if user.is_blocked:
            messages.error(self.request, "Вы заблокированы администрацией сайта.")
            return redirect(reverse('users:login'))  # Назад на страницу входа

        return super().form_valid(form)  # Если не заблокирован, выполняем стандартный процесс входа

    def get_success_url(self):
        return reverse('mailing:home')

class UserProfileUpdateView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_form.html'
    success_url = reverse_lazy('mailing:home')

    def get_object(self, queryset=None):
        return self.request.user  # Возвращаем текущего пользователя


