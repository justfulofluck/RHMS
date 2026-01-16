@api_view(['GET'])
@permission_classes([AllowAny])
def mobile_doctor_slots(request, doctor_id):
    """
    Returns available slots for a specific doctor for the next 7 days.
    Ideal for direct booking flow from search results.
    """
    try:
        doctor = get_object_or_404(Doctor, id=doctor_id)
        
        # Get availability
        today = timezone.localtime().date()
        end_date = today + timedelta(days=7)
        
        slots = DoctorAvailability.objects.filter(
            doctor=doctor,
            date__range=[today, end_date],
            is_available=True
        ).order_by('date', 'start_time')
        
        # Group by date
        grouped_slots = {}
        for slot in slots:
            d_str = slot.date.strftime('%Y-%m-%d')
            if d_str not in grouped_slots:
                grouped_slots[d_str] = []
            
            grouped_slots[d_str].append({
                'id': slot.id,
                'start_time': slot.start_time, # Already string or time obj? Check model.
                'end_time': slot.end_time
            })
            
        # Format for Mobile App (List of days with slots)
        response_data = {
            'doctor': {
                'id': doctor.id,
                'name': doctor.name,
                'specialization': doctor.specialization,
                'hospital': doctor.hospital.name,
                'address': doctor.hospital.address
            },
            'availability': []
        }
        
        # Fill strictly for 7 days
        for i in range(7):
            curr_date = today + timedelta(days=i)
            d_str = curr_date.strftime('%Y-%m-%d')
            
            day_label = curr_date.strftime('%a') # Mon, Tue
            day_num = curr_date.day
            
            response_data['availability'].append({
                'date': d_str,
                'day': day_label,
                'date_num': day_num,
                'slots': grouped_slots.get(d_str, [])
            })
            
        return Response(response_data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)
