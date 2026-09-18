# Customer pilot — SYNERGY RiskGuard

Objective: evaluate an order against account state and deterministic risk limits before execution inside the customer environment under agreed identity, audit, risk and operational controls.

1. **Scope:** freeze use case, representative data/workload and pass/fail criteria.
2. **UAT deployment:** pinned revision, customer identity/audit/monitoring, live off.
3. **Functional evidence:** run `/enterprise/v1/risk/check`, verify roles, request ID and fields **action, approved_notional, reasons, request_id**.
4. **Resilience/performance:** target-hardware load plus failure drills.
5. **Domain gate:** customer OOS/paper process with realistic costs/latency/capacity where relevant.

Final decision: reject / extend research / paper / bounded canary / production review. Technology acceptance does not imply alpha or future profitability.