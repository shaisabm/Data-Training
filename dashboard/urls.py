
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('comparison', views.comparison, name='comparison'),
    path('visualization', views.visualization, name='visualization'),
    path('api/excludedEmails', views.excluded_emails, name='excluded_emails'),

]
