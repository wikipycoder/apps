from django.urls import path
from . import views


urlpatterns = [

    path("apps/", views.AppGetView.as_view(), name="apps"),
    path("app/<int:id>/", views.AppUpdateView.as_view(), name="app"),
    path("app/cancel_subscription/<int:id>/", views.CancelAppSubscription.as_view(), name="cancel_subscription"),
    path("user/register", views.UserRegisterView.as_view(), name="register"),
    path("user/login", views.UserLoginView.as_view(), name="login"),
    path("user/logout", views.UserLogoutView.as_view(), name="logout"),
    path("user/reset_password", views.UserResetPasswordView.as_view(), name="password_reset")
]