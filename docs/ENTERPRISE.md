# Lexecon Enterprise

Core proves the primitive works. Enterprise gets you through procurement and audit.

---

## You Need Enterprise When:

### 1. Regulator Requests Evidence Bundle
**Core:** Cannot export
**Enterprise:** Signed ZIP bundle with:
- `ledger_events.json` - All entries with cryptographic hashes
- `verification_report.json` - Chain integrity check
- `policies.json` - Policy version references
- `summary.md` - Human-readable compliance summary
- `manifest.json` - Signed manifest with file integrity

### 2. CISO Requires Chain Verification
**Core:** Basic ledger only
**Enterprise:** Integrity verification endpoint and UI
- Click "Verify Integrity" → cryptographically verify entire chain
- Visual badge: ✅ VERIFIED or ❌ FAILED
- Drill into failures with entry-level detail

### 3. Multi-Team Deployment
**Core:** Single tenant
**Enterprise:** Full multi-tenancy
- Tenant isolation at row level
- Tenant membership enforcement
- Usage tracking per tenant

### 4. Compliance Automation (SOC2, EU AI Act)
**Core:** Manual compliance
**Enterprise:** Automated artifacts
- EU AI Act Article 12 (record keeping)
- EU AI Act Article 14 (human oversight)
- SOC2 evidence packs
- Pre-built policy packs by vertical

### 5. SIEM Integration
**Core:** Standalone
**Enterprise:** Native integrations
- Splunk export
- Datadog integration
- Custom webhook alerts

### 6. Board-Ready Reporting
**Core:** Raw JSON
**Enterprise:** Executive dashboards
- Compliance status overview
- Risk trend analysis
- Audit-ready summaries

---

## Enterprise Distribution

**Private repository** with:
- Evidence export service
- Integrity verification
- Multi-tenancy service
- Usage tracking and tier enforcement
- Compliance mappings
- Enterprise integrations
- Deployment bundles (K8s, Terraform)

---

## Pricing

| Tier | Price | Includes |
|------|-------|----------|
| **Community** (Core) | Free | Self-hosted, basic ledger, no support |
| **Pilot** | $15,000 (90 days) | Enterprise build, custom policy pack, weekly exports |
| **Growth** | $60,000/year | Unlimited usage, support, SIEM integration |
| **Enterprise** | $150,000+/year | SLA, advanced policy packs, dedicated support |

---

## Pilot Program

**90-Day Deployment: $15,000**

Includes:
- Enterprise build deployed in your environment
- Custom policy pack for your top 3 AI workflows
- Weekly evidence exports
- Email support

**Success Criteria:**
- Auditable decisions
- Exportable compliance artifacts
- Provable hash chain

**[Book a Pilot](mailto:pilot@lexecon.ai)**

---

## Why Not Build It Yourself?

You could. Core is open source (Apache 2.0).

But the evidence bundle format, chain verification, and compliance mappings took **18 months** to get regulator-grade. You're not buying features—you're buying:

1. **Audit confidence** - Evidence that holds up under scrutiny
2. **Deployment speed** - Production-ready in weeks, not quarters
3. **Maintenance burden** - We handle security updates and compliance changes

---

**[Contact Sales](mailto:sales@lexecon.ai)** | **[Book a Pilot](mailto:pilot@lexecon.ai)**
