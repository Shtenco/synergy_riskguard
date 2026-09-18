# Reference SLA / SLO — SYNERGY RiskGuard

Contract starting point, not warranty.

| SLI | Reference target |
|---|---:|
| API availability | 99.9% monthly |
| health p95 | <250 ms on accepted customer environment |
| server 5xx | <0.1% |
| audit correlation | 100% accepted privileged product actions |
| RTO | 30 min reference |
| audit RPO | 5 min reference |

No universal latency promise for `/enterprise/v1/risk/check`. Venue fills, spread, market impact and external availability are separate from service SLOs.