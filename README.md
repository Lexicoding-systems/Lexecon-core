# Lexecon Core

The governance control plane for AI decisions.

**Kick the tires in 5 minutes:**

```bash
pip install lexecon-core
python -m lexecon_core.examples.quickstart
```

**For evidence bundles, compliance automation, and enterprise deployment:**  
[lexecon.ai/enterprise](https://lexecon.ai/enterprise)

---

## What is Lexecon Core?

Lexecon Core is the **proof layer**: a minimal, fast policy engine with a tamper-evident ledger. It exists to answer one question: *"Is this real and does it work?"*

Core provides:
- **Policy Engine**: Graph-based deterministic evaluation (<10ms)
- **Ledger**: Append-only hash chain (SHA-256 linked entries)
- **API**: `/decide` and `/ledger/entries` endpoints

Core is **Apache 2.0 licensed** and designed for engineers to validate the primitive without a sales call.

---

## Quick Start

### Install

```bash
pip install lexecon-core
```

### Run the API

```bash
python -m lexecon_core.api.server
# Server runs at http://localhost:8000
```

### Make a Decision

```bash
curl -X POST http://localhost:8000/decide \
  -H "Content-Type: application/json" \
  -d '{
    "actor": "ai_agent:customer_service",
    "action": "access_customer_data",
    "context": {"purpose": "support_ticket"}
  }'
```

Response:
```json
{
  "decision_id": "dec_1706553600000",
  "decision": "allow",
  "reason": "Policy permits ai_agent:customer_service to perform access_customer_data",
  "timestamp": "2026-01-29T18:00:00.000000"
}
```

### Query the Ledger

```bash
curl http://localhost:8000/ledger/entries
```

---

## Architecture

```
┌─────────────────────────────────────┐
│         FastAPI Server              │
├─────────────────────────────────────┤
│  PolicyEngine (graph-based)         │
│       ↓                             │
│  LedgerChain (hash-chained)         │
└─────────────────────────────────────┘
```

- **No persistence** (in-memory only)
- **No authentication** (add your own)
- **No multi-tenancy** (single tenant)
- **No evidence export** (see Enterprise)

---

## When to Upgrade to Enterprise

| Trigger | Core | Enterprise |
|---------|------|------------|
| Regulator asks for evidence bundle | ❌ | ✅ Signed ZIP with manifest |
| CISO needs chain verification | ❌ | ✅ Integrity verification UI |
| Multi-team deployment | ❌ | ✅ Tenant isolation |
| SOC2/EU AI Act compliance | ❌ | ✅ Automated artifact generation |
| SIEM integration required | ❌ | ✅ Splunk/Datadog export |
| Board-ready compliance reports | ❌ | ✅ Executive dashboards |

**[Book a 90-day pilot ($15,000)](mailto:pilot@lexecon.ai)**

---

## Documentation

- [API Reference](docs/API.md)
- [Policy Engine](docs/POLICY.md)
- [Ledger Design](docs/LEDGER.md)
- [Enterprise Features](docs/ENTERPRISE.md)

---

## License

Apache 2.0 - See [LICENSE](LICENSE)

---

**Built by [Lexicoding Systems](https://lexecon.ai)**
