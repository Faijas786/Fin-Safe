from django import forms
from .models import Member, Transaction, Loan, Deposit


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'username', 'balance'] 

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['member', 'amount', 'description']

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['member', 'amount', 'status']

class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['member', 'amount']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    