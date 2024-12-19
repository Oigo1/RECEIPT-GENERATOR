
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Payment
import random
import string
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.contrib import messages
import os


def generate_receipt_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


@login_required
def payment_form(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        code = request.POST['code']
        amount = request.POST['amount']
        account_number = request.POST['account_number']
        receipt_number = generate_receipt_number()

        # Save payment to the database
        payment = Payment.objects.create(
            name=name,
            email=email,
            code=code,
            amount=amount,
            account_number=account_number,
            receipt_number=receipt_number,
        )

        # Generate Receipt
        file_path = f'receipt_{receipt_number}.pdf'
        pdf_path = os.path.join('static', 'receipts', file_path)
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.drawString(50, 750, f"Receipt Number: {receipt_number}")
        c.drawString(50, 730, f"Name: {name}")
        c.drawString(50, 710, f"Email: {email}")
        c.drawString(50, 690, f"Code: {code}")
        c.drawString(50, 670, f"Amount: ${amount}")
        c.drawString(50, 650, f"Account Number: {account_number}")
        c.drawString(50, 630, f"Date: {payment.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        c.save()

        return render(request, 'payments/success.html', {
            'receipt_number': receipt_number,
            'download_link': f'/static/receipts/{file_path}',
        })

    return render(request, 'payments/payment_form.html')


def register_view(request):
    if request.method == 'POST':  # This line checks if the request is a POST request
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'payments/register.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'payments/register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)  # Automatically log in the user after registration
        return redirect('payment_form')  # Redirect to the payment form

    return render(request, 'payments/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        from django.contrib.auth import authenticate, login

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('payment_form')  # Redirect to payment form after login
        else:
            return render(request, 'payments/login.html', {'error': 'Invalid username or password'})

    return render(request, 'payments/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')
