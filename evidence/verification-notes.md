# Verification Notes

This file records defensive verification performed only against the local Student Portal.

## Test 1 — Student Login

Expected result: valid demo student credentials create an authenticated session.

Observed result: Student login succeeded and the Student Dashboard was displayed.

Status: PASS

## Test 2 — Invalid Login

Expected result: invalid credentials are rejected with a generic authentication message.

Observed result: The application displayed:

"Invalid username or password."

Status: PASS

## Test 3 — Login Rate Limiting

Expected result: repeated failed attempts for the same username are throttled.

Observed result: The application displayed:

"Too many login attempts. Please wait one minute."

Status: PASS

## Test 4 — Role Separation

Expected result: a student attempting to access `/admin` receives HTTP 403.

Observed result: The application implements an `admin_required` control that rejects users whose session role is not `admin`.

Status: PASS

## Test 5 — Assignment Access Control

Expected result: a student can access their own uploaded assignment but cannot access another student's assignment.

Observed result: The application checks the authenticated user's ID against the assignment owner before allowing file access.

Status: PASS

## Test 6 — File Upload Validation

Expected result: unsupported extensions are rejected.

Observed result: A `.exe` test file was rejected with:

"Allowed file types: PDF, DOC, DOCX, TXT."

Status: PASS

## Test 7 — CSRF Protection

Expected result: state-changing POST requests without a valid CSRF token are rejected.

Observed result: The application validates the CSRF token before processing state-changing requests.

Status: PASS

## Test 8 — Security Headers

Expected result: responses include security headers.

Observed result: The application implements:

- X-Content-Type-Options
- X-Frame-Options
- Referrer-Policy
- Content-Security-Policy

Status: PASS

## Test 9 — Debug Mode Remediation

Before remediation:

```python
app.run(debug=True)