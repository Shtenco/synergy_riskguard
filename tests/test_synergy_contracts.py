from uuid import UUID
import pytest

from synergy_riskguard.core import AccountState, OrderIntent, decide
from synergy_riskguard.synergy_contracts import (
    CONTRACT_ID,
    order_intent_from_validated_contracts,
    risk_decision_payload,
)


def test_risk_contract_payload_is_derived_from_core_decision():
    decision = decide(
        AccountState(
            equity=10000,
            start_day_equity=10000,
            high_watermark=10000,
            gross_exposure=0,
        ),
        OrderIntent(symbol="EURUSD", notional=1000, side="BUY"),
    )
    payload = risk_decision_payload(
        source_event_id=UUID("22222222-2222-4222-8222-222222222222"),
        decision=decision,
        account_state_version="acct-1",
        policy_version="risk-2.0",
    )
    assert CONTRACT_ID == "synergy.trading.risk-decision/v1"
    assert payload["action"] == "ALLOW"
    assert payload["approved_notional"] == "1000"


def test_rejected_validation_cannot_become_order_intent():
    portfolio = {"positions":[{"symbol":"EURUSD","side":"BUY","notional":"1000"}]}
    with pytest.raises(ValueError):
        order_intent_from_validated_contracts(
            portfolio_payload=portfolio,
            validation_payload={"gate":"REJECT"},
        )


def test_canary_validation_can_enter_risk_layer():
    order = order_intent_from_validated_contracts(
        portfolio_payload={"positions":[{"symbol":"EURUSD","side":"BUY","notional":"1000"}]},
        validation_payload={"gate":"CANARY"},
    )
    assert order.symbol == "EURUSD"
    assert order.notional == 1000
