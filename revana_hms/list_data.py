from hospitals.models import Department, Treatment

def list_data():
    departments = Department.objects.values_list('name', flat=True).distinct().order_by('name')
    treatments = Treatment.objects.values_list('name', flat=True).distinct().order_by('name')

    print("\n--- Current Categories (Departments) ---")
    if departments:
        for d in departments:
            print(f"- {d}")
    else:
        print("No departments found.")

    print("\n--- Current Treatments ---")
    if treatments:
        for t in treatments:
            print(f"- {t}")
    else:
        print("No treatments found.")

list_data()
