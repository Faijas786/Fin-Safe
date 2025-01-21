from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Member model to represent individual members
class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate with logged-in user
    name = models.CharField(max_length=255)
    email = models.EmailField()
    username = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.name

# Transaction model to represent financial transactions
class Transaction(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)  # Use the Member model here
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction of {self.amount} by {self.member.name}"

# Loan model to represent loans associated with members
class Loan(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Paid', 'Paid')])

    def __str__(self):
        return f"Loan of {self.amount} for {self.member.name}"

# Deposit model to represent deposits made by members
class Deposit(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deposit of {self.amount} by {self.member.name}"

# ChatMessage model to represent messages in the group chat
class ChatMessage(models.Model):
    sender = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.sender} - {self.timestamp}"

class Withdraw(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.member.name} - {self.amount}"

# Group model to represent different groups

class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name='custom_groups')  # Add a unique related_name

    def __str__(self):
        return self.name
    
# Membership model to link a user to a group
class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} in {self.group.group_id}'

# Message model to represent messages in the group chat
class Message(models.Model):
    sender = models.CharField(max_length=100)  # Name of the sender
    message = models.TextField()  # The message content
    timestamp = models.DateTimeField(auto_now_add=True)  # When the message was sent

    def __str__(self):
        return f"{self.sender}: {self.message[:30]}..."
