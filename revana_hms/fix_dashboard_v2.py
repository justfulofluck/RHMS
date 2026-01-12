
path = '/home/bhavan/Desktop/RHMS/revana_hms/doctors/templates/doctors/dashboard.html'

with open(path, 'r') as f:
    content = f.read()

# The incorrect multiline pattern (as seen in view_file)
target = """                                            <button class="btn btn-warning btn-sm text-white fw-bold px-3"
                                                onclick="loadPatientHistory('{{ appt.patient_name }}')" {% if not
                                                appt.has_history %}disabled style="opacity: 0.5; cursor: not-allowed;"
                                                title="First time visitor - No history" {% endif %}>
                                                History
                                            </button>"""

# Robust Replacement using explicit IF/ELSE blocks
replacement = """                                            {% if appt.has_history %}
                                            <button class="btn btn-warning btn-sm text-white fw-bold px-3" onclick="loadPatientHistory('{{ appt.patient_name }}')">
                                                History
                                            </button>
                                            {% else %}
                                            <button class="btn btn-warning btn-sm text-white fw-bold px-3" disabled style="opacity: 0.5; cursor: not-allowed;" title="No History">
                                                History
                                            </button>
                                            {% endif %}"""

if target in content:
    new_content = content.replace(target, replacement)
    with open(path, 'w') as f:
        f.write(new_content)
    print("Fixed successfully with Robust IF/ELSE.")
else:
    print("Target string not found. Trying flexible normalization...")
    # Try normalizing spaces to find it
    import re
    # Escape special regex chars in target, then replace duplicate spaces with \s+
    target_regex = re.escape(target).replace(r'\ ', r'\s+')
    
    # We might need a simpler approach if exact match fails: find the specific block range
    print("Debugging: Could not match exact string.")
    
    # Fallback: Let's dump the file to see why
    lines = content.splitlines()
    for i in range(220, 230):
        if i < len(lines):
             print(f"{i+1}: {repr(lines[i])}")
