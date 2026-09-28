from __future__ import annotations
from typing import Any
from uuid import UUID

from .core import Decision


CONTRACT_ID = "synergy.trading.risk-decision/v1"
AUTHORITY = "trading_risk"


def risk_decision_payload(
    *,
    source_event_id: UUID | str,
    decision: Decision,
    account_state_version: str,
    policy_version: str,
) -> dict[str, Any]:
    return {
        "source_event_id": str(source_event_id),
        "action": decision.action.value,
        "approved_notional": str(decision.approved_notional),
        "reasons": list(decision.reasons),
        "metrics": dict(decision.metrics),
        "account_state_version": account_state_version,
        "policy_version": policy_version,
    }
