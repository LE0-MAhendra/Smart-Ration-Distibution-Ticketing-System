from django.urls import path
from . import views

urlpatterns = [
    path("", views.supplier_login_view, name="supplier_login"),
    path("dashboard/", views.supplier_dashboard_view, name="supplier_dashboard"),
    path(
        "user/book/<str:ration_card>/<int:session_id>/",
        views.user_booking_form,
        name="user_booking_with_card",
    ),
    path(
        "profile/update/", views.supplier_profile_update, name="supplier_profile_update"
    ),
    path("register/", views.supplier_register_view, name="supplier_register"),
    path(
        "user/status/<str:ration_card_number>/",
        views.user_ticket_status,
        name="user_status",
    ),
    path(
        "ticket/update/<int:booking_id>/",
        views.update_ticket_status,
        name="update_ticket_status",
    ),
    path("logout", views.logout_view, name="logout"),
]
