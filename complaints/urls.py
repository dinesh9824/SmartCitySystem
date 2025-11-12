from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('citizen-dashboard/', views.citizen_dashboard, name='citizen_dashboard'),
    path('add-complaint/', views.add_complaint, name='add_complaint'),
    path('edit-complaint/<int:complaint_id>/', views.edit_complaint, name='edit_complaint'),
    path('delete-complaint/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-edit-complaint/<int:complaint_id>/', views.admin_edit_complaint, name='admin_edit_complaint'),
    path('admin-delete-complaint/<int:complaint_id>/', views.admin_delete_complaint, name='admin_delete_complaint'),
    # Electricity Bill URLs
    path('electricity-bills/', views.electricity_bills, name='electricity_bills'),
    path('add-electricity-bill/', views.add_electricity_bill, name='add_electricity_bill'),
    path('edit-electricity-bill/<int:bill_id>/', views.edit_electricity_bill, name='edit_electricity_bill'),
    path('delete-electricity-bill/<int:bill_id>/', views.delete_electricity_bill, name='delete_electricity_bill'),
    path('mark-bill-cleared/<int:bill_id>/', views.mark_bill_cleared, name='mark_bill_cleared'),
    path('admin-electricity-bills/', views.admin_electricity_bills, name='admin_electricity_bills'),
    path('admin-edit-electricity-bill/<int:bill_id>/', views.admin_edit_electricity_bill, name='admin_edit_electricity_bill'),
    path('admin-delete-electricity-bill/<int:bill_id>/', views.admin_delete_electricity_bill, name='admin_delete_electricity_bill'),
    # Message URLs
    path('messages/', views.user_messages, name='user_messages'),
    path('view-message/<int:message_id>/', views.view_message, name='view_message'),
    path('send-message/', views.send_message, name='send_message'),
    path('admin-messages/', views.admin_messages, name='admin_messages'),
]
