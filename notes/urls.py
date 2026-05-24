# urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterView, LoginView, NoteListCreateView, NoteDetailView, ForgotPasswordView, VerifyCodeView, \
    ResetPasswordView, DeleteUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("notes/", NoteListCreateView.as_view(), name="note-list-create"),
    path("notes/<int:pk>/", NoteDetailView.as_view(), name="note-detail"),

    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("verify/", VerifyCodeView.as_view(), name="verify-code"),
    path("reset/", ResetPasswordView.as_view(), name="reset"),

    path("users/<int:user_id>/", DeleteUserView.as_view(), name="delete-user"),
]



