# Hospital Module - Development Documentation

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Database Models](#database-models)
- [User Roles & Permissions](#user-roles--permissions)
- [API Endpoints](#api-endpoints)
- [Workflow Flows](#workflow-flows)
- [Frontend Views](#frontend-views)
- [Key Business Logic](#key-business-logic)
- [Security Considerations](#security-considerations)

---

## Architecture Overview

### Tech Stack
- **Backend**: Django 5.x with Django REST Framework
- **Database**: PostgreSQL
- **Frontend**: Django Templates + Vanilla JS
- **Authentication**: Custom User Model with email-based auth

### Project Structure
```
revana_hms/
├── hospitals/           # Hospital management app
│   ├── models.py      # Hospital, HospitalAdmin, Department, Treatment
│   ├── views.py      # ViewSets & TemplateViews
│   ├── serializers.py
│   ├── urls.py
│   ├── api_views.py  # REST API endpoints
│   ├── api_urls.py
│   └── utils.py      # Utility functions
├── accounts/         # User authentication & profiles
│   ├── models.py    # User, HospitalAdminProfile, DoctorProfile
│   └── views.py
├── doctors/          # Doctor management
├── appointments/    # Appointment & queue management
└── patients/        # Patient management
```

---

## Database Models

### 1. Hospital (`hospitals.Hospital`)
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `name` | CharField(200) | Hospital name |
| `registration_number` | CharField(100) | Unique registration ID |
| `email` | EmailField | Unique hospital email |
| `logo` | ImageField | Hospital logo image |
| `address` | TextField | Full address |
| `phone_number` | CharField(20) | Contact number |
| `city` | CharField(100) | City |
| `state` | CharField(50) | State (default: Gujarat) |
| `country` | CharField(50) | Country (default: India) |
| `status` | CharField(20) | pending/approved/rejected |
| `is_approved` | BooleanField | Approval flag |
| `hospital_type` | JSONField | Types array (general, multispeciality) |
| `hours` | JSONField | Operating hours dict |
| `created_at` | DateTimeField | Auto timestamp |

**Status Constants:**
```python
STATUS_PENDING = 'pending'
STATUS_APPROVED = 'approved'
STATUS_REJECTED = 'rejected'
```

### 2. HospitalAdmin (`hospitals.HospitalAdmin`)
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `user` | OneToOneField | Link to User model |
| `hospital` | ForeignKey | Link to Hospital |

### 3. Department (`hospitals.Department`)
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `hospital` | ForeignKey | Link to Hospital |
| `name` | CharField(100) | Department name |

### 4. Treatment (`hospitals.Treatment`)
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `hospital` | ForeignKey | Link to Hospital |
| `department` | ForeignKey | Link to Department |
| `name` | CharField(100) | Treatment name |

---

## User Roles & Permissions

### Role Hierarchy
```
SuperAdmin (System Admin)
    ↓
    ├── HospitalAdmin (Hospital Manager)
    │       ↓
    │       ├── Doctor
    │       └── Staff
    │
    └── Patient (End User)
```

### Role Definitions

| Role | Description | Permissions |
|------|-------------|--------------|
| `superadmin` | System administrator | Full system access, approve/reject hospitals |
| `hospital_admin` | Hospital manager | Manage own hospital, departments, treatments |
| `doctor` | Medical practitioner | Manage appointments, availability |
| `patient` | End user | Book appointments, view records |

### Permission Classes

**Location**: `core/permissions.py`

```python
IsSuperAdmin      # Only superusers can access
IsHospitalAdminOfSameHospital  # Hospital admin accessing own hospital data
IsAuthenticated # Any authenticated user
IsAuthenticatedOrReadOnly    # Read for all, write for authenticated
```

---

## API Endpoints

### Public Endpoints (No Auth Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/hospitals/register/` | Register new hospital |
| GET | `/api/hospitals/` | List approved hospitals |
| GET | `/hospitals/departments/` | List all departments |
| GET | `/hospitals/departments/<id>/` | Department detail |

### Authentication Required

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/hospitals/hospitals/` | CRUD hospital |
| POST | `/superadmin/hospital/approve/<id>/` | Approve hospital (SuperAdmin) |
| POST | `/superadmin/hospital/reject/<id>/` | Reject hospital (SuperAdmin) |
| GET/POST | `/hospitals/manage/departments/` | Manage departments |
| GET/POST | `/hospitals/manage/treatments/` | Manage treatments |

### API Endpoints Detail

#### 1. Hospital Registration
```
POST /hospitals/register/
Content-Type: application/json

Request:
{
    "name": "City Hospital",
    "registration_number": "CH/2024/001",
    "email": "admin@cityhospital.com",
    "address": "123 Main Road, Surat",
    "phone_number": "+912612345678",
    "city": "Surat"
}

Response (201):
{
    "message": "Hospital submitted for approval",
    "hospitalId": 1
}
```

#### 2. Hospital List (Public)
```
GET /api/hospitals/

Response (200):
[
    {
        "id": 1,
        "name": "City Hospital",
        "city": "Surat",
        "logo": "/media/hospitals/1/logo.png",
        "hospital_type": ["general", "multispeciality"],
        "email": "admin@cityhospital.com",
        "p_number": "+912612345678",
        "address": "123 Main Road, Surat",
        "total_doctors": 5,
        "total_departments": 8
    }
]
```

#### 3. Approve Hospital (SuperAdmin)
```
POST /superadmin/hospital/approve/1/

Response (200):
{
    "status": "success",
    "message": "Hospital approved successfully"
}
```

---

## Workflow Flows

### 1. Hospital Registration Flow

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  User submits   │────▶│  Hospital saved  │────▶│  Status set to   │
│  registration   │     │  with pending    │     │  'pending'      │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Hospital      │◀────│  Admin reviews   │◀────│  SuperAdmin    │
│  admin logs in │     │  & approves      │     │  notified      │
└─────────────────┘     └──────────────────┘     └───────────���─────┘
```

**Step-by-Step:**
1. User fills hospital registration form
2. Hospital saved with `status='pending'`
3. SuperAdmin reviews in admin dashboard
4. If approved: `status='approved'`, credentials sent via email
5. If rejected: `status='rejected'`, notification sent

### 2. Hospital Admin Dashboard Flow

```
┌────────────────────────────────────────────────────────────────┐
│                  Hospital Admin Login                         │
└────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌────────────────────────────────────────────────────────────────┐
│  Dashboard Options:                                           │
│  ├─ Manage Departments                                        │
│  ├─ Manage Treatments                                          │
│  ├─ Manage Doctors (pending approved)                         │
│  ├─ View Appointments                                         │
│  └─ Hospital Settings                                         │
└────────────────────────────────────────────────────────────────┘
```

### 3. Patient Appointment Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Patient     │────▶│  Select      │────▶│  Select      │
│  visits site │     │  Hospital    │     │  Department  │
└──────────────┘     └──────────────┘     └──────────────┘
                                                │
                                                ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Appointment │◀────│  Select     │◀────│  Select      │
│  confirmed   │     │  Doctor     │     │  Date/Time  │
└──────────────┘     └──────────────┘     └──────────────┘
```

### 4. Doctor Management Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Doctor      │────▶│  Hospital   │────▶│  SuperAdmin │
│  applies    │     │  Admin      │     │  approves   │
│             │     │  validates │     │             │
└──────────────┘     └──────────────┘     └──────────────┘
```

### 5. Department & Treatment Management

```
Hospital Admin
    │
    ├── Create Department
    │       └── Name: "Cardiology"
    │
    └── Create Treatment (per department)
            └── Name: "ECG Test", Department: "Cardiology"
```

---

## Frontend Views

### Template Files

| View | Template | Description |
|------|----------|-------------|
| Register | `register.html` | Hospital self-registration |
| Manage Departments | `hospitals/manage_departments.html` | CRUD departments |
| Manage Treatments | `hospitals/manage_treatments.html` | CRUD treatments |
| Department List | `frontend/departments.html` | Public department listing |
| Department Detail | `frontend/department_detail.html` | Department detail with doctors |

### URL Patterns

**Location**: `hospitals/urls.py`

```python
urlpatterns = [
    path('api/', include(router.urls)),
    path('superadmin/hospital/approve/<int:hospital_id>/', approve_hospital_view, name='approve_hospital'),
    path('superadmin/hospital/reject/<int:hospital_id>/', reject_hospital_view, name='reject_hospital'),
    path('nearby/', get_nearby_hospitals, name='nearby_hospitals'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('manage/departments/', views.manage_departments, name='manage_departments'),
    path('manage/treatments/', views.manage_treatments, name='manage_treatments'),
    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:department_id>/', views.department_detail, name='department_detail'),
]
```

---

## Key Business Logic

### 1. Hospital Approval & Credential Generation

**Location**: `hospitals/utils.py`

```python
def approve_hospital_and_notify(hospital_id):
    """Approve hospital and generate admin credentials."""
    hospital = Hospital.objects.get(id=hospital_id)
    
    # Generate secure password
    password = secrets.token_urlsafe(10)
    
    # Create user account
    user, created = User.objects.get_or_create(
        username=hospital.email,
        defaults={'email': hospital.email, 'is_staff': True}
    )
    user.set_password(password)
    user.save()
    
    # Link to hospital
    HospitalAdmin.objects.get_or_create(user=user, hospital=hospital)
    
    # Update status
    hospital.status = Hospital.STATUS_APPROVED
    hospital.is_approved = True
    hospital.save()
    
    # Send credentials email
    send_mail(
        subject='Hospital Approved',
        message=f'Username: {hospital.email}\nPassword: {password}',
        recipient_list=[hospital.email]
    )
```

### 2. Filtering Only Approved Hospitals

**In all public-facing views, filter by approved status:**

```python
def get_queryset(self):
    return Hospital.objects.filter(status=Hospital.STATUS_APPROVED)

# Department list
def department_list(request):
    departments = Department.objects.select_related('hospital').filter(
        hospital__status=Hospital.STATUS_APPROVED
    )
```

### 3. Hospital Admin Authorization

```python
@login_required
def manage_departments(request):
    try:
        hospital_admin = HospitalAdmin.objects.get(user=request.user)
        hospital = hospital_admin.hospital
    except HospitalAdmin.DoesNotExist:
        messages.error(request, "You are not authorized.")
        return redirect('homepage')
```

---

## Security Considerations

### 1. Data Protection
- ❌ **Never expose** pending hospitals in public listings
- ❌ **Never show** pending hospital details to patients
- ❌ **Block appointments** for non-approved hospitals

### 2. Authorization Rules
- ✅ Only `hospital_admin` can manage their own hospital
- ✅ Only `superadmin` can approve/reject hospitals
- ✅ All CRUD operations require authentication

### 3. API Security
```python
# Always check permissions
permission_classes = [permissions.IsAuthenticated]
# For admin operations
permission_classes = [permissions.IsAdminUser]
```

### 4. Email Credentials
- Passwords generated **only on approval** (not during registration)
- Credentials sent via **email** after superadmin approval

---

## Database Schema (ERD)

```
┌─────────────────┐       ┌─────────────────┐
│      User       │       │    Hospital    │
├─────────────────┤       ├��────────────────┤
│ id (PK)         │◀──────│ id (PK)        │
│ email           │       │ name           │
│ role            │       │ registration_   │
│ is_active       │       │   number       │
│ is_staff        │       │ email         │
└─────────────────┘       │ status        │
         │                │ is_approved   │
         │                └─────────────────┘
         │                       │
         │                       │
    ┌────┴─────┐       ┌─────┴──────┐
    │Hospital   │       │Department   │
    │Admin      │       ├─────────────┤
    ├───────────│       │id (PK)     │
    │user_id   │◀─────│hospital_id │
    │hospital_ │       │name        │
    │  id      │       └─────────────┘
    └───────────│              │
               │       ┌──────┴────────┐
               │       │  Treatment    │
               │       ├──────────────┤
               │       │ id (PK)      │
               │       │department_id │
               └───────│hospital_id  │
                      │name          │
                      └──────────────┘

    ┌─────────────────┐       ┌─────────────────┐
    │    Doctor       │       │   Appointment   │
    ├─────────────────┤       ├─────────────────┤
    │ id (PK)         │◀──────│ id (PK)         │
    │ hospital_id    ─┼──────▶│ hospital_id     │
    │ department_id ──┼──────▶│ doctor_id       │
    │ name            │       │ patient_name    │
    │ status         │       │ appointment_   │
    │ is_approved    │       │   date         │
    └─────────────────┘       │ status        │
                                └─────────────────┘
```

---

## File Reference Guide

| File | Purpose | Key Functions/Classes |
|------|---------|---------------------|
| `hospitals/models.py` | Database models | `Hospital`, `HospitalAdmin`, `Department`, `Treatment` |
| `hospitals/views.py` | Web views | `RegisterView`, `HospitalViewSet`, `manage_departments` |
| `hospitals/api_views.py` | REST API | `HospitalRegisterAPI`, `HospitalListAPI`, `ApproveHospitalAPI` |
| `hospitals/serializers.py` | DRF serializers | `HospitalRegisterSerializer`, `HospitalPublicSerializer` |
| `hospitals/urls.py` | URL routing | All URL patterns |
| `hospitals/utils.py` | Utilities | `approve_hospital_and_notify` |
| `accounts/models.py` | User models | `User`, `HospitalAdminProfile`, `DoctorProfile` |
| `doctors/models.py` | Doctor models | `Doctor`, `DoctorAvailability` |
| `appointments/models.py` | Appointment models | `Appointment`, `DoctorAvailability`, `DailyQueue` |

---

## Quick Reference: Common Tasks

### Create New Hospital
```python
hospital = Hospital.objects.create(
    name="New Hospital",
    registration_number="NH/001",
    email="admin@newhospital.com",
    address="Address",
    phone_number="+912612345678",
    city="Surat",
    status=Hospital.STATUS_PENDING
)
```

### Approve Hospital
```python
hospital = Hospital.objects.get(id=1)
hospital.status = Hospital.STATUS_APPROVED
hospital.is_approved = True
hospital.save()
```

### Get Hospital Admin's Hospital
```python
hospital_admin = HospitalAdmin.objects.get(user=request.user)
hospital = hospital_admin.hospital
```

### Filter Approved Hospitals Only
```python
approved_hospitals = Hospital.objects.filter(status=Hospital.STATUS_APPROVED)
```

### Create Department
```python
department = Department.objects.create(
    hospital=hospital,
    name="Cardiology"
)
```

---

## Migration History

| Migration | Description |
|-----------|-------------|
| 0001_initial | Create Hospital, HospitalAdmin |
| 0002_rename | Rename fields |
| 0003_remove | Remove legacy fields |
| 0004_add_country_state | Add location fields |
| 0005_hospital_type | Add hospital_type JSONField |
| 0006_hospital_is_approved | Add is_approved boolean |
| 0007_alter_hospital_type | Alter field types |
| 0008_alter_hospital_type | Further type changes |
| 0009_alter_hospital_type | Additional changes |
| 0010_alter_hospital_logo | Add logo field |
| 0011_department_code | Add department code (unused) |
| 0012_alter_hospitaladmin | Alter relations |
| 0013_remove_department_code | Remove unused code field |

---

## Testing Checklist

### Hospital Registration
- [ ] New hospital can register with all required fields
- [ ] Duplicate email rejected
- [ ] Duplicate registration_number rejected
- [ ] Default status is 'pending'

### Hospital Approval (SuperAdmin)
- [ ] SuperAdmin can approve pending hospital
- [ ] Credentials email sent on approval
- [ ] HospitalAdmin user created automatically
- [ ] Status changes to 'approved'

### Public Listings
- [ ] Only approved hospitals shown
- [ ] Pending hospitals NOT visible
- [ ] Departments filtered by hospital approval

### Hospital Admin Features
- [ ] Can create departments
- [ ] Can create treatments
- [ ] Cannot access other hospital's data

---

*Last Updated: April 2026*
*Version: 1.0*