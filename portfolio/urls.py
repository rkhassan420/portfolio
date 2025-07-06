# portfolio/urls.py

from django.urls import path

from .views import add_home_info, get_home_info, get_about_info, add_about_info, get_footer_info, add_footer_info, \
    add_projects_info, RegisterView, GetCrsfToken, LoginView, LogoutView, \
    get_projects_info, delete_projects_info \

urlpatterns = [

    path('RegisterUser/', RegisterView, name='RegisterUser'),
    path('LoginUser/', LoginView, name='LoginUser'),
    path('LogoutUser/', LogoutView, name='LogoutUser'),
    path('csrf/', GetCrsfToken, name='GetCsrfToken'),

    path('get-home-info/', get_home_info, name='get_home_info'),
    path('add-home-info/', add_home_info, name='add_home_info'),

    path('get-about-info/', get_about_info, name='get_about_info'),
    path('add-about-info/', add_about_info, name='add_about_info'),

    path('get-footer-info/', get_footer_info, name='get_footer_info'),
    path('add-footer-info/', add_footer_info, name='add_footer_info'),

    path('get-projects-info/', get_projects_info, name='get_projects_info'),
    path('add-projects-info/', add_projects_info, name='add_projects_info'),

    path('projects-del/<int:pk>/', delete_projects_info),

]
