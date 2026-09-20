# RiskGuard V3 Production Hardening Design

**Version:** 3.0.0  
**Branch:** `production/v3.0.0`  
**Status:** design approved for implementation planning

## Goal

Turn RiskGuard into an independent, authoritative pre-trade risk service where policies and kill-switch state are server-controlled, persistent, tenant/account scoped, auditable, and impossible for a trader request to override.

## Current-state findings

The current `POST /enterprise/v1/risk/check` request contains:
- account state;
- order intent;
- risk limits;
- `kill_switch`.

The endpoint constructs `Limits` and `AccountState` directly from caller JSON. Therefore the current caller can choose its own risk limits and kill-switch value. This is acceptable for a demo/pilot API but violates the independent-risk-control goal.

PostgreSQL DDL currently includes audit and idempotency tables, but no runtime policy registry, authoritative account-state snapshot store or persistent kill switch.

## V3 invariants

1. Trader requests cannot define or weaken authoritative risk limits.
2. Trader requests cannot clear a kill switch.
3. Every decision references exactly one active server-side policy version.
4. Every decision is tied to a fresh account-state snapshot.
5. Stale or missing authoritative state fails closed.
6. Policy and kill-switch mutations require RISK or ADMIN authority.
7. Decisions are immutable and tenant/account isolated.
8. V3 decision creation is idempotent.
9. Production auth/readiness follow the common V3 enterprise contract.

## Architecture

```text
order intent
  -> AuthVerifier / tenant RBAC
  -> IdempotencyStore
  -> AccountStateStore -> freshness gate
  -> RiskPolicyStore -> active version
  -> KillSwitchStore
  -> deterministic decide()
  -> RiskDecisionStore
  -> AuditStore
  -> metrics / logs / traces
```

## Authoritative state model

```python
@dataclass(frozen=True)
class AccountStateSnapshot:
    tenant_id: str
    account_id: str
    observed_at: datetime
    equity: float
    start_day_equity: float
    high_watermark: float
    gross_exposure: float
    returns: tuple[float, ...]
    source: str
    version: str
```

The V3 risk-check request references `account_id` and supplies only the order intent. The authoritative state is loaded server-side.

Optional state-ingestion endpoint is separately permissioned and cannot be called by a plain TRADER role.

Freshness is policy-configurable, with a safe default. If state is older than the permitted maximum age, the order is rejected/fails closed.

## Risk policy registry

```python
@dataclass(frozen=True)
class RiskPolicy:
    policy_id: UUID
    tenant_id: str
    account_id: str | None
    version: int
    status: DRAFT | ACTIVE | RETIRED
    max_daily_loss: float
    max_drawdown: float
    max_gross_exposure: float
    max_single_position: float
    var_limit: float
    confidence: float
    state_max_age_seconds: int
    created_by: str
    created_at: datetime
```

Policy lifecycle:
- create draft: RISK/ADMIN;
- activate: RISK/ADMIN;
- only one active policy for a given scope;
- activation is transactional;
- activated policy is immutable;
- change requires a new version;
- previous active policy becomes RETIRED.

Trader role has read-only visibility to the policy metadata needed to understand decisions, not mutation rights.

## Persistent kill switch

```python
@dataclass(frozen=True)
class KillSwitchState:
    tenant_id: str
    account_id: str
    killed: bool
    reason: str
    changed_by: str
    changed_at: datetime
    version: int
```

Rules:
- TRADER cannot mutate;
- RISK/ADMIN can engage;
- clearing requires explicit RISK/ADMIN action;
- every transition is persisted and audited;
- risk check reads current state from the server store;
- if kill-switch store cannot be read, risk check fails closed.

## V3 risk-check request

```json
{
  "account_id": "fund-a-primary",
  "order": {
    "symbol": "EURUSD",
    "notional": 5000,
    "side": "BUY"
  }
}
```

No `limits` and no `kill_switch` field are accepted in V3.

## V3 decision artifact

Each decision stores:
- decision_id;
- tenant_id;
- account_id;
- request_id;
- order intent;
- account-state version/timestamp;
- risk policy ID/version;
- kill-switch version;
- action;
- approved notional;
- reasons;
- created_at;
- code version.

Decision history is append-only.

## V3 API

`POST /enterprise/v3/risk/check`
- roles: TRADER, RISK
- requires Idempotency-Key
- reads authoritative state/policy/kill switch

`POST /enterprise/v3/risk/policies`
- roles: RISK, ADMIN
- creates draft

`POST /enterprise/v3/risk/policies/{policy_id}/activate`
- roles: RISK, ADMIN

`GET /enterprise/v3/risk/policies/active?account_id=...`
- roles: TRADER, RISK, ADMIN

`POST /enterprise/v3/risk/accounts/{account_id}/state`
- roles: RISK, OPERATOR, ADMIN
- authoritative state ingestion

`POST /enterprise/v3/risk/accounts/{account_id}/kill`
- roles: RISK, ADMIN

`POST /enterprise/v3/risk/accounts/{account_id}/unkill`
- roles: RISK, ADMIN

`GET /enterprise/v3/risk/decisions/{decision_id}`
- tenant scoped

V1 stays available for migration but is explicitly non-authoritative.

## Persistence

PostgreSQL authoritative tables:
- risk_policies;
- account_state_snapshots;
- kill_switch_state;
- risk_decisions;
- idempotency_keys;
- audit_events.

All writes that change policy/kill state are transactional with audit persistence where practical.

## Common V3 runtime requirements

RiskGuard adopts the same:
- AuthVerifier interface;
- HS256 dev/test verifier;
- JWKS production verifier;
- `/enterprise/live` and `/enterprise/ready`;
- pooled PostgreSQL access;
- runtime idempotency;
- structured logs;
- Prometheus metrics;
- optional OpenTelemetry.

## Failure semantics

- missing/invalid token: 401;
- role violation: 403;
- missing active policy: fail closed;
- stale/missing account state: fail closed;
- kill switch active: deterministic KILL_SWITCH/REJECT result;
- idempotency mismatch: 409;
- authoritative DB unavailable: 503;
- audit failure on privileged policy/kill mutation: fail closed.

## Security boundary

The service is designed to remain independent of mutable strategy logic:
- no strategy process may write risk policy with trader credentials;
- no request-local override of server policy;
- no request-local override of kill switch;
- tenant/account scoping enforced at every store query;
- production service account has no withdrawal capability at venues.

## CI and test requirements

CI must include PostgreSQL service-container integration and prove:
- trader cannot submit limits in V3 to weaken policy;
- trader cannot unkill;
- risk/admin policy lifecycle works;
- exactly one policy is active after transactional activation;
- stale state fails closed;
- database outage makes readiness false;
- duplicate idempotent checks replay the original result;
- same key/different order conflicts;
- cross-tenant reads/mutations fail;
- state/policy/kill versions are embedded in decision evidence;
- existing V2 tests remain green.

## Acceptance gates

RiskGuard V3 is customer-grade only after:
- all tests pass;
- policy authority is server-side;
- kill switch is persistent and independently controlled;
- stale state is rejected;
- policy/decision history survives process restart;
- DB unavailability fails closed;
- production auth is asymmetric/JWKS based;
- audit trail can reconstruct who changed policy/kill state and which versions drove each decision.
