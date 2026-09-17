# Risk Register

Scoring method:

**Risk Score = Likelihood × Impact**

Both likelihood and impact use a 1–5 scale.

| ID | Threat | Likelihood | Impact | Score | Rationale |
|---|---|---:|---:|---:|---|
| R01 | Broken access control | 4 | 5 | 20 | Could expose or modify another user's data |
| R02 | Credential attacks | 4 | 4 | 16 | Could result in account takeover |
| R03 | SQL injection | 3 | 5 | 15 | Could expose or modify database records |
| R04 | Information disclosure | 3 | 5 | 15 | Student information may be sensitive |
| R05 | Session compromise | 3 | 4 | 12 | Could enable user impersonation |
| R06 | Malicious file upload | 3 | 4 | 12 | Unsafe files may affect application or users |
| R07 | Denial of service | 3 | 3 | 9 | Could affect availability |
| R08 | Insufficient logging | 3 | 3 | 9 | Makes incident investigation harder |

## Priority approach

Higher-scoring risks should be addressed first, with controls proportionate to the application's exposure and impact.
