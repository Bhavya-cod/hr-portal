from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    user = request.user
    if user.is_admin():
        from accounts.models import User
        from attendance.models import Attendance, LeaveRequest
        from django.utils import timezone
        
        today = timezone.now().date()
        
        # Stats
        total_employees = User.objects.filter(role=User.Role.EMPLOYEE).count()
        present_today = Attendance.objects.filter(date=today, morning_check_in__isnull=False).count()
        
        # Pending leaves for admin approval
        pending_leaves = LeaveRequest.objects.filter(status='Pending').select_related('user')
        
        # Recent attendance
        recent_attendance = Attendance.objects.all().select_related('user').order_by('-date', '-morning_check_in')[:5]
        
        context = {
            'total_employees': total_employees,
            'present_today': present_today,
            'pending_leaves': pending_leaves,
            'recent_attendance': recent_attendance,
        }
        return render(request, 'dashboard/admin_home.html', context)
    
    # Ensure profile exists for employee
    from employees.models import EmployeeProfile, EmployeeTask
    from company.models import Announcement, CalendarEvent, CompanyPolicy
    from django.utils import timezone
    
    from attendance.models import LeaveRequest, Attendance
    from attendance.forms import LeaveRequestForm
    
    profile, created = EmployeeProfile.objects.get_or_create(user=user)
    
    today = timezone.now().date()
    announcements = Announcement.objects.filter(is_active=True).order_by('-date_posted')[:3]
    calendar_events = CalendarEvent.objects.filter(start_date__gte=today).order_by('start_date')[:4]
    policies = CompanyPolicy.objects.order_by('-last_updated')[:4]
    
    tasks = EmployeeTask.objects.filter(employee=user, is_completed=False).order_by('-created_at')
    
    # Employee's own leaves
    leaves = LeaveRequest.objects.filter(user=user).order_by('-created_at')[:5]
    leave_form = LeaveRequestForm()
    
    # Attendance for today
    attendance_record, _ = Attendance.objects.get_or_create(user=user, date=today)
    
    import datetime
    start_of_week = today - datetime.timedelta(days=today.weekday())
        
    attendances_this_week = Attendance.objects.filter(
        user=user, 
        date__range=[start_of_week, start_of_week + datetime.timedelta(days=6)]
    )
    attendance_dict = {a.date: a for a in attendances_this_week}

    current_week = []
    for i in range(7):
        day = start_of_week + datetime.timedelta(days=i)
        att = attendance_dict.get(day)
        hours = att.total_working_hours if att else 0.0
        
        # Max height for chart is roughly 120px, let's map 12 hours to 120px
        height = min(int(hours * 10), 120)
        
        current_week.append({
            'date': day,
            'is_today': day == today,
            'is_current_month': day.month == today.month,
            'day_name': day.strftime('%a'),
            'hours': hours,
            'hours_display': f"{int(hours)}h {int((hours*60)%60)}m" if hours > 0 else "0h",
            'bar_height': height if height > 0 else 4, # 4px minimum height to show a sliver
            'is_active': (hours > 0)
        })
    
    context = {
        'profile': profile,
        'announcements': announcements,
        'calendar_events': calendar_events,
        'policies': policies,
        'tasks': tasks,
        'leaves': leaves,
        'leave_form': leave_form,
        'attendance': attendance_record,
        'next_action': attendance_record.next_action,
        'current_week': current_week,
    }
    
    return render(request, 'dashboard/employee_home.html', context)

from django.db.models import Q

@login_required
def global_search(request):
    q = request.GET.get('q', '').strip()
    
    from accounts.models import User
    from employees.models import EmployeeTask, EmployeeDocument
    
    people = []
    tasks = []
    documents = []
    
    if q:
        # Search People (everyone can search people)
        people = User.objects.filter(
            Q(first_name__icontains=q) | 
            Q(last_name__icontains=q) | 
            Q(username__icontains=q)
        ).distinct()[:10]
        
        # Search Tasks & Documents
        if request.user.is_admin():
            tasks = EmployeeTask.objects.filter(title__icontains=q).select_related('employee')[:10]
            documents = EmployeeDocument.objects.filter(
                Q(document_type__icontains=q) | 
                Q(file__icontains=q)
            ).select_related('employee')[:10]
        else:
            tasks = EmployeeTask.objects.filter(employee=request.user, title__icontains=q)[:10]
            documents = EmployeeDocument.objects.filter(
                employee=request.user,
                file__icontains=q
            )[:10]
            
    context = {
        'q': q,
        'people': people,
        'tasks': tasks,
        'documents': documents,
    }
    return render(request, 'dashboard/search_results.html', context)
