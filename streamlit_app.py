from datetime import datetime
import streamlit as st
import json
import subprocess
from pypdf import PdfReader
from audit_engine import audit_policy
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Privacy-First AI GRC Audit",
    page_icon="🔒",
    layout="wide"
)

st.title("🔒 Privacy-First AI GRC Audit Agent")

st.write("""
Upload a PDF security policy and perform a local compliance audit
against ISO 27001, NIS2, NIST CSF and GDPR.
""")

uploaded_file = st.file_uploader(
    "Upload Policy PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    with open("policy.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ PDF uploaded successfully.")

    if st.button("🚀 Run Audit"):

        with st.spinner("Reading PDF..."):

            reader = PdfReader("policy.pdf")

            policy_text = ""

            for page in reader.pages:

                text = page.extract_text()

                if text:

                    policy_text += text + "\n"

        st.success("✅ PDF processed successfully.")
        with st.spinner("Running GRC Audit..."):

            audit_result = audit_policy(policy_text)

        import os
        
        os.makedirs("reports", exist_ok=True)
        
        with open("reports/audit_report.json", "w", encoding="utf-8") as f:
            json.dump(audit_result, f, indent=4)
            
        import sys

        subprocess.run(
           [sys.executable, "report_generator.py"],
           check=True
        )            
        
        st.success("✅ Audit Completed Successfully!")
        st.caption(
             f"🕒 Audit Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}"
        )
        st.subheader("📝 Executive Summary")
        import json

        with open("reports/audit_report.json", "r", encoding="utf-8") as f:
           report = json.load(f)

           st.info(report["summary"])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Compliance",
                audit_result["compliant_status"]
            )

        with col2:
            st.metric(
                "Risk Score",
                audit_result["risk_score"]
            )

        with col3:
            st.metric(
                "Risk Level",
                audit_result["risk_level"]
            )

        # -------------------------
        # Risk Score Gauge
        # -------------------------

        st.subheader("🎯 Risk Score Gauge")

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=audit_result["risk_score"],
                title={"text": "Risk Score"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "darkred"},
                    "steps": [
                        {"range": [0, 20], "color": "green"},
                        {"range": [20, 50], "color": "orange"},
                        {"range": [50, 100], "color": "red"}
                    ]
                }
            )
        )

        st.plotly_chart(fig, use_container_width=True)
        # -------------------------
        # Compliance Chart
        # -------------------------

        st.subheader("📊 Compliance Overview")

        total_controls = 21
        missing_controls = len(audit_result["gaps_found"])
        implemented_controls = total_controls - missing_controls

        chart_data = {
            "Status": ["Implemented", "Missing"],
            "Controls": [implemented_controls, missing_controls]
        }

        fig = px.pie(
            chart_data,
            names="Status",
            values="Controls",
            title="Compliance Controls"
        )

        st.plotly_chart(fig, use_container_width=True)

        # -------------------------
        # Framework Compliance
        # -------------------------

        st.subheader("📋 Framework Compliance")

        framework_data = []

        all_frameworks = ["ISO 27001", "NIS2", "NIST CSF", "GDPR"]

        for fw in all_frameworks:
            if fw in " ".join(audit_result["frameworks"]):
                framework_data.append({
                    "Framework": fw,
                    "Status": "✅ Covered"
                })
            else:
                framework_data.append({
                    "Framework": fw,
                    "Status": "❌ Not Covered"
                })

        st.table(framework_data)

        # -------------------------
        # Compliance Gaps
        # -------------------------        

        st.subheader("⚠️ Compliance Gaps")

        if audit_result["gaps_found"]:
            for gap in audit_result["gaps_found"]:
                st.error(gap)
        else:
            st.success("No compliance gaps found.")

        # -------------------------
        # Remediation
        # -------------------------

        st.subheader("🛠 Remediation Steps")

        if audit_result["remediation_steps"]:
            for step in audit_result["remediation_steps"]:
                st.info(step)
        else:
            st.success("No remediation required.")

        # -------------------------
        # Reports
        # -------------------------

        st.subheader("📄 Reports")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🌐 Open HTML Report"):
                import webbrowser
                import os

                report_path = os.path.abspath("reports/audit_report.html")
                webbrowser.open(f"file://{report_path}")

        with col2:
            with open("reports/audit_report.html", "rb") as file:
                st.download_button(
                    label="⬇️ Download HTML Report",
                    data=file,
                    file_name="audit_report.html",
                    mime="text/html"
                )

        st.success("🎉 Privacy-First GRC Audit Completed Successfully!")