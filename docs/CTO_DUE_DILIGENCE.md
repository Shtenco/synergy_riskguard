# CTO due diligence — SYNERGY RiskGuard v2.0.0

**Use case:** Independent pre-trade and portfolio risk control with VaR/CVaR, drawdown veto and kill-switch.  
**Buyer:** Prop firms, brokers, quant funds, family offices and trading desks.  
**Endpoint:** `POST /enterprise/v1/risk/check` · roles **trader, risk**.  
**Status:** paid-pilot / enterprise-deployment candidate; not customer-certified production infrastructure.

Implemented: installable Python/FastAPI, deterministic core, tenant RBAC, request-ID audit, PostgreSQL/ClickHouse, health/metrics, retry/circuit breaker, Bybit/CCXT/MT5 integration contracts with live off by default.

Evidence: **21 tests passed**; local health smoke 80/80 200, p95 **69 ms**.

Boundaries: no independent certification, no universal latency claim, no guaranteed fills/alpha/profitability; customer integration and approvals remain required.