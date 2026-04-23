from django.urls import path
from .views import home, global_search

app_name = 'dashboard'

urlpatterns = [
    path('', home, name='home'),
    path('search/', global_search, name='search'),
]
