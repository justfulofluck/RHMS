# phase_3

Absolutely Bhavan — here’s a clear and complete **flow of patient management** for your hospital system, covering both backend logic and how it connects to the frontend later.

---

## 🧑‍⚕️ Patient Management Flow

### 1. **Patient Registration**
- **Who can register**: Hospital Admin or Receptionist
- **Data collected**:
  - Full name
  - Age, gender
  - Contact info (phone, email)
  - Address
  - Medical history (optional)
- **Backend**:
  - `Patient` model created
  - API endpoint: `POST /api/patients/`
  - Serializer: `PatientSerializer`
- **Frontend**:
  - Bootstrap form for admin to register patient
  - Dart mobile form for walk-in registration

---

### 2. **Patient Profile View**
- **Who can view**: Hospital Admin, Assigned Doctor
- **Data shown**:
  - Personal details
  - Appointment history
  - Treatments received
- **Backend**:
  - API endpoint: `GET /api/patients/{id}/`
  - Permissions: Only staff from same hospital
- **Frontend**:
  - Bootstrap dashboard card
  - Dart mobile view for doctors

---

### 3. **Patient Search & List**
- **Who can access**: Hospital Admin, Receptionist
- **Features**:
  - Search by name, phone, ID
  - Filter by date, doctor, treatment
- **Backend**:
  - API endpoint: `GET /api/patients/?search=...`
  - Pagination and filtering
- **Frontend**:
  - Bootstrap table with search bar
  - Dart list view with filters

---

### 4. **Appointment Booking**
- **Who can book**: Patient (via Dart app), Admin (via dashboard)
- **Data needed**:
  - Patient ID
  - Doctor ID
  - Treatment
  - Date & time
- **Backend**:
  - `Appointment` model links patient, doctor, treatment
  - API endpoint: `POST /api/appointments/`
- **Frontend**:
  - Dart calendar picker
  - Bootstrap booking form

---

### 5. **Medical History & Treatment Tracking**
- **Who can update**: Doctor
- **Features**:
  - Add diagnosis, prescriptions, notes
  - View treatment timeline
- **Backend**:
  - `TreatmentRecord` model (linked to patient + appointment)
  - API endpoint: `POST /api/treatments/record/`
- **Frontend**:
  - Dart treatment timeline
  - Bootstrap expandable cards

---

### 6. **Patient Portal (Dart App)**
- **Features**:
  - View profile
  - Book appointments
  - See upcoming visits
  - Download prescriptions
- **Backend**:
  - Authenticated endpoints for patient role
- **Frontend**:
  - Dart mobile app with secure login

---

## 🔐 Permissions Summary

| Role            | Can Register | Can View Profile | Can Book Appointment | Can Update Treatment |
|-----------------|--------------|------------------|----------------------|----------------------|
| Hospital Admin  | ✅            | ✅                | ✅                    | ❌                  |
| Doctor          | ❌           | ✅ (assigned only)| ❌                   | ✅                   |
| Receptionist    | ✅            | ✅                | ✅                    | ❌                  |
| Patient         | ❌           | ✅ (self only)    | ✅                    | ❌                  |

---

Let me know if you want to start with the **Patient model and API endpoints** — I can scaffold them for you right away.