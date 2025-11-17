import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, authenticate, login
from .models import Patient
from django.shortcuts import render

User = get_user_model()

from django.contrib.auth.decorators import login_required

def patient_dashboard(request):
    return render(request, 'patients/patient_dashboard.html')

    

# ✅ Render registration page
def patient_register_page(request):
    return render(request, "patients/register.html")

# ✅ Handle patient registration (unchanged)
@csrf_exempt  # ⚠️ For production, use CSRF token properly
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

            # Create Patient profile
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

# ✅ Render login page
def login_page(request):
    return render(request, "patients/login.html")

# ✅ Handle login request
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
            else:
                return JsonResponse({"message": "Invalid email or password"}, status=401)

        except Exception as e:
            return JsonResponse({"message": f"Server error: {str(e)}"}, status=000000000000)

    return JsonResponse({"message": "Only POST method allowed."}, status=405)
