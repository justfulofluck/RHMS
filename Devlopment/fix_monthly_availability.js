// This is the complete replacement JavaScript section for monthly_availability.html
// Replace everything from the line "document.getElementById('schedule-form').addEventListener('submit'..."

document.getElementById('schedule-form').addEventListener('submit', function (e) {
    e.preventDefault();
    
    // Enhanced configuration with URL validation
    const APP_CONFIG = {
        AVAILABILITY_LIST_URL: "{% url 'doctor_availability_list' %}",
        MONTHLY_AVAILABILITY_URL: "{% url 'monthly_availability' %}",
        GET_BOOKED_DATES_URL: "{% url 'get_booked_dates' %}",
        FALLBACK_AVAILABILITY_URL: "/hospital/doctors/availability/"
    };
    
    // Debug: Log URL configuration
    console.log('DEBUG: URL Configuration:', APP_CONFIG);
    console.log('DEBUG: Availability List URL:', APP_CONFIG.AVAILABILITY_LIST_URL);
    console.log('DEBUG: Form submission started');

    if (calendar.selectedDates.size === 0) {
        CustomToast.modal('Please click on updates in the calendar to SELECT them (they will turn blue).\n\nYellow dates are just showing what is already scheduled.\nBlue dates are the ones you are about to change.');
        return;
    }

    const slots = [];
    document.querySelectorAll('.slot-row').forEach(row => {
        slots.push({
            start_time: row.querySelector('[name="start_time"]').value,
            end_time: row.querySelector('[name="end_time"]').value
        });
    });

    const data = {
        dates: Array.from(calendar.selectedDates),
        slots: slots,
        duration: document.getElementById('slot_duration').value
    };

    console.log('DEBUG: Form data:', data);
    console.log('DEBUG: Submitting to:', APP_CONFIG.MONTHLY_AVAILABILITY_URL);
    console.log('DEBUG: Dates selected:', data.dates.length);

    fetch(APP_CONFIG.MONTHLY_AVAILABILITY_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        console.log('DEBUG: Response status:', response.status);
        console.log('DEBUG: Response OK:', response.ok);
        
        if (!response.ok) {
            console.error('DEBUG: HTTP Error:', response.statusText);
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return response.json();
    })
    .then(result => {
        console.log('DEBUG: Parsed result:', result);
        
        if (result.success) {
            console.log('DEBUG: Success path triggered');
            console.log('DEBUG: Success message:', result.message);
            CustomToast.success(result.message);
            calendar.clearSelection();
            calendar.fetchAvailability(); // Refresh highlights
            
            // Redirect to availability list after toast message
            setTimeout(() => {
                console.log('DEBUG: Redirect timer executed');
                console.log('DEBUG: Attempting redirect to:', APP_CONFIG.AVAILABILITY_LIST_URL);
                
                // Enhanced URL validation and redirect logic
                const targetUrl = APP_CONFIG.AVAILABILITY_LIST_URL;
                if (targetUrl && targetUrl !== 'None' && targetUrl !== '' && targetUrl.includes('availability')) {
                    console.log('DEBUG: Using primary URL:', targetUrl);
                    window.location.href = targetUrl;
                } else {
                    console.log('DEBUG: Using fallback URL:', APP_CONFIG.FALLBACK_AVAILABILITY_URL);
                    window.location.href = APP_CONFIG.FALLBACK_AVAILABILITY_URL;
                }
            }, 3500);
        } else {
            console.log('DEBUG: Error path triggered:', result.error);
            CustomToast.error('Error: ' + result.error);
        }
    })
    .catch(err => {
        console.error('DEBUG: Fetch error:', err);
        console.error('DEBUG: Error stack:', err.stack);
        CustomToast.error('An error occurred: ' + err.message);
    });
});
