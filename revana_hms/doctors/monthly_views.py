import json
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from frontend.decorators import role_required
from doctors.models import Doctor
from appointments.models import DoctorAvailability
from django.views.decorators.csrf import csrf_exempt


@login_required
@role_required('doctor')
def create_monthly_availability(request):
    """Create availability for specific dates with multiple slots"""
    doctor = Doctor.objects.get(user=request.user)
    
    if request.method == 'POST':
        try:
            # Handle JSON data from new advanced scheduler
            if request.content_type == 'application/json':
                print(f"DEBUG: Scheduler Payload: {request.body.decode('utf-8')}")
                data = json.loads(request.body)
                dates = data.get('dates', [])
                slots = data.get('slots', [])
                slot_duration = int(data.get('duration', 30))
                
                if not dates or not slots:
                    return JsonResponse({'success': False, 'error': 'Please select dates and configure time slots.'})
                
                created_count = 0
                
                for date_str in dates:
                    try:
                        current_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    except ValueError:
                        continue
                        
                    # Overwrite Strategy:
                    # 1. We delete ALL existing availability for this specific date
                    #    This allows "editing" by simply re-selecting the date and applying new slots.
                    DoctorAvailability.objects.filter(
                        doctor=doctor,
                        date=current_date
                    ).delete()
                    
                    # 2. Create new availability for each slot
                    for slot in slots:
                        start_time = slot.get('start_time')
                        end_time = slot.get('end_time')
                        
                        if start_time and end_time:
                            # Parse times
                            # Helper to convert string to time/datetime
                            fmt = '%H:%M'
                            try:
                                t_start = datetime.strptime(start_time, fmt)
                                t_end = datetime.strptime(end_time, fmt)
                                
                                # Convert to full datetime for arithmetic (using dummy date)
                                dt_start = datetime.combine(datetime.today(), t_start.time())
                                dt_end = datetime.combine(datetime.today(), t_end.time())
                                
                                # Loop to create slots
                                current_slot_start = dt_start
                                while current_slot_start + timedelta(minutes=slot_duration) <= dt_end:
                                    current_slot_end = current_slot_start + timedelta(minutes=slot_duration)
                                    
                                    DoctorAvailability.objects.create(
                                        doctor=doctor,
                                        date=current_date,
                                        start_time=current_slot_start.time(),
                                        end_time=current_slot_end.time(),
                                        slot_duration=slot_duration,
                                        is_available=True
                                    )
                                    created_count += 1
                                    
                                    current_slot_start = current_slot_end
                            except ValueError as e:
                                print(f"Error parsing time: {e}")
                                continue
                            created_count += 1
                            
                return JsonResponse({'success': True, 'message': f'Successfully updated schedule for {len(dates)} days.', 'count': len(dates)})
            
            else:
                return JsonResponse({'success': False, 'error': 'Invalid content type. Expected JSON.'})
                
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    # GET request - show form
    return render(request, 'doctors/monthly_availability.html', {
        'doctor': doctor,
        'today': timezone.now().date()
    })


@login_required
@role_required('doctor')
def doctor_availability_list(request):
    """View and manage doctor's availability"""
    doctor = Doctor.objects.get(user=request.user)
    
    today = timezone.now().date()
    availabilities = DoctorAvailability.objects.filter(
        doctor=doctor,
        date__gte=today
    ).order_by('date', 'start_time')
    
    return render(request, 'doctors/availability_list.html', {
        'doctor': doctor,
        'availabilities': availabilities
    })

@login_required
@role_required('doctor')
def delete_availability(request, availability_id):
    """Delete a specific availability entry"""
    if request.method == 'POST':
        try:
            doctor = Doctor.objects.get(user=request.user)
            availability = get_object_or_404(DoctorAvailability, id=availability_id, doctor=doctor)
            
            # Check if there are any booked appointments in this slot?
            # For now, we'll allow deletion but you might want to prevent it if appointments exist.
            # appointments = Appointment.objects.filter(doctor=doctor, appointment_date__date=availability.date, ...)
            
            availability.delete()
            messages.success(request, 'Availability slot deleted successfully.')
            
        except Exception as e:
            messages.error(request, f'Error deleting availability: {str(e)}')
            
    return redirect('doctor_availability_list')


@login_required
@role_required('doctor')
def get_booked_dates(request):
    """API to get dates that already have availability for a specific month"""
    doctor = Doctor.objects.get(user=request.user)
    year_str = request.GET.get('year')
    month_str = request.GET.get('month')
    
    if not year_str or not month_str:
        return JsonResponse({'dates': []})
        
    try:
        year = int(year_str)
        month = int(month_str)
        
        # Get availability for this month
        availabilities = DoctorAvailability.objects.filter(
            doctor=doctor,
            date__year=year,
            date__month=month
        ).values_list('date', flat=True).distinct()
        
        # Convert dates to string format 'YYYY-MM-DD'
        dates = [d.strftime('%Y-%m-%d') for d in availabilities]
        
        return JsonResponse({'dates': dates})
        
    except ValueError:
        return JsonResponse({'dates': []})
