# Threat Model

## 1. Application

Student Portal is a small web application where students can authenticate, view their dashboard and submit assignments. Administrators can manage users and review submissions.

## 2. Assets

- User accounts
- Password hashes
- Authentication sessions
- Student information
- Assignment files
- Database records
- Administrator functions
- Application/security logs

## 3. Actors

### Student
Normal authenticated user.

### Administrator
Privileged user with access to administrative functions.

### External attacker
Untrusted Internet actor who may attempt authentication attacks, unauthorized access, malicious input or resource abuse.

## 4. Trust boundaries

1. Internet/user to web application
2. Web application to database
3. Web application to file storage
4. Web application to external services in a real deployment

## 5. Data flows

Student/Admin -> HTTPS -> Web Application
Web Application -> Database
Web Application -> File Storage
Web Application -> Security Logs

## 6. STRIDE threats

| Category | Example threat | Asset |
|---|---|---|
| Spoofing | Credential attack/account takeover | User account |
| Tampering | Unauthorized assignment modification | Assignment |
| Repudiation | User denies performing an action | Audit trail |
| Information Disclosure | Unauthorized profile access | Student data |
| Denial of Service | Excessive login/request traffic | Application availability |
| Elevation of Privilege | Student accesses admin functionality | Admin functions |

## 7. Defensive controls

- Password hashing
- CSRF protection
- Rate limiting
- Role-based access control
- Object-level authorization
- Parameterized SQL
- Upload validation
- Secure session settings
- Security headers
- Security logging

All testing should remain within the local authorized environment.
