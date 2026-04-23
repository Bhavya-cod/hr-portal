from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserRegistrationForm

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard:home')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')

class SignUpView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'
    success_message = "Your account was created successfully! You can now log in."

from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AccountSettingsForm

class AccountSettingsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = AccountSettingsForm
    template_name = 'accounts/account_settings.html'
    success_message = "Your account settings have been successfully updated."
    
    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('accounts:settings')
