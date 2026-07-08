import subprocess
print("RUNNING THE CORRECT APP.PY")

import requests
import json
import traceback
from pypdf import PdfReader
from audit_engine import audit_policy

# ==============================
# CONFIG
# ==============================
MODEL_NAME = "phi"      # Change to "phi" later if you want

API_URL = "http://localhost:11434/api/generate"

# ==============================
# COMPLIANCE LAWS
# ==============================
mock_laws = """
NIS2 Article 21(2)(j): Requires encryption and multi-factor authentication.

ISO 27001:2022 A.5.15: Access control policies must be documented.

ISO 27001:2022 A.5.17: Authentication information must be securely managed.

ISO 27001:2022 A.8.24: Use cryptography to protect sensitive information.

ISO 27001:2022 A.5.23: Information security requirements for cloud services.

ISO 27001:2022 A.8.15: Logging and monitoring must be enabled.

ISO 27001:2022 A.5.7: Threat intelligence should be collected.

NIST CSF PR.AA: Identity and Access Management.

NIST CSF PR.DS: Data Security.

NIST CSF DE.CM: Continuous Security Monitoring.

GDPR Article 32: Personal data must be protected using appropriate technical and organizational measures.
"""

# ==============================
# LOAD PDF
# ==============================
pdf_path = input("\nEnter PDF file path: ")

reader = PdfReader(pdf_path)

mock_policy = ""

for page in reader.pages:
    text = page.extract_text()
    if text:
        mock_policy += text + "\n"

print("\nPDF loaded successfully!")
print("Characters in PDF:", len(mock_policy))
print(mock_policy)

audit_result = audit_policy(mock_policy)

audit_result["summary"] = (
    f"The policy was analyzed against ISO 27001, NIS2, NIST CSF and GDPR. "
    f"Compliance Status: {audit_result['compliant_status']}. "
    f"Risk Level: {audit_result['risk_level']}."
)

print("\n=== PYTHON AUDIT ===")
print(json.dumps(audit_result, indent=4))

with open("reports/audit_report.json", "w") as f:
    json.dump(audit_result, f, indent=4)

print("\n✅ Audit report saved to reports/audit_report.json")
# ==============================
# PROMPT
# ==============================
prompt_content = f"""
You are a cybersecurity auditor.

Compliance Laws:
{mock_laws}

Internal Policy:
{mock_policy}

Analyze the policy and return ONLY this JSON.
Analyze the policy carefully.

For each framework:
- Identify whether the policy contains relevant controls.
- Include every applicable framework in the "frameworks" array.
- List all missing security controls in "gaps_found".
- Provide practical remediation steps in "remediation_steps".
- Generate a professional executive summary.
- Return ONLY valid JSON. Do not include markdown or explanations.

{{
"compliant_status":"Compliant or Non-Compliant",
"risk_score":number,
"risk_level":"Low, Medium or High",
"frameworks":["frameworks":[
    "List ONLY the compliance frameworks that apply based on the uploaded policy. Choose from: ISO 27001, NIS2, NIST CSF, GDPR."
],
"gaps_found":["gap1","gap2"],
"remediation_steps":["step1","step2"],
"summary":"short summary"
}}
"""
# ==============================
# PAYLOAD
# ==============================
payload = {
    "model": MODEL_NAME,
    "prompt": prompt_content,
    "stream": False,
    "options": {
        "temperature": 0
    }
}

print("\n[+] Starting GRC Audit...")
print("[i] Model:", MODEL_NAME)

# ==============================
# API CALL
# ==============================
try:

    response = requests.post(
        API_URL,
        json=payload,
        timeout=300
    )

    response.raise_for_status()

    data = response.json()

    output = data.get("response", "").strip()

    print("\n=== RAW OUTPUT ===")
    print(output)

    try:
        parsed = json.loads(output)
        with open("reports/audit_report.json", "w", encoding="utf-8") as f:
         json.dump(parsed, f, indent=4)

        print("\n=== PARSED RESULT ===")
        print(json.dumps(parsed, indent=4))

    except json.JSONDecodeError:
        print("\nOutput is not valid JSON.")

except requests.exceptions.Timeout:
    print("\nERROR: Request timed out.")

except requests.exceptions.ConnectionError:
    print("\nERROR: Cannot connect to Ollama. Run: ollama serve")

except Exception as e:
    print("\nERROR:", e)
    traceback.print_exc()

# ==============================
# GENERATE HTML REPORT
# ==============================

print("\nGenerating Professional HTML Report...")

subprocess.run(["python", "report_generator.py"])

print("Professional HTML Report Generated!")