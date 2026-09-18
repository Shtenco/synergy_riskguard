# API examples — SYNERGY RiskGuard

Control: `/enterprise/health`, `/enterprise/metrics`, `/enterprise/whoami`, admin `/enterprise/audit`.

Primary action: `POST /enterprise/v1/risk/check` — roles **trader, risk**.

```json
{"state":{"equity":100000,"start_day_equity":100500,"high_watermark":101000,"gross_exposure":10000,"returns":[0.001,-0.002,0.001,0.0005,-0.001,0.002]},"order":{"symbol":"EURUSD","notional":5000,"side":"BUY"}}
```

```bash
curl -X POST http://127.0.0.1:8000/enterprise/v1/risk/check \\
 -H "Authorization: Bearer $TOKEN" \\
 -H "Content-Type: application/json" \\
 -H "X-Request-ID: pilot-001" \\
 -d @request.json
```

Expected response includes **action, approved_notional, reasons, request_id**. Generate evaluation tokens with `synergy_riskguard.enterprise.auth.sign_token`; production identity should use customer-managed identity. Canonical interface: `/docs` or `/openapi.json`.