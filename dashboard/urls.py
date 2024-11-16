
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('comparison', views.comparison, name='comparison'),
    path('visualization', views.visualization, name='visualization'),
    path('api/excludedEmails', views.excluded_emails, name='excluded_emails'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('api/getMissingFiles', views.get_missing_files, name='get_missing_files'),

]
