from django.urls import path
from account.views.views import register, login_view, logout_view, profile_view, edit_profile
from utils.email import send_email_confirm
from django.contrib.auth import views as auth_views


app_name = 'account'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('edit_profile/', edit_profile, name='edit_profile'),

    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
         name='password_change'),

    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
         name='password_change_done'),

    path("confirm_email/", send_email_confirm, name="confirm_email"),

    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="password_reset/form.html",
        email_template_name="password_reset/email.html",
        success_url="done/"
    ), name="password_reset"),

    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="password_reset/done.html"
    ), name="password_reset_done"),

    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset/confirm.html"
    ), name="password_reset_confirm"),

    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="password_reset/complete.html"
    ), name="password_reset_complete")
]
