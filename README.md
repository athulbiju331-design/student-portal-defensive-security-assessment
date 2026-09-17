# Student Portal Web Application — Threat Model & Secure Configuration

## Overview

This is a small fictional Student Portal built with Python and Flask for a defensive cybersecurity learning project.

The application demonstrates common web application components that can be threat-modelled:

- Student registration and authentication
- Student dashboard
- Assignment upload
- Administrator dashboard
- SQLite database
- File storage
- Security logging

## Security controls implemented

The application includes educational examples of:

- Password hashing with Werkzeug
- Parameterized SQL queries
- Role-based access control
- Server-side authorization checks
- CSRF tokens
- Login rate limiting
- Secure session cookie attributes
- Upload filename sanitization
- File extension allow-list
- Upload size limit
- Security HTTP headers
- Security event logging
- Least-privilege style access checks

## Demo accounts

Student:
- Username: `student`
- Password: `StudentDemo123!`

Administrator:
- Username: `admin`
- Password: `AdminDemo123!`

These credentials are for the local demonstration only. Do not reuse them in a real system.

## Run locally

```bash
python -m pip install -r requirements.txt
python app.py
```

Open:

`http://127.0.0.1:5000`

## Project scope

This application is intentionally small and is intended for local defensive learning. No external systems should be scanned or tested.

## Threat-model deliverables

The repository should also contain:

- `docs/threat-model.md`
- `docs/risk-register.md`
- `docs/hardening-checklist.md`
- `diagrams/threat-model.drawio`
- `evidence/verification-notes.md`
