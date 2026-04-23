from django.urls import path
from .views import check_status, perform_action, summary, export_csv, apply_leave, approve_leave, reject_leave

app_name = 'attendance'

urlpatterns = [
    path('status/', check_status, name='check_status'),
    path('action/', perform_action, name='perform_action'),
    path('summary/', summary, name='summary'),
    path('export/', export_csv, name='export_csv'),
    path('leave/apply/', apply_leave, name='apply_leave'),
    path('leave/approve/<int:pk>/', approve_leave, name='approve_leave'),
    path('leave/reject/<int:pk>/', reject_leave, name='reject_leave'),
]
