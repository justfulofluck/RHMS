// SOLUTION: Enhanced JavaScript with debugging and fixes for monthly_availability.html

// 1. Add this debug configuration at the top of the script section
const DEBUG_CONFIG = {
    AVAILABILITY_LIST_URL: "{% url 'doctor_availability_list' %}",
    MONTHLY_AVAILABILITY_URL: "{% url 'monthly_availability' %}",
    GET_BOOKED_DATES_URL: "{% url 'get_booked_dates' %}"
};

// Debug log to verify URL rendering
console.log('DEBUG: URL Configuration:', DEBUG_CONFIG);
console.log('DEBUG: Availability List URL:', DEBUG_CONFIG.AVAILABILITY_LIST_URL);

// 2. REPLACE the existing form submission handler with this enhanced version
document.getElementById('schedule-form').addEventListener('submit', function (e) {
    e.preventDefault();
    
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
    console.log('DEBUG: Submitting to:', DEBUG_CONFIG.MONTHLY_AVAILABILITY_URL);

    fetch(DEBUG_CONFIG.MONTHLY_AVAILABILITY_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        console.log('DEBUG: Response status:', response.status);
        console.log('DEBUG: Response headers:', response.headers);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(result => {
        console.log('DEBUG: Parsed result:', result);
        
        if (result.success) {
            console.log('DEBUG: Success path triggered');
            CustomToast.success(result.message);
            calendar.clearSelection();
            calendar.fetchAvailability(); // Refresh highlights
            
            console.log('DEBUG: About to set redirect timer to:', DEBUG_CONFIG.AVAILABILITY_LIST_URL);
            
            // FIX: Store timer ID and add additional logging
            const redirectTimer = setTimeout(() => {
                console.log('DEBUG: Redirect timer executed');
                console.log('DEBUG: Redirecting to:', DEBUG_CONFIG.AVAILABILITY_LIST_URL);
                
                // FIX: Add validation before redirect
                if (DEBUG_CONFIG.AVAILABILITY_LIST_URL && DEBUG_CONFIG.AVAILABILITY_LIST_URL !== 'None' && DEBUG_CONFIG.AVAILABILITY_LIST_URL !== '') {
                    window.location.href = DEBUG_CONFIG.AVAILABILITY_LIST_URL;
                } else {
                    console.error('DEBUG: Invalid URL for redirect');
                    // Fallback redirect
                    window.location.href = '/hospital/doctors/availability/';
                }
            }, 3500);
            
            console.log('DEBUG: Redirect timer set with ID:', redirectTimer);
            
        } else {
            console.log('DEBUG: Error path triggered:', result.error);
            CustomToast.error('Error: ' + result.error);
        }
    })
    .catch(err => {
        console.error('DEBUG: Fetch error:', err);
        console.error('DEBUG: Error details:', err.stack);
        CustomToast.error('An error occurred: ' + err.message);
    });
});

// 3. ENHANCED CustomToast.success method to add completion callback
// Replace the existing CustomToast.success method with this:
class CustomToast {
    static success(message) {
        const toast = document.createElement('div');
        toast.className = 'custom-toast-success';
        toast.textContent = message;
        document.body.appendChild(toast);
        
        // Auto-close after 3 seconds
        const closeTimer = setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => {
                toast.remove();
                console.log('DEBUG: Toast removed, redirect should happen in 500ms');
            }, 300);
        }, 3000);
        
        return closeTimer; // Return timer ID for debugging
    }
    
    static error(message) {
        const toast = document.createElement('div');
        toast.className = 'custom-toast-error';
        toast.textContent = message;
        document.body.appendChild(toast);
        
        // Auto-close after 5 seconds for errors
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    }
    
    static modal(message) {
        const modal = document.createElement('div');
        modal.className = 'custom-toast-modal';
        modal.innerHTML = `
            <div class="custom-toast-modal-content">
                <div class="custom-toast-modal-icon">!</div>
                <div class="custom-toast-modal-title">Information</div>
                <div class="custom-toast-modal-message">${message}</div>
                <button class="custom-toast-modal-btn">OK</button>
            </div>
        `;
        document.body.appendChild(modal);
        
        // Add event listener for OK button
        modal.querySelector('.custom-toast-modal-btn').addEventListener('click', () => {
            modal.style.animation = 'modalFadeOut 0.3s ease-out';
            setTimeout(() => modal.remove(), 300);
        });
    }
}
