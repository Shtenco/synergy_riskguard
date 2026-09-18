# Benchmarks and acceptance — SYNERGY RiskGuard

Fresh verification: **21 tests passed**. RBAC tests cover permitted roles and viewer denial; product actions are tested for request-ID/audit linkage.

Local `/enterprise/health` smoke: **80/80 HTTP 200**, p50 **15.4 ms**, p95 **69 ms**, p99 **82.8 ms**, ~**539 req/s** at 80 requests / concurrency 16.

These are local health-endpoint smoke figures only — not production SLA, product-endpoint latency, venue latency, execution quality or profitability.

Customer gates: reproduce tests; map IdP/RBAC; trace audit; target-hardware load test; freeze acceptance data/criteria; sandbox/paper before live canary; run timeout/429/5xx/DB outage/restart/rollback drills.