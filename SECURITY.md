# Security policy — SYNERGY RiskGuard v2.0.0

- No production secrets in Git.
- Live execution disabled by default; customer approval remains mandatory.
- Prefer customer OIDC/mTLS/JWKS over the included HS256 evaluation boundary.
- Use least-privilege venue credentials; disable withdrawals where supported.
- Request IDs are correlation evidence, not authentication/idempotency secrets.
- Unknown financial side effects must not be blindly retried.
- Risk veto remains outside mutable strategy/agent logic.

PostgreSQL is the reference authoritative audit store; ClickHouse is an analytical mirror. Define encryption, retention, backup/restore and access policy before production.

No SOC 2, ISO 27001 or regulatory certification is claimed. Use private vulnerability reporting for sensitive disclosures.