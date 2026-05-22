# phase_one_testing

Perfect Bhavan — let’s start by creating the **Super Admin** user. This account will have full access to all models and admin actions.

---

## ✅ Step 1: Create Super Admin via CLI

Run this command in your terminal:

```bash
python manage.py createsuperuser
```

You’ll be prompted to enter:

- **Username**: e.g., `admin`
- **Email**: e.g., `admin@revana.com`
- **Password**: (choose a secure one)

---

## ✅ Step 2: Login to Django Admin

- Go to: `http://127.0.0.1:8000/admin/`
- Login with the superuser credentials
- You should see full access to:
  - Hospitals
  - Departments
  - Treatments
  - Doctors
  - Appointments
  - Users
  - Groups

---

## ✅ Step 3: Confirm Permissions

- Try creating a hospital
- Try approving a doctor
- Try accessing all viewsets via API (e.g., `/api/doctors/`, `/api/hospitals/`)

✅ If everything works, your super admin is ready.

---

Let me know once you’ve created and logged in — I’ll guide you to test hospital creation next.