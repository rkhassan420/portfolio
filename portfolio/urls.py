from django.urls import path
from .views import (
    JWTRegisterView, JWTLoginView, RefreshTokenView,
    SendOTPView, VerifyOTPView,
    get_home_info, add_home_info,
    get_about_info, add_about_info,
    get_footer_info, add_footer_info,
    get_projects_info, add_projects_info,
    delete_projects_info,
    delete_user_account, get_analytics, track_visit, GitHubOAuthView, GoogleOAuthView,
)

urlpatterns = [
    path('api/register/',      JWTRegisterView,  name='jwt-register'),
    path('api/login/',         JWTLoginView,     name='jwt-login'),
    path('api/token/refresh/', RefreshTokenView, name='token-refresh'),
    path('api/send-otp/',      SendOTPView,      name='send-otp'),
    path('api/verify-otp/',    VerifyOTPView,    name='verify-otp'),
    path('get-home-info/',     get_home_info,    name='get_home_info'),
    path('add-home-info/',     add_home_info,    name='add_home_info'),
    path('get-about-info/',    get_about_info,   name='get_about_info'),
    path('add-about-info/',    add_about_info,   name='add_about_info'),
    path('get-footer-info/',   get_footer_info,  name='get_footer_info'),
    path('add-footer-info/',   add_footer_info,  name='add_footer_info'),
    path('get-projects-info/', get_projects_info, name='get_projects_info'),
    path('add-projects-info/', add_projects_info, name='add_projects_info'),
    path('projects-del/<int:pk>/',       delete_projects_info, name='delete_project'),
    path('account-del/<str:username>/',  delete_user_account,  name='delete_account'),

    # ── Analytics ──
    path('api/track-visit/', track_visit, name='track-visit'),
    path('api/analytics/<str:username>/', get_analytics, name='get-analytics'),

    # ── OAuth ─────────────────────────────────────────────────
    path('api/auth/google/', GoogleOAuthView, name='google-oauth'),
    path('api/auth/github/', GitHubOAuthView, name='github-oauth'),

]