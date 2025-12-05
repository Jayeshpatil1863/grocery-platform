from django.urls import path
from . import views as v
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('add', v.add_user, name="add"),
    path('login', v.login_user, name="login"),
    path('logout', v.logout_user, name="logout"),
    path('detail/<int:id>/', v.product_detail, name='detail'),
    path('add_review/<int:id>/', v.add_review, name='add_review'),
    path('review/<int:review_id>/delete/', v.delete_review, name='delete_review'),
    # path('forgot_password/', v.forgot_password, name='forgot_password'),
    # path('verify-otp/', v.verify_otp, name='verify_otp'),
    # path('reset-password/', v.reset_password, name='reset_password'),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name="password_reset"),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),
]
