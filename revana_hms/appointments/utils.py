from datetime import datetime, timedelta, time


def generate_time_slots(availability):
    """
    Generate individual time slots from a DoctorAvailability object.
    
    Args:
        availability: DoctorAvailability object with date, start_time, end_time, and slot_duration
    
    Returns:
        List of dictionaries containing individual slot information:
        [
            {
                'availability_id': int,
                'date': date object,
                'start_time': time object,
                'end_time': time object,
                'duration': int (minutes),
                'is_available': bool
            },
            ...
        ]
    
    Example:
        If availability is 9:00 AM - 12:00 PM with 30-minute slots:
        Returns 6 slots: 9:00-9:30, 9:30-10:00, ..., 11:30-12:00
    """
    slots = []
    
    # Combine date with start time to create datetime for calculation
    current_datetime = datetime.combine(datetime.today(), availability.start_time)
    end_datetime = datetime.combine(datetime.today(), availability.end_time)
    
    # Duration as timedelta
    duration_delta = timedelta(minutes=availability.slot_duration)
    
    # Generate slots
    while current_datetime < end_datetime:
        slot_end_datetime = current_datetime + duration_delta
        
        # Only add slot if it fits within the availability window
        if slot_end_datetime.time() <= availability.end_time:
            slots.append({
                'availability_id': availability.id,
                'date': availability.date,
                'start_time': current_datetime.time(),
                'end_time': slot_end_datetime.time(),
                'duration': availability.slot_duration,
                'is_available': availability.is_available
            })
        
        # Move to next slot
        current_datetime = slot_end_datetime
    
    return slots


def format_time_12hr(time_obj):
    """
    Format time object to 12-hour format string.
    
    Args:
        time_obj: datetime.time object
    
    Returns:
        String in format "9:00 AM"
    """
    return datetime.combine(datetime.today(), time_obj).strftime('%I:%M %p')


def calculate_slot_count(start_time, end_time, duration_minutes):
    """
    Calculate how many slots fit in a time range.
    
    Args:
        start_time: time object
        end_time: time object
        duration_minutes: int
    
    Returns:
        int: Number of slots that fit
    """
    start_dt = datetime.combine(datetime.today(), start_time)
    end_dt = datetime.combine(datetime.today(), end_time)
    
    total_minutes = (end_dt - start_dt).total_seconds() / 60
    return int(total_minutes // duration_minutes)
