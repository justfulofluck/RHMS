
path = '/home/bhavan/Desktop/RHMS/revana_hms/doctors/templates/doctors/dashboard.html'

with open(path, 'r') as f:
    content = f.read()

# The incorrect multiline pattern
target = """                                            <button class="btn btn-warning btn-sm text-white fw-bold px-3"
                                                onclick="loadPatientHistory('{{ appt.patient_name }}')" {% if not
                                                appt.has_history %}disabled style="opacity: 0.5; cursor: not-allowed;"
                                                title="First time visitor - No history" {% endif %}>
                                                History
                                            </button>"""

# The correct single-line pattern
replacement = """                                            <button class="btn btn-warning btn-sm text-white fw-bold px-3"
                                                onclick="loadPatientHistory('{{ appt.patient_name }}')" {% if not appt.has_history %}disabled style="opacity: 0.5; cursor: not-allowed;" title="First time visitor - No history"{% endif %}>
                                                History
                                            </button>"""

if target in content:
    new_content = content.replace(target, replacement)
    with open(path, 'w') as f:
        f.write(new_content)
    print("Fixed successfully.")
else:
    print("Target string not found. Printing dump around line 220:")
    lines = content.splitlines()
    for i in range(218, 228):
        if i < len(lines):
            print(f"{i+1}: {lines[i]}")
