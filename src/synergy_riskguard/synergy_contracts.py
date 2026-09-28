from __future__ import annotations
from typing import Any
from uuid import UUID

from .core import Decision, OrderIntent


CONTRACT_ID = "synergy.trading.risk-decision/v1"
AUTHORITY = "trading_risk"
UPSTREAM_CONTRACTS = {
    "synergy.trading.portfolio-decision/v1",
    "synergy.trading.validation-decision/v1",
}


def order_intent_from_validated_contracts(
    *,
    portfolio_payload: dict[str, Any],
    validation_payload: dict[str, Any],
    position_index: int = 0,
) -> OrderIntent:
    gate = str(validation_payload.get("gate", "")).upper()
    if gate not in {"PAPER", "CANARY"}:
        raise ValueError(f"validation gate does not permit risk evaluation: {gate}")
    positions = portfolio_payload.get("positions") or []
    try:
        p = positions[position_index]
    except (IndexError, TypeError) as exc:
        raise ValueError("missing portfolio position") from exc
    side = str(p["side"]).upper()
    if side not in {"BUY", "SELL"}:
        raise ValueError("FLAT position is not an executable order intent")
    notional = float(p["notional"])
    if notional <= 0:
        raise ValueError("notional must be positive")
    return OrderIntent(symbol=str(p["symbol"]), notional=notional, side=side)


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
