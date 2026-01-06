Flutter Patient API Documentation
jango server is running at: http://192.168.1.208:8000

1. Get Mobile Availability Slots (3-Day View)
Fetches available time slots for a specific doctor for Today, Tomorrow, and the Day After.

Endpoint: /appointments/api/mobile-slots/<doctor_id>/
Method: GET
Parameters: None (Doctor ID is in URL)
Response (JSON):
{
  "success": true,
  "days": [
    {
      "date": "2023-12-12",
      "label": "Today",
      "slots": [
        {
          "id": 101,
          "start": "09:00 AM",
          "end": "09:30 AM"
        },
        {
          "id": 102,
          "start": "10:00 AM",
          "end": "10:30 AM"
        }
      ]
    },
    {
      "date": "2023-12-13",
      "label": "Tomorrow",
      "slots": []
    },
    {
      "date": "2023-12-14",
      "label": "Thu, 14 Dec",
      "slots": [...]
    }
  ]
}


2. Book Appointment

Books a specific slot for the currently authenticated user.

Endpoint: /appointments/api/mobile-book/
Method: POST
Headers:
Content-Type: application/json
X-CSRFToken: <csrf-token> (If using session auth/cookies)
Authorization: Token <token> (If using DRF Token Auth)
Body:
{
  "availability_id": 101
}

Response (Success):
{
  "message": "Appointment booked",
  "doctor": "Dr. Smith",
  "date": "2023-12-12",
  "start": "09:00:00",
  "end": "09:30:00"
}

Response (Error):
{
  "error": "Slot not available" 
}

3. List Doctors 

need to search/list doctors first.

Endpoint: /appointments/widget/doctors/
Method: GET
Parameters:
hospital_id: (Required) Int
department
: (Required) String name
Response:
{
  "doctors": [
    {
      "id": 1,
      "name": "Dr. John Doe",
      "specialization": "Cardiology"
    }
  ]
}