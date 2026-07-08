# 🔒 Privacy-First AI GRC Audit Agent

## Overview

Privacy-First AI GRC Audit Agent is an AI-powered compliance auditing tool that analyzes organizational security policies against major cybersecurity frameworks.

The application runs locally using Ollama, ensuring sensitive policy documents never leave the user's system.

## Features

- Upload PDF security policies
- AI-powered compliance analysis
- Executive Summary
- Risk Score Gauge
- Compliance Overview Chart
- Framework Compliance Table
- Compliance Gap Detection
- Remediation Recommendations
- HTML Report Generation
- Downloadable Reports
- Privacy-first local processing

## Technologies

- Python
- Streamlit
- Ollama
- Plotly
- PyPDF
- JSON

## Supported Frameworks

- ISO 27001
- NIS2
- NIST CSF
- GDPR

## Project Structure

privacy-first-grc-agent/
│
├── streamlit_app.py
├── app.py
├── audit_engine.py
├── report_generator.py
├── reports/
├── screenshots/
└── README.md

## How to Run

1. Install dependencies

pip install -r requirements.txt

2. Start Ollama

ollama serve

3. Run the application

streamlit run streamlit_app.py

## Author

Aditi Bhavar
BSc Cyber Security