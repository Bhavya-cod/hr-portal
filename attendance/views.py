import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
from .models import Attendance, LeaveRequest
from .forms import LeaveRequestForm

@login_required
def check_status(request):
    today = timezone.now().date()
    attendance, created = Attendance.objects.get_or_create(user=request.user, date=today)
    
    context = {
        'attendance': attendance,
        'next_action': attendance.next_action,
        'current_time': timezone.now()
    }
    return render(request, 'attendance/partials/status.html', context)

@login_required
def perform_action(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed", status=405)
        
    today = timezone.now().date()
    attendance, created = Attendance.objects.get_or_create(user=request.user, date=today)
    
    action = attendance.next_action
    if action:
        now = timezone.now()
        setattr(attendance, action, now)
        
        # Grace Period Logic (9:30 AM + 15 mins = 9:45 AM)
        if action == 'morning_check_in':
            local_now = timezone.localtime(now)
            # If after 09:45:00
            if local_now.hour > 9 or (local_now.hour == 9 and local_now.minute > 45):
                attendance.status = 'LOP'
                if not attendance.remarks:
                    attendance.remarks = f"Late Login: {local_now.strftime('%H:%M')} (LOP Applied)"
        
        # Geolocation recording
        loc_name = request.POST.get('location_name')
        if loc_name:
            # Because action is 'morning_check_in', we can find the location field by string splitting
            base_action = action.replace('check_in', '').replace('check_out', '').strip('_')
            location_field = f"{base_action}_location" if base_action else f"{action.split('_')[0]}_location"
            setattr(attendance, location_field, loc_name)
            
        attendance.save()
        
    context = {
        'attendance': attendance,
        'next_action': attendance.next_action,
        'current_time': timezone.now()
    }
    
    if request.GET.get('source') == 'small':
        return render(request, 'attendance/partials/actions.html', context)
    return render(request, 'attendance/partials/status.html', context)

@login_required
def summary(request):
    # Only for admin
    if not request.user.is_admin():
        return HttpResponse("Unauthorized", status=403)
        
    attendances = Attendance.objects.all().select_related('user').order_by('-date', 'user__username')
    return render(request, 'attendance/summary.html', {'attendances': attendances})

@login_required
def export_csv(request):
    if not request.user.is_admin():
        return HttpResponse("Unauthorized", status=403)
        
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_summary.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Employee', 'Morning In', 'Lunch Out', 'Afternoon In', 'Final Out'])
    
    attendances = Attendance.objects.all().select_related('user').order_by('-date', 'user__username')
    for att in attendances:
        writer.writerow([
            att.date,
            att.user.username,
            att.morning_check_in.strftime('%H:%M') if att.morning_check_in else '--',
            att.lunch_check_out.strftime('%H:%M') if att.lunch_check_out else '--',
            att.afternoon_check_in.strftime('%H:%M') if att.afternoon_check_in else '--',
            att.final_check_out.strftime('%H:%M') if att.final_check_out else '--'
        ])
        
    return response

@login_required
def apply_leave(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            
            # Logic for 1 paid leave per month
            start_date = leave.start_date
            month = start_date.month
            year = start_date.year
            
            # Check for approved or pending paid leaves in the same month
            paid_leaves_count = LeaveRequest.objects.filter(
                user=request.user,
                start_date__month=month,
                start_date__year=year,
                leave_type='Paid'
            ).exclude(status='Rejected').count()
            
            if paid_leaves_count >= 1:
                leave.leave_type = 'LOP'
            else:
                leave.leave_type = 'Paid'
                
            leave.save()
            return redirect('dashboard:home')
    else:
        form = LeaveRequestForm()
    
    return render(request, 'attendance/leave_apply.html', {'form': form})

@login_required
def approve_leave(request, pk):
    if not request.user.is_admin():
        return HttpResponse("Unauthorized", status=403)
    
    leave = get_object_or_404(LeaveRequest, pk=pk)
    leave.status = 'Approved'
    leave.save()
    return redirect('dashboard:home')

@login_required
def reject_leave(request, pk):
    if not request.user.is_admin():
        return HttpResponse("Unauthorized", status=403)
    
    leave = get_object_or_404(LeaveRequest, pk=pk)
    leave.status = 'Rejected'
    if request.method == 'POST':
        leave.admin_remarks = request.POST.get('remarks', '')
    leave.save()
    return redirect('dashboard:home')
