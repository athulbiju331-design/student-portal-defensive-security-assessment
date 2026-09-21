# Security Findings

## Finding F-01 — Debug Mode Enabled

**Severity:** Medium

**Category:** Security Misconfiguration

### Evidence

The original application configuration used:

```python
app.run(debug=True)