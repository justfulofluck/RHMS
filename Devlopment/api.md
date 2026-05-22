# REVANA HMS - MOBILE API DOCUMENTATION (v2.0)

**Base URL:** (Your Server URL, e.g., `http://192.168.x.x:8000`)

---

## 1. AUTHENTICATION (JWT)

### Login (Get Tokens)
*   **Endpoint:** `POST /api/token/`
*   **Body:**
    ```json
    { "email": "user@example.com", "password": "yourpassword" }
    ```
*   **Response:** `{ "access": "...", "refresh": "..." }`

### Refresh Token
*   **Endpoint:** `POST /api/token/refresh/`
*   **Body:** `{ "refresh": "your_refresh_token" }`

### Password Reset
*   **Request:** `POST /api/accounts/password-reset/` (Body: `{ "email": "..." }`)
*   **Confirm:** `POST /api/accounts/password-reset-confirm/`

---

## 2. UNIVERSAL SEARCH (⚡ NEW)

### Search Everything (Doctors & Hospitals)
*   **Endpoint:** `GET /api/universal-search/`
*   **Query Params:** `query` (e.g., "Fracture", "Heart"), `city` (e.g., "Vadodara")
*   **Description:** Smart search that handles synonyms (e.g., "Bone break" -> "Orthopedics") and location filtering.
*   **Response:**
    ```json
    {
      "doctors": [
        {
          "id": 1,
          "name": "Dr. Amit Patel",
          "specialization": "Orthopedics",
          "hospital_name": "Sunshine Hospital",
          "action": "Book"
        }
      ],
      "hospitals": [
        { "id": 5, "name": "Sunshine Hospital", "action": "Visit" }
      ]
    }
    ```

---

## 3. BOOKING FLOW (⚡ UPDATED)

### Get Doctor Slots (Booking Screen)
*   Use this when user clicks "Book" on a doctor card.
*   **Endpoint:** `GET /appointments/api/mobile-doctor-slots/<doctor_id>/`
*   **Response:**
    *   Doctor Details (Name, Hospital, Address)
    *   **Availability:** Lists next 7 days with specific time slots.

### Book Appointment
*   **Endpoint:** `POST /mobile/book/`
*   **Headers:** `Authorization: Bearer <access_token>`
*   **Body:**
    ```json
    {
      "availability_id": 456  // (REQUIRED: The specific slot ID user clicked on)
    }
    ```

### Cancel Appointment
*   **Endpoint:** `POST /api/appointments/cancel/<appointment_id>/`
*   **Headers:** `Authorization: Bearer <access_token>`

### My Appointments
*   **Endpoint:** `GET /api/appointments/my-appointments/`
*   **Headers:** `Authorization: Bearer <access_token>`

---

## 4. PATIENT MANAGEMENT

### Register Patient
*   **Endpoint:** `POST /patients/register/`
*   **Body:**
    ```json
    {
      "email": "user@email.com",
      "password": "password123",
      "name": "Full Name",
      "age": 25,
      "gender": "Male",
      "phone": "9876543210",
      "address": "Full Address"
    }
    ```

### Profile & Notifications
*   **Get Profile:** `GET /patients/api/profile/`
*   **Update Profile:** `PATCH /patients/api/profile/`
*   **Medical History:** `GET /patients/api/medical-history/`
*   **Notifications:** `GET /patients/api/notifications/`
*   **Read Notification:** `PATCH /patients/api/notifications/<id>/mark-read/`

---

## 5. CORE DATA & HOSPITALS

### List Approved Hospitals (⚡ NEW)
*   **Endpoint:** `GET /api/hospitals/hospitals/`
*   **Response:** List of all approved hospitals with details.

### Core Lists
*   **Departments:** `GET /api/departments/`
*   **Treatments:** `GET /api/treatments/`
*   **Doctors:** `GET /api/doctors/`