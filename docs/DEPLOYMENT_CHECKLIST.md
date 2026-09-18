# Deployment checklist — SYNERGY RiskGuard

- [ ] Pin commit/image and rerun tests.
- [ ] Customer TLS ingress + OIDC/mTLS/JWKS.
- [ ] Least-privilege roles and KMS/secret manager.
- [ ] Restricted PostgreSQL/ClickHouse/venue networks.
- [ ] Backup/restore and audit-correlation test.
- [ ] Exercise `/enterprise/v1/risk/check` with representative payload.
- [ ] Prove roles **trader, risk** and viewer denial.
- [ ] Monitor metrics and drill timeout/429/5xx/DB outage/restart.
- [ ] Keep live execution disabled through evaluation.
- [ ] Trading + Risk + Ops + Security/Compliance approve any live canary.