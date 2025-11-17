import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Patient

User = get_user_model()


# ----------------------------------------------------
# ✅ Patient Dashboard
# ----------------------------------------------------
@login_required
def patient_dashboard(request):
    return render(request, 'patients/patient_dashboard.html')


# ----------------------------------------------------
# ✅ Render Registration Page
# ----------------------------------------------------
def patient_register_page(request):
    return render(request, "patients/register.html")


# ----------------------------------------------------
# ✅ Handle Patient Registration (API)
# ----------------------------------------------------
@csrf_exempt
def register_patient(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            email = data.get("email")
            password = data.get("password")
            name = data.get("name")
            age = data.get("age")
            gender = data.get("gender")
            phone = data.get("phone")
            address = data.get("address")

            # Validation
            if not email:
                return JsonResponse({"message": "Email is required."}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "Email already registered!"}, status=400)

            # Create User
            user = User.objects.create_user(email=email, password=password)
            user.first_name = name
            user.save()

            # Create Patient Profile
            Patient.objects.create(
                user=user,
                age=age or 0,
                gender=gender or "Other",
                phone=phone or "",
                address=address or "",
            )

            return JsonResponse({"message": "Patient registered successfully!"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON format."}, status=400)

        except Exception as e:
            return JsonResponse({"message": f"Server error: {str(e)}"}, status=500)

    return JsonResponse({"message": "Only POST method allowed."}, status=405)


# ----------------------------------------------------
# ✅ Render Login Page
# ----------------------------------------------------
def login_page(request):
    return render(request, "patients/login.html")


# ----------------------------------------------------
# ✅ Handle Login Request (API)
# ----------------------------------------------------
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            email = data.get("email")
            password = data.get("password")

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({"message": "Login successful"}, status=200)

            return JsonResponse({"message": "Invalid email or password"}, status=401)

        except Exception as e:
            return JsonResponse({"message": f"Server error: {str(e)}"}, status=500)

    return JsonResponse({"message": "Only POST method allowed."}, status=405)


# ----------------------------------------------------
# ✅ Update Profile (Logged-in User)
# ----------------------------------------------------
@login_required
@csrf_exempt
def update_profile(request):
    if request.method == "POST":
        try:
            patient = Patient.objects.get(user=request.user)

            # Update Patient Data
            patient.age = request.POST.get("age") or patient.age
            patient.gender = request.POST.get("gender") or patient.gender
            patient.phone = request.POST.get("phone") or patient.phone
            patient.address = request.POST.get("address") or patient.address

            # Update User Name
            new_name = request.POST.get("name")
            if new_name:
                request.user.first_name = new_name
                request.user.save()

            # Photo upload check
            if "profile_photo" in request.FILES:
                patient.profile_photo = request.FILES["profile_photo"]

            patient.save()

            return JsonResponse({"message": "Profile updated successfully"}, status=200)

        except Patient.DoesNotExist:
            return JsonResponse({"message": "Patient profile not found."}, status=404)

        except Exception as e:
            return JsonResponse({"message": f"Server error: {str(e)}"}, status=500)

    return JsonResponse({"message": "Invalid method"}, status=405)
