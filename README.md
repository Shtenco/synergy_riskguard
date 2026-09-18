# SYNERGY RiskGuard

> **Independent pre-trade and portfolio risk control with VaR/CVaR, drawdown veto and kill-switch**

Version: `2.0.0`

**Enterprise v2.0.0** · Python 3.11+ · FastAPI/OpenAPI · Docker/Compose · PostgreSQL/ClickHouse audit · RBAC/JWT · CI/tests

**Designed for:** Prop firms, brokers, quant funds, family offices and trading desks  
**Primary endpoint:** `POST /enterprise/v1/risk/check`  
**Commercial mode:** paid technical pilot · source-code licensing · OEM/white-label integration

> [!IMPORTANT]
> Trading/research infrastructure only. No promise of investment return, profitable execution or regulatory approval. Production requires customer OOS/paper/canary evidence and Security/Risk/Ops/Compliance sign-off.

## Fund-facing capabilities
- deterministic product core separated from enterprise controls;
- tenant RBAC, request-ID audit, PostgreSQL + ClickHouse;
- health/Prometheus metrics and bounded retry/circuit-breaker;
- Bybit V5, CCXT and MT5 integration contracts; live execution off by default;
- Docker/Compose, synthetic demo data, load harnesses and due-diligence documentation.

## Verification snapshot
| Evidence | Snapshot |
|---|---:|
| tests | **21 passed** |
| health smoke | **80/80 HTTP 200** |
| p50 / p95 / p99 | **15.4 / 69 / 82.8 ms** |
| local throughput | **539 req/s** |

Local health smoke only; not a production SLA or market/execution benchmark.

## Quick evaluation
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev,enterprise]'
pytest -q
python -m synergy_riskguard.api
```
Open `http://127.0.0.1:8000/docs`.

## CTO package
[Due diligence](docs/CTO_DUE_DILIGENCE.md) · [Architecture](docs/ARCHITECTURE_DIAGRAMS.md) · [API](docs/API_EXAMPLES.md) · [Security](SECURITY.md) · [Benchmarks](docs/BENCHMARKS_AND_ACCEPTANCE.md) · [SLA/SLO](docs/SLA_SLO.md) · [Deployment](docs/DEPLOYMENT_CHECKLIST.md) · [Pilot](docs/CUSTOMER_PILOT.md)
