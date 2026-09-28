from uuid import UUID

from synergy_riskguard.core import AccountState, OrderIntent, decide
from synergy_riskguard.synergy_contracts import CONTRACT_ID, risk_decision_payload


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
