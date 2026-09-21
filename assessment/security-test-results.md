# Security Test Results

## 1. Configuration Security

### Debug Mode

- Before: `app.run(debug=True)`
- Result: Debug mode was enabled.
- Risk: Detailed error information could be exposed.
- Remediation: Changed to `app.run(debug=False)`.
- Retest: Application started successfully with debug mode disabled.
- Status: PASS after remediation.

### Session Cookie Configuration

- `HttpOnly`: Enabled.
- `SameSite`: `Lax`.
- `Secure`: Disabled for the local HTTP training environment.
- Production recommendation: Use HTTPS and enable `Secure=True`.
- Status: PASS for the local assessment scope.

### Security Headers

The application implements:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy`
- `Content-Security-Policy`

- Status: PASS.

## 2. Authentication Security

### Invalid Login

- Test: Submitted invalid credentials.
- Observed: `Invalid username or password.`
- Result: Generic authentication error.
- Status: PASS.

### Login Rate Limiting

- Test: Repeated failed login attempts.
- Observed: `Too many login attempts. Please wait one minute.`
- Result: Repeated attempts are rate limited.
- Status: PASS.

### Password Hashing

- Implementation: Werkzeug password hashing.
- Password verification uses `check_password_hash()`.
- Plain-text passwords are not used for password verification.
- Status: PASS.

## 3. Input Validation

### File Upload

- Test: Attempted upload of a `.exe` file.
- Observed: `Allowed file types: PDF, DOC, DOCX, TXT.`
- Result: Disallowed file type was rejected.
- Status: PASS.

### File Size

- Maximum request size: 5 MB.
- Status: PASS.

### CSRF Protection

- POST forms use server-side CSRF token validation.
- Invalid or missing tokens are rejected.
- Status: PASS.

## 4. Authorization

### Role-Based Access Control

- Student users are restricted from administrator functionality.
- Administrative routes require the admin role.
- Status: PASS.

### File Access Control

- Uploaded files are checked against the authenticated user's ID.
- Administrators can access authorized administrative content.
- Unauthorized users receive a forbidden response.
- Status: PASS.

## 5. Database Security

- SQL queries use parameterized placeholders.
- User input is not directly concatenated into SQL statements.
- Status: PASS.

## 6. Security Logging

The application records security-relevant events including:

- Successful login
- Failed login
- Rate-limit events
- Logout
- Registration
- Blocked file uploads

Passwords and authentication tokens are not intentionally written to the security log.

- Status: PASS.

## 7. Dependency Security

- Dependencies are defined in `requirements.txt`.
- Dependency security was checked using `pip-audit`.
- Result: No known vulnerabilities found.
- Status: PASS.

## Overall Result

The Student Portal contains multiple defensive security controls.

The assessment identified a debug-mode configuration issue, which was remediated by changing `app.run(debug=True)` to `app.run(debug=False)`.

Authentication, input validation, authorization, database security, security logging, security headers, and dependency security were reviewed and verified.

The dependency review using `pip-audit` reported no known vulnerabilities.

The application remained functional after the security remediation.