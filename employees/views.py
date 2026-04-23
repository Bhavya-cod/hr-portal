from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import AdminEmployeeCreationForm, AdminEmployeeUpdateForm
from accounts.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView

@login_required
def employee_list(request):
    if not request.user.is_admin():
        return HttpResponse("Unauthorized", status=403)
    
    from accounts.models import User
    employees = User.objects.filter(role=User.Role.EMPLOYEE).select_related('profile')
    
    return render(request, 'employees/list.html', {'employees': employees})

class EmployeeCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    form_class = AdminEmployeeCreationForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employees:employee_list')
    success_message = "Employee added successfully!"

    def test_func(self):
        return self.request.user.is_admin()

class EmployeeUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = AdminEmployeeUpdateForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employees:employee_list')
    success_message = "Employee updated successfully!"
    
    def test_func(self):
        return self.request.user.is_admin()
        
    def get_queryset(self):
        return User.objects.filter(role=User.Role.EMPLOYEE)

class EmployeeDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'employees/employee_confirm_delete.html'
    success_url = reverse_lazy('employees:employee_list')
    success_message = "Employee deleted successfully!"
    
    def test_func(self):
        return self.request.user.is_admin()
        
    def get_queryset(self):
        return User.objects.filter(role=User.Role.EMPLOYEE)

@login_required
def task_manage(request, pk):
    if not request.user.is_admin():
        return HttpResponse("Unauthorized", status=403)
        
    employee = User.objects.get(pk=pk, role=User.Role.EMPLOYEE)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            from .models import EmployeeTask
            EmployeeTask.objects.create(employee=employee, title=title)
            
    from .models import EmployeeTask
    tasks = EmployeeTask.objects.filter(employee=employee).order_by('is_completed', '-created_at')
    
    return render(request, 'employees/task_manage.html', {'employee': employee, 'tasks': tasks})

@login_required
def task_complete(request, pk):
    if request.method != 'POST':
        return HttpResponse("Method not allowed", status=405)
        
    from .models import EmployeeTask
    try:
        task = EmployeeTask.objects.get(pk=pk, employee=request.user)
        task.is_completed = True
        task.save()
        # Return empty response to HTMX so the ticket disappears from the DOM
        return HttpResponse("")
    except EmployeeTask.DoesNotExist:
        return HttpResponse("Not found", status=404)

@login_required
def document_manage(request):
    from .models import EmployeeDocument
    from .forms import EmployeeDocumentForm
    
    if request.method == 'POST':
        form = EmployeeDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.employee = request.user
            doc.save()
            return redirect('employees:document_manage')
    else:
        form = EmployeeDocumentForm()
        
    documents = EmployeeDocument.objects.filter(employee=request.user)
    return render(request, 'employees/documents.html', {'form': form, 'documents': documents})

@login_required
def document_delete(request, pk):
    if request.method != 'POST':
        return HttpResponse("Method not allowed", status=405)
        
    from .models import EmployeeDocument
    doc = get_object_or_404(EmployeeDocument, pk=pk, employee=request.user)
    doc.delete()
    return redirect('employees:document_manage')

from .forms import PerformanceFeedbackForm, HRPerformanceFeedbackForm
from .models import PerformanceFeedback

@login_required
def feedback_submit(request):
    """View for employees to submit feedback for themselves or colleagues"""
    if request.method == 'POST':
        form = PerformanceFeedbackForm(request.POST, user=request.user)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.reviewer = request.user
            # Check if it's self-evaluation
            feedback.is_self_evaluation = (feedback.employee == request.user)
            feedback.save()
            return redirect('employees:feedback_submit')
    else:
        form = PerformanceFeedbackForm(user=request.user)
    
    # Show feedback received by others AND feedback given by this user
    feedback_received = PerformanceFeedback.objects.filter(employee=request.user).order_by('-created_at')
    feedback_given = PerformanceFeedback.objects.filter(reviewer=request.user).exclude(employee=request.user).order_by('-created_at')
    
    return render(request, 'employees/feedback_submit.html', {
        'form': form, 
        'feedback_received': feedback_received,
        'feedback_given': feedback_given
    })

@login_required
def hr_feedback_manage(request):
    """View for HR/Admin to give feedback to employees"""
    if not request.user.is_admin():
        return HttpResponse("Unauthorized", status=403)
        
    if request.method == 'POST':
        form = HRPerformanceFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.reviewer = request.user
            feedback.is_self_evaluation = False
            feedback.save()
            return redirect('employees:hr_feedback_manage')
    else:
        form = HRPerformanceFeedbackForm()
        
    all_feedback = PerformanceFeedback.objects.all().select_related('employee', 'reviewer')
    return render(request, 'employees/hr_feedback_manage.html', {'form': form, 'all_feedback': all_feedback})
