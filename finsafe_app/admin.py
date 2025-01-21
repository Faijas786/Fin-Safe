from django.contrib import admin
from .models import Member, Transaction, Loan, Deposit, ChatMessage

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'username', 'balance')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('member', 'amount', 'date', 'description')
    list_filter = ('date',)
    search_fields = ('member__name', 'description')

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('member', 'amount', 'date', 'status')  # Use correct field names
    list_filter = ('status', 'date')

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('member', 'amount', 'date')  # Use correct field names
    list_filter = ('date',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'message', 'timestamp')  # Ensure correct fields
    list_filter = ('timestamp',)
