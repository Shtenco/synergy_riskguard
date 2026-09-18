import json
from fastapi.testclient import TestClient
from synergy_riskguard.api import app
from synergy_riskguard.enterprise.auth import sign_token
from synergy_riskguard.enterprise.models import Role

SECRET="dev-only-change-me-not-for-production"

def token(role):
    return sign_token(SECRET,subject="fund-user",roles=[Role(role)],tenant_id="fund-a",ttl_seconds=3600)

def test_product_enterprise_endpoint_and_audit_linkage():
    c=TestClient(app)
    request_id="acceptance-123"
    res=c.post('/enterprise/v1/risk/check',json={'state': {'equity': 100000, 'start_day_equity': 100500, 'high_watermark': 101000, 'gross_exposure': 10000, 'returns': [0.001, -0.002, 0.001, 0.0005, -0.001, 0.002]}, 'order': {'symbol': 'EURUSD', 'notional': 5000, 'side': 'BUY'}},headers={"Authorization":"Bearer "+token('risk'),"X-Request-ID":request_id})
    assert res.status_code==200, res.text
    body=res.json()
    for key in ['action', 'approved_notional', 'request_id']: assert key in body
    assert body["request_id"]==request_id
    admin=token("admin")
    audit=c.get('/enterprise/audit',headers={"Authorization":"Bearer "+admin})
    assert audit.status_code==200
    assert any(e["request_id"]==request_id for e in audit.json())

def test_product_endpoint_requires_authorized_role():
    c=TestClient(app)
    res=c.post('/enterprise/v1/risk/check',json={'state': {'equity': 100000, 'start_day_equity': 100500, 'high_watermark': 101000, 'gross_exposure': 10000, 'returns': [0.001, -0.002, 0.001, 0.0005, -0.001, 0.002]}, 'order': {'symbol': 'EURUSD', 'notional': 5000, 'side': 'BUY'}},headers={"Authorization":"Bearer "+token("viewer")})
    assert res.status_code==403

def test_api_exposes_enterprise_control_routes():
    paths={r.path for r in app.routes}
    assert '/enterprise/health' in paths
    assert '/enterprise/v1/risk/check' in paths
