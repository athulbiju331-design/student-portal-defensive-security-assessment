# Prioritized Hardening Checklist

## Priority 1 — Critical

- [ ] Hash passwords using a secure password-hashing algorithm.
- [ ] Use parameterized SQL queries.
- [ ] Enforce authorization on the server side.
- [ ] Separate student and administrator roles.
- [ ] Implement CSRF protection for state-changing requests.

## Priority 2 — High

- [ ] Apply login rate limiting.
- [ ] Restrict file-upload extensions.
- [ ] Enforce a maximum upload size.
- [ ] Sanitize uploaded filenames.
- [ ] Restrict access to uploaded files by ownership/authorization.
- [ ] Use HttpOnly and SameSite session cookies.

## Priority 3 — Medium

- [ ] Configure security-related HTTP headers.
- [ ] Log important security events.
- [ ] Use HTTPS in production.
- [ ] Store the production SECRET_KEY securely in environment variables.
- [ ] Centralize security logs for monitoring.
- [ ] Use automated dependency scanning.

## Verification

- [ ] Test student login.
- [ ] Test invalid login handling.
- [ ] Test login rate limiting.
- [ ] Test student/admin role separation.
- [ ] Test unauthorized file access.
- [ ] Test invalid file-upload types.
- [ ] Test CSRF protection.
- [ ] Check security response headers.