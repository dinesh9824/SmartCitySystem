from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .models import Complaint, ElectricityBill, Message
from .forms import RegistrationForm, ComplaintForm, ComplaintUpdateForm, ElectricityBillForm, ElectricityBillUpdateForm, MessageForm


def home(request):
    return render(request, 'home.html')


def register_view(request):
    if request.method == 'POST':
        print("Registration form submitted")  # Debug
        form = RegistrationForm(request.POST)
        print(f"Form is valid: {form.is_valid()}")  # Debug
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Registration successful! Welcome to Smart City System.')
                return redirect('citizen_dashboard')
            except Exception as e:
                print(f"Registration error: {str(e)}")  # Debug
                messages.error(request, f'Registration failed: {str(e)}')
        else:
            print(f"Form errors: {form.errors}")  # Debug
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        print("Login form submitted")  # Debug
        form = AuthenticationForm(request, data=request.POST)
        print(f"Form is valid: {form.is_valid()}")  # Debug
        if form.is_valid():
            try:
                user = form.get_user()
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('citizen_dashboard')
            except Exception as e:
                print(f"Login error: {str(e)}")  # Debug
                messages.error(request, f'Login failed: {str(e)}')
        else:
            print(f"Form errors: {form.errors}")  # Debug
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def citizen_dashboard(request):
    complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'citizen_dashboard.html', {'complaints': complaints})


@login_required
def add_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            messages.success(request, 'Complaint submitted successfully!')
            return redirect('citizen_dashboard')
    else:
        form = ComplaintForm()
    return render(request, 'add_complaint.html', {'form': form})


@login_required
def edit_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id, user=request.user)
    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            messages.success(request, 'Complaint updated successfully!')
            return redirect('citizen_dashboard')
    else:
        form = ComplaintForm(instance=complaint)
    return render(request, 'edit_complaint.html', {'form': form, 'complaint': complaint})


@login_required
def delete_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id, user=request.user)
    if request.method == 'POST':
        complaint.delete()
        messages.success(request, 'Complaint deleted successfully!')
        return redirect('citizen_dashboard')
    return render(request, 'delete_complaint.html', {'complaint': complaint})


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('citizen_dashboard')
    
    complaints = Complaint.objects.all()
    return render(request, 'admin_dashboard.html', {'complaints': complaints})


@login_required
def admin_edit_complaint(request, complaint_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('citizen_dashboard')
    
    complaint = get_object_or_404(Complaint, id=complaint_id)
    old_status = complaint.status
    
    if request.method == 'POST':
        form = ComplaintUpdateForm(request.POST, instance=complaint)
        if form.is_valid():
            complaint = form.save()
            # Send email notification if status changed
            if old_status != complaint.status:
                send_status_notification(complaint)
            messages.success(request, 'Complaint updated successfully!')
            return redirect('admin_dashboard')
    else:
        form = ComplaintUpdateForm(instance=complaint)
    return render(request, 'admin_edit_complaint.html', {'form': form, 'complaint': complaint})


@login_required
def admin_delete_complaint(request, complaint_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('citizen_dashboard')
    
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if request.method == 'POST':
        complaint.delete()
        messages.success(request, 'Complaint deleted successfully!')
        return redirect('admin_dashboard')
    return render(request, 'admin_delete_complaint.html', {'complaint': complaint})


def send_status_notification(complaint):
    """Send email notification when complaint status changes"""
    subject = f'Complaint Status Update: {complaint.title}'
    message = f'''
Dear {complaint.user.first_name},

Your complaint "{complaint.title}" status has been updated to: {complaint.get_status_display()}

Category: {complaint.get_category_display()}
Description: {complaint.description}

Thank you for using Smart City System.

Best regards,
Smart City Administration
    '''
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER or 'noreply@smartcity.com',
        [complaint.user.email],
        fail_silently=False,
    )


# Electricity Bill Views
@login_required
def electricity_bills(request):
    # Show only the current user's bills
    bills = ElectricityBill.objects.filter(user=request.user).order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    if search_query:
        bills = bills.filter(
            Q(bill_number__icontains=search_query) |
            Q(consumer_name__icontains=search_query)
        )
    
    if status_filter:
        bills = bills.filter(status=status_filter)
    
    # Get user's personal statistics
    user_total = bills.count()
    user_due = bills.filter(status='Due').count()
    user_cleared = bills.filter(status='Cleared').count()
    user_amount = sum(bill.amount for bill in bills)
    
    context = {
        'bills': bills,
        'user_total': user_total,
        'user_due': user_due,
        'user_cleared': user_cleared,
        'user_amount': user_amount,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'electricity_bills.html', context)


@login_required
def add_electricity_bill(request):
    # Only admin users can add electricity bills
    if not request.user.is_staff:
        messages.error(request, 'Only administrators can add electricity bills.')
        return redirect('electricity_bills')
    
    if request.method == 'POST':
        form = ElectricityBillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.user = request.user
            bill.save()
            messages.success(request, 'Electricity bill added successfully!')
            return redirect('admin_electricity_bills')
    else:
        form = ElectricityBillForm()
    return render(request, 'add_electricity_bill.html', {'form': form})


@login_required
def edit_electricity_bill(request, bill_id):
    bill = get_object_or_404(ElectricityBill, id=bill_id, user=request.user)
    if request.method == 'POST':
        form = ElectricityBillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Electricity bill updated successfully!')
            return redirect('electricity_bills')
    else:
        form = ElectricityBillForm(instance=bill)
    return render(request, 'edit_electricity_bill.html', {'form': form, 'bill': bill})


@login_required
def delete_electricity_bill(request, bill_id):
    bill = get_object_or_404(ElectricityBill, id=bill_id, user=request.user)
    if request.method == 'POST':
        bill.delete()
        messages.success(request, 'Electricity bill deleted successfully!')
        return redirect('electricity_bills')
    return render(request, 'delete_electricity_bill.html', {'bill': bill})


@login_required
def mark_bill_cleared(request, bill_id):
    bill = get_object_or_404(ElectricityBill, id=bill_id, user=request.user)
    if request.method == 'POST':
        bill.status = 'Cleared'
        bill.save()
        messages.success(request, 'Bill marked as cleared!')
        return redirect('electricity_bills')
    return render(request, 'mark_bill_cleared.html', {'bill': bill})


@login_required
def admin_electricity_bills(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('electricity_bills')
    
    bills = ElectricityBill.objects.all()
    return render(request, 'admin_electricity_bills.html', {'bills': bills})


@login_required
def admin_edit_electricity_bill(request, bill_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('electricity_bills')
    
    bill = get_object_or_404(ElectricityBill, id=bill_id)
    old_status = bill.status
    
    if request.method == 'POST':
        form = ElectricityBillUpdateForm(request.POST, instance=bill)
        if form.is_valid():
            bill = form.save()
            # Send email notification if status changed
            if old_status != bill.status:
                send_bill_status_notification(bill)
            messages.success(request, 'Electricity bill updated successfully!')
            return redirect('admin_electricity_bills')
    else:
        form = ElectricityBillUpdateForm(instance=bill)
    return render(request, 'admin_edit_electricity_bill.html', {'form': form, 'bill': bill})


@login_required
def admin_delete_electricity_bill(request, bill_id):
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('electricity_bills')
    
    bill = get_object_or_404(ElectricityBill, id=bill_id)
    if request.method == 'POST':
        bill.delete()
        messages.success(request, 'Electricity bill deleted successfully!')
        return redirect('admin_electricity_bills')
    return render(request, 'admin_delete_electricity_bill.html', {'bill': bill})


def send_bill_status_notification(bill):
    """Send email notification when bill status changes"""
    subject = f'Electricity Bill Status Update: {bill.bill_number}'
    message = f'''
Dear {bill.user.first_name},

Your electricity bill status has been updated.

Bill Details:
- Bill Number: {bill.bill_number}
- Consumer Name: {bill.consumer_name}
- Amount: ₹{bill.amount}
- Due Date: {bill.due_date}
- Status: {bill.get_status_display()}

Thank you for using Smart City System.

Best regards,
Smart City Administration
    '''
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER or 'noreply@smartcity.com',
        [bill.user.email],
        fail_silently=False,
    )


# Message Views
@login_required
def user_messages(request):
    """View for users to see their received messages"""
    user_messages = Message.objects.filter(recipient=request.user)
    unread_count = user_messages.filter(is_read=False).count()
    
    context = {
        'messages': user_messages,
        'unread_count': unread_count,
    }
    return render(request, 'user_messages.html', context)


@login_required
def view_message(request, message_id):
    """View a specific message and mark it as read"""
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    message.mark_as_read()
    
    context = {
        'message': message,
    }
    return render(request, 'view_message.html', context)


@login_required
def send_message(request):
    """View for admins to send messages to users"""
    if not request.user.is_staff:
        messages.error(request, 'Only administrators can send messages.')
        return redirect('home')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, f'Message sent to {message.recipient.username} successfully!')
            return redirect('admin_messages')
    else:
        form = MessageForm()
    
    return render(request, 'send_message.html', {'form': form})


@login_required
def admin_messages(request):
    """View for admins to see all sent messages"""
    if not request.user.is_staff:
        messages.error(request, 'Only administrators can access this page.')
        return redirect('home')
    
    sent_messages = Message.objects.filter(sender=request.user)
    
    context = {
        'messages': sent_messages,
    }
    return render(request, 'admin_messages.html', context)