# Architecture diagrams — SYNERGY RiskGuard

```mermaid
flowchart LR
 A[Fund client] --> B[OIDC/mTLS gateway]
 B --> C[JWT + tenant RBAC]
 C --> D[Risk Decision Core]
 D --> E[Decision artifact]
 E --> F[AuditEvent + X-Request-ID]
 F --> G[(PostgreSQL)]
 F --> H[(ClickHouse)]
 E --> I{Execution boundary}
```

Primary action: `POST /enterprise/v1/risk/check`. Authentication failures deny. Live execution remains separately gated. Retry/circuit-breaker logic is bounded and never blindly replays unknown financial side effects.