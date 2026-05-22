# Hospital Registration Workflow - Development Guide

## Table of Contents
- [Overview](#overview)
- [User Flow Diagram](#user-flow-diagram)
- [Step-by-Step Workflow](#step-by-step-workflow)
- [Technical Implementation](#technical-implementation)
- [API Specifications](#api-specifications)
- [Frontend Implementation](#frontend-implementation)
- [Backend Implementation](#backend-implementation)
- [Database Schema](#database-schema)
- [Email Notifications](#email-notifications)
- [Security Considerations](#security-considerations)
- [Testing Checklist](#testing-checklist)

---

## Overview

The Hospital Registration feature allows new hospitals to:
1. **Register** themselves through a public form
2. **Wait** for admin approval (status = pending)
3. **Receive credentials** via email after approval
4. **Access** the hospital admin dashboard

### Key States

```
┌──────────┐     ┌─────────┐     ┌──────────┐
│ pending  │────▶│approved │────▶│ rejected│
│ (initial)     (active)      (denied)
└──────────┘     └─────────┘     └──────────┘
```

---

## User Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    HOSPITAL REGISTRATION FLOW                         │
└──────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
  │  Hospital  │         │   Backend   │         │  SuperAdmin│
  │    User   │         │    (API)    │         │  Dashboard │
  └─────┬─────┘         └─────┬─────┘         └─────┬─────┘
        │                    │                    │
        │ POST /register    │                    │
        │ ──────────────▶   │                    │
        │                  │                    │
        │                  │ Save: status='pending'
        │                  │ ─────────────────▶ [Database]
        │                  │                    │
        │                  │ Response: 201 Created
        │ ◀────────────────│
        │                  │                    │
        │ "Submitted for   │                    │
        │   approval"     │                    │
        │                  │                    │
        │                  │                    │ View pending hospitals
        │                  │ ◀─────────────────
        │                  │                    │
        │                  │                    │ POST /approve/<id>
        │                  │                    │ ────────────────▶
        │                  │                    │
        │                  │ status='approved'  │
        │                  │ ◀─────────────────���│
        │                  │                    │
        │                  │ Generate password  │
        │                  │ Create User       │
        │                  │ Link HospitalAdmin│
        │                  │ Send email        │
        │                  │ ──────────────────▶[Email Service]
        │                  │                    │
        │                  │ Response: success  │
        │ ◀─────────────────────────────────────
        │                  │                    │

        │                                          │
        │   Email received                         │
        │ ┌─────────────────────────────────┐    │
        │ │  Hospital Approved!             │    │
        │ │  Username: admin@hospital.com   │    │
        │ │  Password: xxxxxxxx             │    │
        │ │  Login: /admin/                 │    │
        │ └─────────────────────────────────┘    │
        │                                          │
        │ ▼                                        ▼
        │ ─────────────────────────────────────────
        │         LOGIN TO DASHBOARD
```


---

## Step-by-Step Workflow

### Phase 1: Hospital Registration

| Step | Actor | Action | Result |
|------|-------|-------|--------|--------|
| 1.1 | Hospital User | Opens registration page | Form displayed |
| 1.2 | Hospital User | Fills hospital details | Form validated |
| 1.3 | Hospital User | Submits form | API called |
| 1.4 | Backend | Validates input | ✅ Valid or ❌ Error |
| 1.5 | Backend | Checks duplicates | Email/RegNo unique |
| 1.6 | Backend | Creates Hospital record | `status='pending'` |
| 1.7 | Backend | Returns response | 201 Created |

### Phase 2: Admin Approval

| Step | Actor | Action | Result |
|------|-------|--------|--------|
| 2.1 | SuperAdmin | Views pending hospitals | List displayed |
| 2.2 | SuperAdmin | Reviews details | - |
| 2.3 | SuperAdmin | Clicks Approve | API called |
| 2.4 | Backend | Updates status | `status='approved'` |
| 2.5 | Backend | Generates password | 10-char token |
| 2.6 | Backend | Creates User account | is_staff=True |
| 2.7 | Backend | Links HospitalAdmin | Profile created |
| 2.8 | Backend | Sends email | Credentials delivered |
| 2.9 | Backend | Returns success | 200 OK |

### Phase 3: Rejection (Optional)

| Step | Actor | Action | Result |
|------|-------|--------|--------|
| 3.1 | SuperAdmin | Reviews hospital | - |
| 3.2 | SuperAdmin | Clicks Reject | API called |
| 3.3 | Backend | Updates status | `status='rejected'` |
| 3.4 | Backend | Sends rejection email | Notification sent |

---

## Technical Implementation

### URL Routing

**File**: `hospitals/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    # Public endpoint
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # API endpoints
    path('api/register-hospital/', views.hospital_register_api, name='register_api'),
    path('superadmin/hospital/approve/<int:hospital_id>/', views.approve_hospital_view, name='approve_hospital'),
    path('superadmin/hospital/reject/<int:hospital_id>/', views.reject_hospital_view, name='reject_hospital'),
]
```

### View Implementation

**File**: `hospitals/views.py`

```python
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .models import Hospital, HospitalAdmin
from .serializers import HospitalRegisterSerializer
import secrets

User = get_user_model()

class RegisterView(TemplateView):
    template_name = 'hospital_admin/register.html'


@csrf_exempt
@require_POST
def hospital_register_api(request):
    """
    Register a new hospital with status='pending'.
    Public endpoint - no authentication required.
    """
    serializer = HospitalRegisterSerializer(data=request.POST)
    if serializer.is_valid():
        hospital = serializer.save()  # status defaults to 'pending'
        return JsonResponse({
            'success': True,
            'message': 'Hospital submitted for approval',
            'hospitalId': hospital.id
        }, status=201)
    else:
        return JsonResponse({
            'success': False,
            'errors': serializer.errors
        }, status=400)


@login_required
@require_POST
def approve_hospital_view(request, hospital_id):
    """
    Approve a hospital and send credentials.
    Requires superuser/admin privileges.
    """
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        hospital = Hospital.objects.get(id=hospital_id, status='pending')
    except Hospital.DoesNotExist:
        return JsonResponse({'error': 'Hospital not found'}, status=404)
    
    # Generate password
    password = secrets.token_urlsafe(10)
    
    # Create or update user
    user, created = User.objects.get_or_create(
        username=hospital.email,
        defaults={
            'email': hospital.email,
            'is_staff': True,
            'is_superuser': False
        }
    )
    user.set_password(password)
    user.save()
    
    # Update hospital status
    hospital.status = 'approved'
    hospital.is_approved = True
    hospital.save()
    
    # Link HospitalAdmin profile
    HospitalAdmin.objects.get_or_create(user=user, hospital=hospital)
    
    # Send credentials email
    try:
        send_mail(
            subject='Hospital Approved - Admin Credentials',
            message=(
                f'Dear {hospital.name},\n\n'
                f'Your hospital has been approved.\n\n'
                f'Login: http://localhost:8000/admin/\n'
                f'Username: {hospital.email}\n'
                f'Password: {password}\n\n'
                f'Please change your password after first login.'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[hospital.email],
            fail_silently=False,
        )
    except Exception as e:
        # Log error but don't fail the approval
        print(f"Email failed: {e}")
    
    return JsonResponse({
        'success': True,
        'message': 'Hospital approved and credentials sent'
    })


@login_required
@require_POST
def reject_hospital_view(request, hospital_id):
    """
    Reject a hospital.
    """
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        hospital = Hospital.objects.get(id=hospital_id)
    except Hospital.DoesNotExist:
        return JsonResponse({'error': 'Hospital not found'}, status=404)
    
    hospital.status = 'rejected'
    hospital.save()
    
    # Send rejection notification
    try:
        send_mail(
            subject='Hospital Registration Update',
            message=(
                f'Dear {hospital.name},\n\n'
                f'Your hospital registration has been rejected.\n'
                f'Please contact support for more information.'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[hospital.email],
        )
    except Exception as e:
        print(f"Email failed: {e}")
    
    return JsonResponse({
        'success': True,
        'message': 'Hospital rejected'
    })
```

---

## API Specifications

### 1. Register Hospital

```
POST /api/register-hospital/
Content-Type: multipart/form-data

Request Fields:
├── name              : string (required) - Hospital name
├── registration_number: string (required) - Unique registration ID
├── email             : string (required) - Valid email
├── phone_number      : string (required) - Contact number
├── address          : string (required) - Full address
├── city             : string (required) - City
├── state            : string (optional) - State (default: Gujarat)
├── country          : string (optional) - Country (default: India)
├── hospital_type    : string (optional) - Type (general, multispeciality)
├── logo             : file (optional) - Image file
└── hours            : JSON (optional) - Operating hours

Success Response (201):
{
    "success": true,
    "message": "Hospital submitted for approval",
    "hospitalId": 1
}

Error Response (400):
{
    "success": false,
    "errors": {
        "email": ["Hospital with this email already exists."],
        "registration_number": ["Hospital with this registration number already exists."]
    }
}
```

### 2. Approve Hospital

```
POST /superadmin/hospital/approve/<hospital_id>/
Authorization: Required (superuser)
Content-Type: application/json

Success Response (200):
{
    "success": true,
    "message": "Hospital approved and credentials sent"
}

Error Responses:
- 403: {"error": "Permission denied"}
- 404: {"error": "Hospital not found"}
```

### 3. Reject Hospital

```
POST /superadmin/hospital/reject/<hospital_id>/
Authorization: Required (superuser)

Success Response (200):
{
    "success": true,
    "message": "Hospital rejected"
}
```


---

## Frontend Implementation

### Registration Form Template

**File**: `templates/hospital_admin/register.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hospital Registration</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h4 class="mb-0">Hospital Registration</h4>
                    </div>
                    <div class="card-body">
                        <form id="hospitalForm" enctype="multipart/form-data">
                            <!-- Hospital Name -->
                            <div class="mb-3">
                                <label class="form-label">Hospital Name *</label>
                                <div class="input-group">
                                    <span class="input-group-text"><i class="fa fa-hospital"></i></span>
                                    <input type="text" class="form-control" name="name" required>
                                </div>
                            </div>

                            <!-- Hospital Type -->
                            <div class="mb-3">
                                <label class="form-label">Hospital Type *</label>
                                <select class="form-select" name="hospital_type" required>
                                    <option value="">Select Type</option>
                                    <option value="General Hospital">General Hospital</option>
                                    <option value="Multi-Speciality">Multi-Speciality</option>
                                    <option value="Clinic">Clinic</option>
                                    <option value="Diagnostic Center">Diagnostic Center</option>
                                </select>
                            </div>

                            <!-- Phone & Email -->
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Phone Number *</label>
                                    <input type="text" class="form-control" name="phone_number" 
                                           placeholder="+91XXXXXXXXXX" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Email *</label>
                                    <input type="email" class="form-control" name="email" required>
                                </div>
                            </div>

                            <!-- Registration Number -->
                            <div class="mb-3">
                                <label class="form-label">Registration Number *</label>
                                <input type="text" class="form-control" name="registration_number" required>
                            </div>

                            <!-- Address -->
                            <div class="mb-3">
                                <label class="form-label">Address *</label>
                                <textarea class="form-control" name="address" rows="2" required></textarea>
                            </div>

                            <!-- City/State/Country -->
                            <div class="row">
                                <div class="col-md-4 mb-3">
                                    <label class="form-label">City *</label>
                                    <input type="text" class="form-control" name="city" required>
                                </div>
                                <div class="col-md-4 mb-3">
                                    <label class="form-label">State</label>
                                    <input type="text" class="form-control" name="state" value="Gujarat">
                                </div>
                                <div class="col-md-4 mb-3">
                                    <label class="form-label">Country</label>
                                    <input type="text" class="form-control" name="country" value="India">
                                </div>
                            </div>

                            <!-- Logo Upload -->
                            <div class="mb-3">
                                <label class="form-label">Hospital Logo</label>
                                <input type="file" class="form-control" name="logo" accept="image/*">
                            </div>

                            <!-- Submit -->
                            <div class="text-center">
                                <button type="submit" class="btn btn-primary">Register Hospital</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Scripts -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.css" rel="stylesheet">

    <script>
    $(document).ready(function() {
        $('#hospitalForm').on('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            try {
                const response = await fetch('/api/register-hospital/', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    toastr.success(data.message);
                    setTimeout(() => {
                        window.location.href = '/hospital/login/';
                    }, 2000);
                } else {
                    toastr.error(data.errors || 'Registration failed');
                }
            } catch (error) {
                toastr.error('Network error occurred');
            }
        });
    });
    </script>
</body>
</html>
```


---

## Backend Implementation

### Model Definition

**File**: `hospitals/models.py`

```python
from django.db import models

class Hospital(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    logo = models.ImageField(upload_to='hospitals/logos/', blank=True, null=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50, default='Gujarat')
    country = models.CharField(max_length=50, default='India')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    is_approved = models.BooleanField(default=False)
    hospital_type = models.JSONField(default=list, blank=True)
    hours = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rhms_hospitals'

    def __str__(self):
        return self.name


class HospitalAdmin(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.hospital.name}"
```

### Serializer

**File**: `hospitals/serializers.py`

```python
from rest_framework import serializers
from .models import Hospital

class HospitalRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = [
            'name',
            'registration_number',
            'email',
            'logo',
            'address',
            'phone_number',
            'city',
            'state',
            'country',
            'hospital_type',
            'hours',
        ]
        extra_kwargs = {
            'state': {'default': 'Gujarat'},
            'country': {'default': 'India'},
            'hospital_type': {'default': []},
            'hours': {'default': {}},
        }

    def validate_email(self, value):
        if Hospital.objects.filter(email=value).exists():
            raise serializers.ValidationError("Hospital with this email already exists.")
        return value

    def validate_registration_number(self, value):
        if Hospital.objects.filter(registration_number=value).exists():
            raise serializers.ValidationError("Hospital with this registration number already exists.")
        return value
```


---

## Database Schema

### Hospital Table

| Column | Type | Constraints | Default |
|--------|------|-------------|---------|
| id | BIGINT | PK | AUTO |
| name | VARCHAR(200) | NOT NULL | - |
| registration_number | VARCHAR(100) | UNIQUE, NOT NULL | - |
| email | VARCHAR(254) | UNIQUE, NOT NULL | - |
| logo | VARCHAR(100) | NULLABLE | NULL |
| address | TEXT | NOT NULL | - |
| phone_number | VARCHAR(20) | NOT NULL | - |
| city | VARCHAR(100) | NOT NULL | - |
| state | VARCHAR(50) | NOT NULL | Gujarat |
| country | VARCHAR(50) | NOT NULL | India |
| status | VARCHAR(20) | NOT NULL | pending |
| is_approved | BOOLEAN | NOT NULL | false |
| hospital_type | JSON | NULLABLE | [] |
| hours | JSON | NULLABLE | {} |
| created_at | TIMESTAMP | NOT NULL | AUTO |

### HospitalAdmin Table

| Column | Type | Constraints |
|--------|------|------------|
| id | BIGINT | PK |
| user_id | BIGINT | FK → auth_user.id |
| hospital_id | BIGINT | FK → rhms_hospitals |


---

## Email Notifications

### 1. Approval Email

```
Subject: Hospital Approved - Admin Credentials

Body:
Dear [Hospital Name],

Your hospital has been approved.

Login: http://localhost:8000/admin/
Username: [hospital_email]
Password: [generated_password]

Please change your password after first login.

Thanks,
RHMS Team
```

### 2. Rejection Email

```
Subject: Hospital Registration Update

Body:
Dear [Hospital Name],

Your hospital registration has been rejected.
Please contact support for more information.

Thanks,
RHMS Team
```


---

## Security Considerations

### 1. Input Validation
- ✅ All required fields must be validated
- ✅ Email format validation
- ✅ Phone number format validation
- ✅ Unique constraints on email & registration_number

### 2. Authorization
- ✅ Registration endpoint is PUBLIC (no auth needed)
- ✅ Approval endpoint requires `is_superuser=True`
- ✅ Rejection endpoint requires `is_superuser=True`

### 3. Data Protection
- ❌ NEVER show pending hospitals in public listings
- ❌ DO NOT generate credentials during registration
- ✅ Only generate credentials on approval

### 4. Password Security
- ✅ Use `secrets.token_urlsafe(10)` for secure password generation
- ✅ Never store plain text passwords (use Django's `set_password()`)


---

## Testing Checklist

### Registration Flow
- [ ] Can register with all required fields
- [ ] Form validation works (required fields)
- [ ] Duplicate email shows error
- [ ] Duplicate registration_number shows error
- [ ] Logo upload works
- [ ] Response shows success message
- [ ] Hospital saved with status='pending'

### Approval Flow
- [ ] Non-admin cannot approve (403 error)
- [ ] Approve hospital returns success
- [ ] Status changes to 'approved'
- [ ] is_approved=True
- [ ] User account created
- [ ] HospitalAdmin linked
- [ ] Email sent with credentials

### Rejection Flow
- [ ] Non-admin cannot reject (403 error)
- [ ] Status changes to 'rejected'
- [ ] Rejection email sent

### Public Listings
- [ ] Pending hospitals NOT visible
- [ ] Only approved hospitals in list
- [ ] Department filter works

### Dashboard Access
- [ ] Approved hospital admin can login
- [ ] Pending hospital admin CANNOT login
- [ ] Rejected hospital admin CANNOT login

---

*Last Updated: April 2026*
*Version: 1.0*