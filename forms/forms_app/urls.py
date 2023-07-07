from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('form/<str:form_name>', views.form_details, name='form_details'), # for creator
    path('form_fill/<str:form_name>', views.form_fill, name='form_fill'), # for user
]
