import json

def audit_policy(policy_text):

    controls = {
        "Encryption": {
            "keywords": ["encrypt", "encryption", "cryptography"],
            "severity": 20
        },
        "Multi-Factor Authentication": {
            "keywords": ["multi-factor", "mfa"],
            "severity": 20
        },
        "Password Policy": {
            "keywords": ["password"],
            "severity": 10
        },
        "Access Control": {
            "keywords": ["access control"],
            "severity": 15
        },
        "Least Privilege": {
            "keywords": ["least privilege"],
            "severity": 15
        },
        "Logging": {
            "keywords": ["log", "logging"],
            "severity": 10
        },
        "Monitoring": {
            "keywords": ["monitor", "monitoring"],
            "severity": 10
        },
        "Backup": {
            "keywords": ["backup"],
            "severity": 15
        },
        "Incident Response": {
            "keywords": ["incident"],
            "severity": 15
        },
        "Patch Management": {
            "keywords": ["patch"],
            "severity": 10
        },
        "Vulnerability Management": {
            "keywords": ["vulnerability"],
            "severity": 15
        },
        "Asset Inventory": {
            "keywords": ["asset"],
            "severity": 5
        },
        "Cloud Security": {
            "keywords": ["cloud"],
            "severity": 10
        },
        "Data Classification": {
            "keywords": ["classification"],
            "severity": 5
        },
        "Data Retention": {
            "keywords": ["retention"],
            "severity": 5
        },
        "Business Continuity": {
            "keywords": ["business continuity"],
            "severity": 10
        },
        "Disaster Recovery": {
            "keywords": ["disaster recovery"],
            "severity": 10
        },
        "Vendor Risk": {
            "keywords": ["vendor"],
            "severity": 10
        },
        "Threat Intelligence": {
            "keywords": ["threat"],
            "severity": 10
        },
        "Security Awareness": {
            "keywords": ["training", "awareness"],
            "severity": 5
        },
        "Network Security": {
            "keywords": ["firewall", "network"],
            "severity": 10
        }
    }

    frameworks = [
        "ISO 27001",
        "NIS2",
        "NIST CSF",
        "GDPR"
    ]

    gaps_found = []
    remediation_steps = []

    risk_score = 0

    policy_lower = policy_text.lower()

    for control, info in controls.items():

        found = False

        for keyword in info["keywords"]:
            if keyword in policy_lower:
                found = True
                break

        if not found:
            gaps_found.append(f"{control} is missing.")
            remediation_steps.append(f"Implement {control}.")
            risk_score += info["severity"]

    risk_score = min(risk_score, 100)

    if risk_score <= 20:
        compliant_status = "Compliant"
        risk_level = "Low"

    elif risk_score <= 50:
        compliant_status = "Partially Compliant"
        risk_level = "Medium"

    else:
        compliant_status = "Non-Compliant"
        risk_level = "High"

    return {
        "compliant_status": compliant_status,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "frameworks": frameworks,
        "gaps_found": gaps_found,
        "remediation_steps": remediation_steps
    }