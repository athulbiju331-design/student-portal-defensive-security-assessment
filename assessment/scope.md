# Security Assessment Scope

## Application

Student Portal - Defensive Security Assessment

## Assessment Type

Authorized defensive security assessment.

## Target

The assessment target is the Student Portal application running locally on:

http://127.0.0.1:5000

## Authorization

The application is owned and controlled by the project author. Testing is performed only against this local application as part of the EdVyro Cyber Security Task 5 assessment.

## Scope

The assessment covers:

- Application configuration
- Authentication
- Session security
- Input validation
- File upload validation
- Authorization and access control
- Dependency security
- Security logging
- Security headers

## Out of Scope

The following are outside the assessment scope:

- Public websites
- Third-party systems
- External IP addresses
- Real user accounts
- Real personal data
- Denial-of-service testing
- Destructive testing

## Rules of Engagement

- Perform testing only against the local application.
- Use only test accounts and synthetic data.
- Do not access systems outside the defined scope.
- Do not use destructive payloads.
- Do not publish passwords, secrets, tokens, or personal information.
- Record evidence for each security test.
- Retest security controls after remediation.

## Assessment Objective

Identify security weaknesses, document the findings, fix the highest-priority issues, and verify the improvements through retesting.