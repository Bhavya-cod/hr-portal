from django.urls import path
from .views import employee_list, EmployeeCreateView, EmployeeUpdateView, EmployeeDeleteView
from . import views

app_name = 'employees'

urlpatterns = [
    path('list/', employee_list, name='employee_list'),
    path('add/', EmployeeCreateView.as_view(), name='employee_add'),
    path('<int:pk>/edit/', EmployeeUpdateView.as_view(), name='employee_edit'),
    path('<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),
    path('<int:pk>/tasks/', views.task_manage, name='task_manage'),
    path('tasks/<int:pk>/complete/', views.task_complete, name='task_complete'),
    path('documents/', views.document_manage, name='document_manage'),
    path('documents/<int:pk>/delete/', views.document_delete, name='document_delete'),
    path('feedback/', views.feedback_submit, name='feedback_submit'),
    path('hr/feedback/', views.hr_feedback_manage, name='hr_feedback_manage'),
]
