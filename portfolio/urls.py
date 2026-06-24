from django.urls import path
from .views import (
    JWTRegisterView, JWTLoginView, RefreshTokenView,
    SendOTPView, VerifyOTPView,
    GoogleOAuthView, GitHubOAuthView,
    ForgotPasswordSendOTP, ForgotPasswordVerifyOTP, ForgotPasswordReset,
    get_home_info, add_home_info,
    get_about_info, add_about_info,
    get_footer_info, add_footer_info,
    get_projects_info, add_projects_info,
    delete_projects_info,
    delete_user_account,
    track_visit, get_analytics,
    CheckSlugView,
    PortfolioLinkView, PublicPortfolioView, edit_projects_info, get_single_project, get_project_detail,
    save_project_detail, generate_cv, profile_links, profile_summary, education_list, education_detail, experience_list,
    experience_detail, certification_list, certification_detail, achievement_list, achievement_detail, language_detail,
    language_list, soft_skill_list, hobby_list, soft_skill_detail, hobby_detail, SettingsView, generate_word_cv,
    CVPreferenceView
)

urlpatterns = [
    # ── JWT Auth ──────────────────────────────────────────────
    path('api/register/',      JWTRegisterView,  name='jwt-register'),
    path('api/login/',         JWTLoginView,     name='jwt-login'),
    path('api/token/refresh/', RefreshTokenView, name='token-refresh'),

    # ── OTP ───────────────────────────────────────────────────
    path('api/send-otp/',   SendOTPView,   name='send-otp'),
    path('api/verify-otp/', VerifyOTPView, name='verify-otp'),

    # ── OAuth ─────────────────────────────────────────────────
    path('api/auth/google/', GoogleOAuthView, name='google-oauth'),
    path('api/auth/github/', GitHubOAuthView, name='github-oauth'),

    # ── Forgot Password ───────────────────────────────────────
    path('api/forgot-password/send-otp/',    ForgotPasswordSendOTP,   name='forgot-send-otp'),
    path('api/forgot-password/verify-otp/',  ForgotPasswordVerifyOTP, name='forgot-verify-otp'),
    path('api/forgot-password/reset/',       ForgotPasswordReset,     name='forgot-reset'),

    # ── Portfolio Data ────────────────────────────────────────
    path('get-home-info/',     get_home_info,     name='get_home_info'),
    path('add-home-info/',     add_home_info,     name='add_home_info'),
    path('get-about-info/',    get_about_info,    name='get_about_info'),
    path('add-about-info/',    add_about_info,    name='add_about_info'),
    path('get-footer-info/',   get_footer_info,   name='get_footer_info'),
    path('add-footer-info/',   add_footer_info,   name='add_footer_info'),
    path('get-projects-info/', get_projects_info, name='get_projects_info'),
    path('add-projects-info/', add_projects_info, name='add_projects_info'),
    path('projects-edit/<int:pk>/', edit_projects_info),
    path('projects-del/<int:pk>/',      delete_projects_info, name='delete_project'),
    path('account-del/<str:username>/', delete_user_account,  name='delete_account'),

    # ── Analytics ─────────────────────────────────────────────
    path('api/track-visit/',              track_visit,   name='track-visit'),
    path('api/analytics/<str:username>/', get_analytics, name='get-analytics'),


    # urlpatterns — add these 3 lines
    path('get-project/<int:pk>/',         get_single_project,  name='get_single_project'),
    path('project-detail/<int:pk>/',      get_project_detail,  name='get_project_detail'),
    path('project-detail/<int:pk>/save/', save_project_detail, name='save_project_detail'),

    # - Slug --------------------------------------------------
    path('portfolio-link/', PortfolioLinkView.as_view()),
    path('portfolio-link/check-slug/', CheckSlugView.as_view()),
    path('portfolio/<str:identifier>/', PublicPortfolioView.as_view(), name='public-portfolio'),

    path('api/cv/<str:username>/', generate_cv, name='generate-cv'),





    # ── Profile ───────────────────────────────────────────────────
    path('api/profile/links/',   profile_links,   name='profile-links'),
    path('api/profile/summary/', profile_summary, name='profile-summary'),

    # ── Education ─────────────────────────────────────────────────
    path('api/education/',        education_list,          name='education-list'),
    path('api/education/<int:pk>/', education_detail,      name='education-detail'),

    # ── Experience ────────────────────────────────────────────────
    path('api/experience/',         experience_list,       name='experience-list'),
    path('api/experience/<int:pk>/', experience_detail,    name='experience-detail'),

    # ── Certifications ────────────────────────────────────────────
    path('api/certifications/',         certification_list,    name='cert-list'),
    path('api/certifications/<int:pk>/', certification_detail, name='cert-detail'),

    # ── Achievements ──────────────────────────────────────────────
    path('api/achievements/',         achievement_list,    name='ach-list'),
    path('api/achievements/<int:pk>/', achievement_detail, name='ach-detail'),

    # ── Languages ─────────────────────────────────────────────────
    path('api/languages/',         language_list,   name='lang-list'),
    path('api/languages/<int:pk>/', language_detail, name='lang-detail'),

    # ── Soft Skills ───────────────────────────────────────────────
    path('api/soft-skills/',         soft_skill_list,   name='soft-list'),
    path('api/soft-skills/<int:pk>/', soft_skill_detail, name='soft-detail'),

    # ── Hobbies ───────────────────────────────────────────────────
    path('api/hobbies/',         hobby_list,   name='hobby-list'),
    path('api/hobbies/<int:pk>/', hobby_detail, name='hobby-detail'),

    # ── CV Generator ──────────────────────────────────────────────
    path('api/cv/<str:username>/', generate_cv, name='generate-cv'),
    path('settings/<str:username>/', SettingsView.as_view()),
    path('cv-word/<str:username>/', generate_word_cv),
    path('cv-preferences/<str:username>/', CVPreferenceView.as_view()),






]
