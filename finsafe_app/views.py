from django.shortcuts import render, redirect, get_object_or_404
from .models import Member, Transaction, Loan, Deposit, ChatMessage, Withdraw, Message, Group
from .forms import MemberForm, TransactionForm, LoanForm, DepositForm
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal

# Home view

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Check if the user has any members
    if not Member.objects.filter(user=request.user).exists():
        # Create default members for new user
        Member.objects.create(user=request.user, name='Default Member')
    
    return render(request, 'home.html')

# Member list view
def member_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Fetch members associated with the logged-in user
    members = Member.objects.filter(user=request.user)

    # Calculate total deposit for each member
    for member in members:
        total_deposit = Deposit.objects.filter(member=member).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        member.total_deposit = total_deposit

    return render(request, 'members/member_list.html', {'members': members})

# Transaction history view for a specific member
def transaction_history(request, member_id): 
    if not request.user.is_authenticated:
        return redirect('login')

    # Ensure the member belongs to the logged-in user
    member = get_object_or_404(Member, id=member_id, user=request.user)

    # Get all transactions for the member
    transactions = Transaction.objects.filter(member=member)

    # Calculate the total transaction amount
    total_transaction_amount = transactions.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    # Adjust as per your model relationship
    member = get_object_or_404(Member, id=member_id)
    transactions = member.transactions.all()

    return render(request, 'transactions/transaction_history.html', {
        'transactions': transactions,
        'total_transaction_amount': total_transaction_amount,
        'member': member
    })
# Loan history view for a specific member
def loan_history(request, member_id):
    # Ensure the member belongs to the logged-in user
    member = get_object_or_404(Member, id=member_id, user=request.user)

    # Get loans for the member
    loans = Loan.objects.filter(member=member)
    total_amount = loans.filter(status='Pending').aggregate(total=Sum('amount'))['total'] or Decimal('0')
    return render(request, 'loans/loan_history.html', {'loans': loans, 'member_id': member_id, 'total_amount': total_amount})


def add_loan(request, member_id):
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        member = Member.objects.get(id=member_id)
        Loan.objects.create(member=member, amount=amount, status='Pending')
        return redirect('loan_history', member_id=member_id)
    return redirect('loan_history', member_id=member_id)

def pay_loan(request, member_id):
    if request.method == 'POST':
        pay_amount = Decimal(request.POST.get('pay_amount'))
        loans = Loan.objects.filter(member__id=member_id, status='Pending').order_by('id')
        for loan in loans:
            if pay_amount <= 0:
                break
            if loan.amount <= pay_amount:
                pay_amount -= loan.amount
                loan.amount = Decimal('0')
                loan.status = 'Paid'
            else:
                loan.amount -= pay_amount
                pay_amount = Decimal('0')
            loan.save()
        return redirect('loan_history', member_id=member_id)
    return redirect('loan_history', member_id=member_id)

# Deposit history view for a specific member
def deposit_history(request, member_id):
    # Ensure the member belongs to the logged-in user
    member = get_object_or_404(Member, id=member_id, user=request.user)

    # Get deposits for the member
    deposits = Deposit.objects.filter(member=member)

    # Calculate the total deposit amount
    total_deposit = deposits.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    if request.method == 'POST':
        if 'deposit_amount' in request.POST:
            deposit_amount = float(request.POST.get('deposit_amount'))
            Deposit.objects.create(amount=deposit_amount, member=member)
            messages.success(request, f'₹ {deposit_amount} deposited successfully.')

        elif 'withdrawal_amount' in request.POST:
            withdrawal_amount = float(request.POST.get('withdrawal_amount'))
            if withdrawal_amount <= total_deposit:
                Withdraw.objects.create(amount=withdrawal_amount, member=member)
                Deposit.objects.create(amount=-withdrawal_amount, member=member)
                messages.success(request, f'₹ {withdrawal_amount} withdrawn successfully.')
            else:
                messages.error(request, 'Insufficient balance to withdraw.')

        return redirect('deposit_history', member_id=member_id)

    return render(request, 'deposits/deposit_history.html', {
        'deposits': deposits,
        'total_deposit': total_deposit,
        'member': member,
    })

# Add a new member
def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.user = request.user  # Associate the logged-in user
            member.save()
            return redirect('member_list')
    else:
        form = MemberForm()
    return render(request, 'members/add_member.html', {'form': form})
# Add a new transaction
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_history', member_id=form.cleaned_data['member'].id)
    else:
        form = TransactionForm()
    return render(request, 'transactions/add_transaction.html', {'form': form})

# Group chat view
def group_chat(request):
    if request.method == 'POST':
        sender = request.POST.get('sender')
        message = request.POST.get('message')

        if sender and message:
            Message.objects.create(sender=sender, message=message)
            return redirect('group_chat')  # Redirect to avoid form resubmission

    messages = Message.objects.order_by('timestamp')  # Fetch messages in order
    return render(request, 'group_chat.html', {'messages': messages})

def account(request):
    if request.method == "POST":
        # Handle login
        if "login_form" in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("account_details")
            else:
                messages.error(request, "Invalid username or password.")
        
        # Handle registration
        elif "register_form" in request.POST:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            group_name = request.POST.get("group_name")

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered.")
            else:
                try:
                    # Create user
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()

                    # Assign user to a group
                    group, created = Group.objects.get_or_create(name=group_name)
                    group.user_set.add(user)

                    messages.success(request, "Registration successful. Please log in.")
                    return redirect("account")
                except Exception as e:
                    messages.error(request, f"An error occurred: {e}")

    return render(request, "account.html")

def account_view(request):
    if request.method == "POST":
        if "login_form" in request.POST:
            # Handle login
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("account_details")  # Redirect to account details page
            else:
                messages.error(request, "Invalid username or password.")
        
        elif "register_form" in request.POST:
            # Handle registration
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            else:
                User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, "Registration successful. Please log in.")
                return redirect("account")  # Redirect to login after registration

    return render(request, "account.html")


@login_required
def account_details(request):
    try:
        # Get the logged-in user's member profile
        member = Member.objects.get(username=request.user.username)
        # Filter transactions for the member
        transactions = Transaction.objects.filter(member=member)
    except Member.DoesNotExist:
        transactions = []  # If the member doesn't exist, show no transactions
    
    return render(request, "account_details.html", {"transactions": transactions})

def logout_view(request):
    logout(request)
    return redirect('login')