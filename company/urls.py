from django.urls import path
from . import views

app_name = 'company'

urlpatterns = [
    # Announcements
    path('announcements/', views.AnnouncementListView.as_view(), name='announcement_list'),
    path('announcements/add/', views.AnnouncementCreateView.as_view(), name='announcement_add'),
    path('announcements/<int:pk>/edit/', views.AnnouncementUpdateView.as_view(), name='announcement_edit'),
    path('announcements/<int:pk>/delete/', views.AnnouncementDeleteView.as_view(), name='announcement_delete'),
    
    # Policies
    path('policies/', views.PolicyListView.as_view(), name='policy_list'),
    path('policies/add/', views.PolicyCreateView.as_view(), name='policy_add'),
    path('policies/<int:pk>/edit/', views.PolicyUpdateView.as_view(), name='policy_edit'),
    path('policies/<int:pk>/delete/', views.PolicyDeleteView.as_view(), name='policy_delete'),
    
    # Calendar
    path('calendar/', views.CalendarListView.as_view(), name='calendar_list'),
    path('calendar/add/', views.CalendarCreateView.as_view(), name='calendar_add'),
    path('calendar/<int:pk>/edit/', views.CalendarUpdateView.as_view(), name='calendar_edit'),
    path('calendar/<int:pk>/delete/', views.CalendarDeleteView.as_view(), name='calendar_delete'),
]
