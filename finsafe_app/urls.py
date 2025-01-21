from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('members/', views.member_list, name='member_list'),
    path('members/<int:member_id>/transactions/', views.transaction_history, name='transaction_history'),
    path('members/<int:member_id>/loans/', views.loan_history, name='loan_history'),
    path('members/<int:member_id>/loans/add/', views.add_loan, name='add_loan'),
    path('members/<int:member_id>/loans/pay/', views.pay_loan, name='pay_loan'),
    path('members/<int:member_id>/deposits/', views.deposit_history, name='deposit_history'),   
    path('members/add/', views.add_member, name='add_member'),
    path('transactions/add/', views.add_transaction, name='add_transaction'),
    path('group_chat/', views.group_chat, name='group_chat'),  # Corrected path
    path('', views.account, name='account'),
    path('login/', views.account, name='login'),  # Add this line
    path('account/details/', views.account_details, name='account_details'),
    path('logout/', views.logout_view, name='logout'),
]
