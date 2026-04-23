from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Announcement, CompanyPolicy, CalendarEvent
from .forms import CalendarEventForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin()

# --- Announcements ---
class AnnouncementListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'company/announcements.html'
    context_object_name = 'announcements'
    ordering = ['-date_posted']

class AnnouncementCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Announcement
    template_name = 'company/company_form.html'
    fields = '__all__'
    success_url = reverse_lazy('company:announcement_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Post Announcement'
        return context

class AnnouncementUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Announcement
    template_name = 'company/company_form.html'
    fields = '__all__'
    success_url = reverse_lazy('company:announcement_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Announcement'
        return context

class AnnouncementDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Announcement
    template_name = 'company/company_confirm_delete.html'
    success_url = reverse_lazy('company:announcement_list')

# --- Policies ---
class PolicyListView(LoginRequiredMixin, ListView):
    model = CompanyPolicy
    template_name = 'company/policies.html'
    context_object_name = 'policies'
    ordering = ['-last_updated']

class PolicyCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = CompanyPolicy
    template_name = 'company/company_form.html'
    fields = '__all__'
    success_url = reverse_lazy('company:policy_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Company Policy'
        return context

class PolicyUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = CompanyPolicy
    template_name = 'company/company_form.html'
    fields = '__all__'
    success_url = reverse_lazy('company:policy_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Company Policy'
        return context

class PolicyDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = CompanyPolicy
    template_name = 'company/company_confirm_delete.html'
    success_url = reverse_lazy('company:policy_list')

# --- Calendar ---
class CalendarListView(LoginRequiredMixin, ListView):
    model = CalendarEvent
    template_name = 'company/calendar.html'
    context_object_name = 'events'
    ordering = ['start_date']

class CalendarCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = CalendarEvent
    template_name = 'company/company_form.html'
    form_class = CalendarEventForm
    success_url = reverse_lazy('company:calendar_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Schedule Calendar Event'
        return context

class CalendarUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = CalendarEvent
    template_name = 'company/company_form.html'
    form_class = CalendarEventForm
    success_url = reverse_lazy('company:calendar_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Calendar Event'
        return context

class CalendarDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = CalendarEvent
    template_name = 'company/company_confirm_delete.html'
    success_url = reverse_lazy('company:calendar_list')
