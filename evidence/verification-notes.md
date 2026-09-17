# Verification Notes

This file records defensive verification performed only against the local Student Portal.

## Test 1 — Student login

Expected result: valid demo student credentials create an authenticated session.

## Test 2 — Invalid login

Expected result: invalid credentials are rejected and a security event is logged.

## Test 3 — Login rate limiting

Expected result: repeated failed attempts for the same username are throttled after the configured threshold.

## Test 4 — Role separation

Expected result: a student attempting to open `/admin` receives HTTP 403.

## Test 5 — Assignment access control

Expected result: a student can access their own uploaded assignment but cannot access another student's assignment.

## Test 6 — File upload validation

Expected result: unsupported extensions are rejected.

## Test 7 — CSRF protection

Expected result: state-changing POST requests without a valid CSRF token are rejected.

## Test 8 — Security headers

Expected result: responses include security headers such as X-Content-Type-Options and X-Frame-Options.

No external systems are included in the test scope.
