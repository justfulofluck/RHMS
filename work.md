State Management: Syncing state between web and mobile clients can get tricky—especially with auth, sessions, and real-time updates.

Use Django REST Framework to expose APIs cleanly.

Use Docker to isolate services and simplify deployment.

Consider JWT-based auth for mobile and web clients to unify login flows.




Please act as a senior developer and collaborate with me to write the code correctly. Also, aim to simplify the logic.



Phase 1: Implement hospital registration + approval (already scaffolded).

Phase 2: Build hospital admin dashboard (scoped data, branding with logo/name).

Phase 3: Add doctor management + availability.

Phase 4: Expose APIs for Flutter dev (appointments, availability, hospital listing).

Phase 5: Integrate Celery for async notifications (email/SMS).


🧱 Step 1: Project Setup
Create Django project: rhms

Core apps:
accounts → authentication, roles (superadmin, hospital admin, doctor, patient)
hospitals → hospital registration, approval, dashboard
appointments → doctors, availability, bookings
audit → logging actions (optional, can be merged later)

🗄️ Step 2: Database Schema (Core Entities)
Hospital
id
name
registration_number
email
logo
address
phone_number
city
status (pending, approved, rejected)
created_at

HospitalAdmin
user_id (FK → Django User)
hospital_id (FK → Hospital)

Doctor
id
hospital_id (FK → Hospital)
name, email, specialization, fee, status

DoctorAvailability
id
doctor_id (FK → Doctor)
date, start_time, end_time, is_available

Patient
user_id (FK → Django User)
name, email, phone_number

Appointment
id
hospital_id, doctor_id, patient_id
appointment_date, appointment_time
status (booked, completed, cancelled)

AuditLog
id
user_id
action
entity
entity_id
timestamp

🌐 Step 3: API Structure (Django REST Framework)
Auth
POST /api/auth/login/
POST /api/auth/register/ (patients)
POST /api/auth/logout/

Hospitals
POST /api/hospitals/register/ → public hospital registration
GET /api/hospitals/ → list approved hospitals
GET /api/hospitals/{id}/ → hospital details
POST /api/admin/hospitals/{id}/approve/ → superadmin approves
POST /api/admin/hospitals/{id}/reject/ → superadmin rejects

Doctors
GET /api/doctors/?hospital_id=
GET /api/doctors/{id}/availability/
POST /api/doctors/{id}/availability/set/ (hospital admin/doctor)

Appointments
POST /api/appointments/book/
GET /api/appointments/user/ (patient’s bookings)
GET /api/appointments/hospital/ (hospital admin view)
POST /api/appointments/{id}/cancel/

Super Admin
GET /api/admin/hospitals/pending/
GET /api/admin/audit-logs/


Phase 1 Implementation Plan
Hospital Registration Form (public)
Saves hospital with status=pending

Superadmin Dashboard (Django Admin)
Lists pending hospitals
Approve → creates hospital admin user, emails credentials
Reject → updates status

Login Page
Superadmin uses Django admin login
Hospital admin uses same login but scoped to their hospital


database info:
user - rhms_user
pass - klsaDb23@#

superadmin
user - bgtuser
user - blueglobalcloud@gmail.com
pass - bgt@123

Token - eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9

pjooewfxcxhtldod
