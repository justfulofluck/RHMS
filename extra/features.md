# RHMS - System Features Documentation

**Project:** Revana Hospital Management System  
**Version:** 1.0  
**Architecture:** Django 5.2 + MySQL + DRF + JWT  
**Last Updated:** 2026-05-06

---

## Table of Contents

1. [Core Modules](#1-core-modules)
2. [User Roles & Permissions](#2-user-roles--permissions)
3. [Authentication & Authorization](#3-authentication--authorization)
4. [API Endpoints](#4-api-endpoints)
5. [Frontend Pages](#5-frontend-pages)
6. [Widget/Embedded System](#6-widgetembedded-system)
7. [Database Schema Overview](#7-database-schema-overview)
8. [Third-Party Integrations](#8-third-party-integrations)
9. [Not Yet Implemented](#9-not-yet-implemented)

---

## 1. Core Modules

### 1.1 Accounts Module (`/accounts`)
**Purpose:** User authentication, profile management, role-based access control

**Models:**
- `User` - Custom Django User model (extends AbstractUser)
  - Fields: email (unique), phone, role (choices: superadmin, hospitaladmin, doctor, patient), is_verified, verification_token
  - Supports email-based login
  - Role-based permission system

**Features:**
- User registration (hospital, doctor, patient)
- User login/logout
- Password reset (email-based)
- User profile management
- Email verification system
- Admin user listing and management
- SuperAdmin dashboard for user oversight

**URLs:**
- `/accounts/register/` - User registration
- `/accounts/login/` - Login page
- `/accounts/logout/` - Logout
- `/accounts/profile/` - User profile
- `/api/accounts/` - DRF API endpoints
- `/api/admin/` - Admin-only endpoints

---

### 1.2 Hospitals Module (`/hospitals`)
**Purpose:** Hospital management, department and treatment configuration

**Models:**
- `Hospital` - Hospital profile
  - Fields: name, address, city, state, registration_number, phone_number, email, logo, status (pending/approved/rejected)
- `Department` - Hospital departments
  - Fields: hospital (FK), name, description
- `Treatment` - Medical treatments/services
  - Fields: department (FK), name, description, price, duration
- `HospitalAdmin` - Links admin user to hospital
  - Fields: user (FK to User), hospital (FK)

**Features:**
- Hospital registration with approval workflow
- Hospital admin dashboard
- Department creation and management
- Treatment/service catalog management
- Hospital profile editing
- Multi-hospital support
- Hospital verification status tracking

**Views:**
- Hospital registration (public + admin)
- Department CRUD
- Treatment CRUD
- Hospital listing and detail
- Admin approval workflow

**API:**
- `/api/hospitals/` - Hospital CRUD
- `/api/admin/hospitals/` - Admin-only endpoints
- `/api/departments/` - Department management
- `/api/treatments/` - Treatment management

---

### 1.3 Doctors Module (`/doctors`)
**Purpose:** Doctor profiles, schedule management, availability tracking

**Models:**
- `Doctor` - Doctor profile
  - Fields: user (FK), hospital (FK), specialization, qualifications, experience_years, consultation_fee, doctor_image, is_available, bio
- `DoctorAvailability` - Doctor time slots
  - Fields: doctor (FK), date, start_time, end_time, is_available, is_booked
  - Unique constraint: one availability per doctor per time slot
- `MonthlyDoctorAvailability` - Monthly recurring availability
  - Fields: doctor, day_of_week, start_time, end_time, is_active

**Features:**
- Doctor registration and profile creation
- Monthly availability calendar (day-by-day view)
- Time slot management
- Doctor-patient relationship tracking
- Doctor dashboard with appointment statistics
- Public doctor listing
- Doctor search by hospital/specialty

**Views:**
- Doctor list (public and filtered)
- Doctor detail
- Doctor profile edit
- Availability management (AJAX-based)
- Monthly availability calendar
- Doctor dashboard (appointments today, statistics)

**API:**
- `/api/doctors/` - Doctor CRUD
- `/api/availability/` - Availability management
- `/api/public-availability/` - Public slot viewing
- `/hospital/doctors/` - Hospital-specific doctor pages

**Special Note:** Model architecture has issue - `DoctorAvailability` appears in two apps (doctors and appointments). Should be consolidated.

---

### 1.4 Patients Module (`/patients`)
**Purpose:** Patient records, appointment history, medical history

**Models:**
- `Patient` - Patient profile
  - Fields: user (FK OneToOne), hospital (FK), dob, gender, blood_group, address, emergency_contact, medical_history, allergies
- `MedicalRecord` - Patient medical history
  - Fields: patient (FK), doctor (FK), diagnosis, prescription, visit_date, notes
- `PatientReport` - Generated medical reports
  - Fields: patient, generated_by (FK User), report_type, file (PDF)

**Features:**
- Patient registration
- Patient profile management
- Medical history tracking
- Appointment history
- Report generation (PDF)
- Patient dashboard with upcoming appointments

**API:**
- `/api/patients/` - Patient CRUD
- `/patients/` - Patient-specific pages

---

### 1.5 Appointments Module (`/appointments`)
**Purpose:** Appointment booking, scheduling, calendar management, token generation

**Models:**
- `Appointment` - Appointment record
  - Fields: patient (FK), doctor (FK), hospital (FK), appointment_date, appointment_time, token_number, status (scheduled/completed/cancelled/no-show), notes, created_at
- `DoctorAvailability` (canonical version)
  - Fields: doctor (FK), date, start_time, end_time, is_available, is_booked
  - Unique constraint prevents double-booking

**Features:**
- Online appointment booking (widget + standalone)
- Token-based queue system (sequential numbering per day/doctor)
- Calendar view (daily/monthly)
- Appointment status tracking
- Cancellation and rescheduling
- Mobile-responsive booking form
- Multi-step booking wizard
- Real-time availability checking
- SMS/Email notifications (infrastructure in place)

**Views:**
- Appointment booking (multi-step form)
- My appointments (patient view)
- Appointment detail
- Calendar view
- Doctor schedule management
- Mobile booking API

**API:**
- `/api/appointments/` - Full CRUD
- `/api/appointments/my-appointments/` - Patient's appointments only
- `/api/appointments/doctor-availabilities/` - Doctor slots
- `/appointments/` - HTML views (calendar, management)

**Widget:** Embeddable booking system for external websites

**Critical Flow:** Booking process uses `select_for_update()` to prevent race conditions - properly implemented.

---

### 1.6 Core Module (`/core`)
**Purpose:** Shared utilities, permissions, search

**Models:**
- `AuditLog` - System activity logging
- `Notification` - In-app notifications (via django-notifications)

**Features:**
- Universal search across all entities (doctors, hospitals, patients, departments)
- Semantic search using sentence-transformers (ML-based)
- Custom permissions (IsSuperAdmin, IsHospitalAdmin, IsDoctor, IsPatient)
- Permission mixins for views
- System-wide settings management
- Activity audit trail

**Views:**
- `universal_search` - Search across multiple models
- `test_auth` - Authentication testing endpoint

---

### 1.7 Notifications Module (`/notifications`)
**Purpose:** Real-time notifications for appointments, approvals, messages

**Features:**
- Signal-based notification system (django-notifications)
- Email notifications (SMTP)
- Appointment confirmations
- Status change alerts
- In-app notification badge

---

### 1.8 Advertisements Module (`/advertisements`)
**Purpose:** Promotional content management

**Models:**
- `Advertisement` - Ad campaigns
  - Fields: title, image, link, hospital (FK), is_active, start_date, end_date

**Features:**
- Hospital-specific advertisements
- Display on frontend pages
- Active/inactive status
- Date-range based serving

**API:**
- `/api/advertisements/` - CRUD endpoints

---

### 1.9 Frontend Module (`/frontend`)
**Purpose:** Main user-facing pages, template rendering, static assets

**Pages (Templates):**
- `homepage.html` - Landing page with links to all portals
- `hospital_login.html` - Hospital admin login
- `doctor_login.html` - Doctor login
- `universal_login.html` - Combined login page
- `request_password_reset.html` - Forgot password
- `reset_password_confirm.html` - Password reset confirmation
- `register_hospital.html` - Hospital registration
- `departments.html` - Department listing
- `department_detail.html` - Single department view
- `hospital_appointments.html` - Patient appointment booking portal
- `hospital_admin/dashboard.html` - Hospital admin main dashboard
- `hospital_admin/register.html` - Doctor registration by admin

**Static Assets:**
- CSS: Bootstrap, Toastr, custom styles
- JS: jQuery, Bootstrap JS, custom functions (appointment_widget.js, dashboard.js)
- Images: logos, icons, backgrounds

**Widget:** Appointments widget embedded across sites

---

## 2. User Roles & Permissions

### Role Hierarchy

1. **SuperAdmin**
   - Full system access
   - Approve/reject hospitals
   - Manage all users
   - View all data across hospitals
   - Access `/admin/` Django admin

2. **HospitalAdmin**
   - Manage own hospital's doctors, patients, appointments
   - Approve/ reject doctor requests
   - View hospital dashboard
   - Access hospital-specific data only

3. **Doctor**
   - View personal schedule
   - Mark availability
   - View own appointments
   - Update appointment status (complete/cancel)
   - Access patient medical history for own patients

4. **Patient**
   - Book appointments
   - View own appointments
   - Edit profile
   - Cancel own appointments (within limits)

### Permission Classes (in `core/permissions.py`)
- `IsSuperAdmin` - Only super admins
- `IsHospitalAdmin` - Only hospital admins
- `IsHospitalAdminOfSameHospital` - Admin of specific hospital
- `IsDoctor` - Only doctors
- `IsPatient` - Only patients
- `IsDoctorOrHospitalAdmin` - Either role
- `IsOwner` - Object owner (user-specific)
- `IsDoctorAssignedToPatient` - Doctor assigned to patient

---

## 3. Authentication & Authorization

### JWT Tokens
- Algorithm: HS256
- Access token lifetime: 2 hours
- Refresh token lifetime: 7 days
- Token rotation enabled (refresh rotates)
- Blacklist after rotation enabled

### Session Authentication
- Enabled for browser-based dashboard
- Required for CSRF protection on HTML forms

### Endpoints
- `POST /api/token/` - Obtain JWT pair
- `POST /api/token/refresh/` - Refresh access token
- `POST /login/` - Universal login (renders page)
- `POST /logout/` - Session logout

### CSRF Protection
- Enabled for HTML forms
- **BROKEN FOR AJAX:** Missing tokens in JavaScript requests
- Trusted origins configured for production domain

---

## 4. API Endpoints

### Authentication
| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/token/` | POST | No | Get JWT tokens |
| `/api/token/refresh/` | POST | Yes | Refresh access token |
| `/api/test-auth/` | GET | Yes | Test authentication status |
| `/login/` | POST | No | Universal login endpoint |
| `/logout/` | POST | Yes | Logout |

### Users & Accounts
| Endpoint | Method | Auth | Role |
|----------|--------|------|------|
| `/api/accounts/register/` | POST | No | Public registration |
| `/api/accounts/profile/` | GET/PUT | Yes | Own profile |
| `/api/admin/users/` | GET | SuperAdmin | List all users |
| `/api/admin/users/<id>/` | PUT/DELETE | SuperAdmin | Manage users |

### Doctors
| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/doctors/` | GET/POST | Mixed* | List/create doctors |
| `/api/doctors/<id>/` | GET/PUT/DELETE | Mixed* | Doctor detail |
| `/api/availability/` | GET/POST | Doctor/Admin | Manage availability |
| `/api/public-availability/` | GET | No | Public slot display |
| `/hospital/doctors/` | GET | No | Public doctor listing |

* Doctors can edit own profile, HospitalAdmin can edit own hospital's doctors

### Appointments
| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/appointments/` | GET/POST | Mixed* | List/create appointments |
| `/api/appointments/<id>/` | GET/PUT/DELETE | Mixed* | Appointment detail |
| `/api/appointments/my-appointments/` | GET | Patient/Doctor | Own appointments |
| `/api/appointments/doctor-availabilities/` | GET | Mixed | Doctor slots |
| `/api/appointments/calendar/` | GET | Yes | Calendar data |
| `/api/appointments/book/` | POST | Yes | Book appointment |
| `/api/appointments/cancel/<id>/` | POST | Yes | Cancel appointment |

### Hospitals
| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/hospitals/` | GET/POST | Yes | List/create hospitals |
| `/api/hospitals/<id>/` | GET/PUT/DELETE | Yes | Hospital detail |
| `/api/hospitals/<id>/doctors/` | GET | Yes | Hospital's doctors |
| `/api/hospitals/<id>/departments/` | GET | Yes | Hospital's departments |
| `/api/hospitals/<id>/treatments/` | GET | Yes | Hospital's treatments |
| `/api/admin/hospitals/approve/<id>/` | POST | SuperAdmin | Approve hospital |

### Departments & Treatments
| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/departments/` | GET/POST | HospitalAdmin | CRUD |
| `/api/treatments/` | GET/POST | HospitalAdmin | CRUD |

### Patients
| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/patients/` | GET/POST | Yes | List/create patients |
| `/api/patients/<id>/` | GET/PUT | Yes | Patient detail |
| `/api/patients/<id>/records/` | GET | Doctor | Medical history |
| `/api/patients/<id>/reports/` | GET | Doctor | Generated reports |

### Search
| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/universal-search/` | GET | No | Search across entities |
| `/api/universal-search/semantic/` | GET | No | AI-powered search |

---

## 5. Frontend Pages

### Public Pages
| URL | Template | Purpose |
|-----|----------|---------|
| `/` | homepage.html | Landing page |
| `/register/` | register_hospital.html | Hospital registration |
| `/hospitals/` | hospital_listing.html | List hospitals |
| `/hospitals/<slug>/` | hospital_detail.html | Hospital details |
| `/doctor/login/` | doctor_login.html | Doctor login |
| `/hospital/login/` | hospital_login.html | Admin login |
| `/accounts/login/` | universal_login.html | Combined login |
| `/accounts/password-reset/` | request_password_reset.html | Forgot password |

### Authenticated - Patient
| URL | Template | Purpose |
|-----|----------|---------|
| `/hospital/<id>/appointments/` | hospital_appointments.html | Book appointment |
| `/appointments/my/` | my_appointments.html | View my appointments |
| `/accounts/profile/` | patient_profile.html | Edit profile |

### Authenticated - Doctor
| URL | Template | Purpose |
|-----|----------|---------|
| `/doctor/dashboard/` | doctor_dashboard.html | Doctor dashboard |
| `/doctor/availability/` | doctor_availability.html | Set availability |
| `/doctor/appointments/` | doctor_appointments.html | Manage appointments |

### Authenticated - Hospital Admin
| URL | Template | Purpose |
|-----|----------|---------|
| `/hospital/admin/` | hospital_admin/dashboard.html | Admin dashboard |
| `/hospital/admin/doctors/` | doctor_listing.html | Manage doctors |
| `/hospital/admin/register-doctor/` | hospital_admin/register.html | Add doctor |
| `/hospital/admin/departments/` | departments.html | Manage departments |
| `/hospital/admin/treatments/` | treatments.html | Manage treatments |
| `/hospital/admin/appointments/` | appointments_manage.html | Manage appointments |

### Widget
| URL | Purpose |
|-----|---------|
| `/widget/<hospital_id>/` | Embeddable appointment booking iframe |

---

## 6. Widget/Embedded System

**Purpose:** Allow external websites to embed RHMS appointment booking

**Implementation:**
- `/appointment_widget/` template renders standalone booking form
- Can be embedded via iframe: `<iframe src="https://rhms.blueglobaltechnology.com/widget/123/" width="100%" height="600"></iframe>`
- Hospital-specific branding (logo, colors)
- Multi-step booking wizard
- AJAX-based availability fetching
- Token generation
- Mobile-responsive design

**Technical:**
- No authentication required (public)
- CSRF token embedded in page
- jQuery-based interactivity
- Endpoint: `/mobile/book/` handles POST

---

## 7. Database Schema Overview

### Main Tables (MySQL)

```
auth_user (Django built-in)
├── id, username, email, password, first_name, last_name, ...

accounts_user (Custom User Model)
├── user_id (PK → auth_user.id)
├── phone, role, is_verified, verification_token, ...

hospitals_hospital
├── id, name, address, city, state, registration_number
├── phone_number, email, logo, status, created_at

hospitals_department
├── id, hospital_id (FK), name, description

hospitals_treatment
├── id, department_id (FK), name, description, price, duration

hospitals_hospitaladmin
├── id, user_id (FK), hospital_id (FK)

doctors_doctor
├── id, user_id (FK), hospital_id (FK), specialization
├── qualifications, experience_years, consultation_fee
├── doctor_image, is_available, bio, created_at

doctors_doctoravailability  ← PROBLEM: DUPLICATE TABLE ALSO IN appointments app
├── id, doctor_id (FK), date, start_time, end_time
├── is_available, is_booked
├── unique_together: (doctor, date, start_time, end_time)

appointments_appointment
├── id, patient_id (FK), doctor_id (FK), hospital_id (FK)
├── appointment_date, appointment_time
├── token_number, status, notes, created_at

appointments_doctoravailability  ← CANONICAL VERSION
├── id, doctor_id (FK), date, start_time, end_time
├── is_available, is_booked

patients_patient
├── id, user_id (FK OneToOne), hospital_id (FK)
├── dob, gender, blood_group, address, emergency_contact
├── medical_history, allergies

patients_medicalrecord
├── id, patient_id (FK), doctor_id (FK), diagnosis
├── prescription, visit_date, notes

notifications_notification
├── id, recipient_id (FK), actor_id (FK)
├── verb, timestamp, unread, target_object_id, ...

advertisements_advertisement
├── id, title, image, link, hospital_id (FK)
├── is_active, start_date, end_date
```

### Indexes Present
- Primary keys on all tables
- Foreign keys auto-indexed (InnoDB)
- `User.email` unique
- `Hospital.email` unique

### Indexes Missing (Performance Issues)
- `Hospital.phone_number` - frequently searched
- `Hospital.city`, `state` - filter queries
- `Patient.phone` - lookup by phone
- `Appointment` composite indexes:
  - `(doctor, appointment_date)`
  - `(hospital, appointment_date)`
  - `(token_number, status)`
- `DoctorAvailability` composite: `(doctor, date, is_available)`

---

## 8. Third-Party Integrations

### Django Packages
- **Django 5.2.7** - Web framework
- **DRF 3.16.1** - REST API
- **SimpleJWT 5.5.1** - JWT authentication
- **django-filter 25.2** - Filtering
- **django-notifications** (GitHub master) - Notification system
- **mysqlclient 2.2.7** - MySQL driver

### Frontend Libraries
- **Bootstrap 5** (CSS + JS) - UI framework
- **jQuery 3.x** - DOM manipulation
- **Toastr** - Notification toasts
- **FontAwesome** (assumed) - Icons

### ML/AI
- **sentence-transformers** - Semantic search embeddings
- **scikit-learn** - ML utilities
- **numpy** - Numerical operations

### Deployment
- **Gunicorn** - WSGI server
- **Docker** - Containerization (Dockerfile, docker-compose.yml)
- **AA Panel** - Hosting panel deployment guide

---

## 9. Not Yet Implemented / Roadmap

### Planned Features (Based on Code Comments & TODOs)
- Semantic search UI integration (core/semantic_search.py exists but not wired to frontend)
- Doctor monthly availability bulk upload (script exists in Devlopment/)
- Advanced appointment analytics dashboard
- Patient medical report PDF generation (models exist, view missing)
- SMS notifications (infrastructure not complete)
- Doctor video consultation integration
- Multi-language support
- Responsive mobile app (APIs ready)
- Insurance claim management
- Pharmacy/inventory module
- Lab test management
- Bed management system

### In Progress
- Docker deployment configuration
- AA panel deployment setup
- Production security hardening

---

## Known Issues Blocking Features

| Feature | Blocker | Priority |
|---------|---------|----------|
| Appointment booking | CSRF token missing in AJAX | Critical |
| Doctor availability | Duplicate model in 2 apps | High |
| All forms | CSRF exemptions on endpoints | Critical |
| Admin dashboard | Broken template inheritance | High |
| Public doctor listing | URL name mismatch | Medium |
| Security | Hardcoded credentials | Critical |
| Data integrity | FK default=1 | High |

---

## Conclusion

RHMS is a **feature-complete** hospital management system with well-designed modules for all core operations. The architecture follows Django best practices with separation of concerns, REST APIs, and role-based access control.

However, **quality issues** are significant:
- Multiple critical security vulnerabilities
- Data model inconsistencies
- Broken frontend templates
- Runtime errors in production code
- Missing CSRF protection on AJAX

**Recommendation:** Address all Critical and High severity issues before production deployment. The codebase is otherwise well-structured and maintainable once these foundational problems are fixed.
