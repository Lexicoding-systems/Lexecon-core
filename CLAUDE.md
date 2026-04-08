# CLAUDE.md — Lexecon Core

AI assistant reference for the `lexecon-core` repository.

---

## Project Overview

Lexecon Core is the **open-source proof layer** of the Lexecon AI governance platform — a minimal, fast policy engine with a tamper-evident ledger. It answers one question: *"Is this real and does it work?"*

- **Package name:** `lexecon-core` (PyPI) / `lexecon_core` (import)
- **Version:** 0.1.0 (Beta)
- **License:** Apache 2.0
- **Python:** 3.8–3.12
- **Maintained by:** Lexicoding Systems

---

## Repository Layout

```
Lexecon-core/
├── src/lexecon_core/          # All source code (src layout)
│   ├── __init__.py            # Public API surface
│   ├── api/
│   │   └── server.py          # FastAPI application
│   ├── policy/
│   │   ├── engine.py          # PolicyEngine, PolicyMode, PolicyDecision
│   │   ├── terms.py           # PolicyTerm, TermType
│   │   └── relations.py       # PolicyRelation, RelationType
│   ├── ledger/
│   │   ├── __init__.py        # Re-exports LedgerChain, LedgerEntry
│   │   └── chain.py           # LedgerChain, LedgerEntry
│   └── examples/
│       └── quickstart.py      # Runnable demo
├── examples/                  # Root-level example scripts
├── docs/
│   └── ENTERPRISE.md          # Enterprise tier comparison
├── .github/
│   └── workflows/
│       └── greetings.yml      # First-time contributor greeting only
├── pyproject.toml             # Build config, deps, tool config
├── README.md
└── LICENSE
```

---

## Technology Stack

| Concern | Tool |
|---------|------|
| Language | Python 3.8+ |
| Web framework | FastAPI 0.109.0+ |
| Data validation | Pydantic 2.5.0+ |
| ASGI server | uvicorn[standard] 0.27.0+ |
| Formatting | black (100-char line length) |
| Type checking | mypy 1.8+ |
| Testing | pytest 7.4+ + pytest-cov |

---

## Installation & Setup

```bash
# Minimum install
pip install lexecon-core

# With server support (adds uvicorn)
pip install "lexecon-core[server]"

# Development install (adds pytest, black, mypy)
pip install -e ".[dev]"
```

---

## Development Commands

There is no Makefile. Run tools directly.

```bash
# Format code
black .

# Type check
mypy src/

# Run tests (no tests exist yet — see Known Issues)
pytest
pytest --cov=lexecon_core

# Run the API server locally
python -m lexecon_core.api.server
# Server starts at http://localhost:8000
```

---

## Core Abstractions

### PolicyTerm (`src/lexecon_core/policy/terms.py`)

A **node** in the policy graph. Represents actors, actions, resources, data classes, or contexts.

```python
from lexecon_core.policy.terms import PolicyTerm, TermType

actor = PolicyTerm.create_actor("ai_agent", "AI Agent", "Customer service agent")
action = PolicyTerm.create_action("read_data", "Read Data")
```

Term IDs are namespaced: `actor:<id>`, `action:<id>`, `data:<id>`, `resource:<id>`.

**Serialization supports two formats:**
- Full: `{"term_id": "...", "term_type": "...", "label": "...", "description": "..."}`
- Simplified: `{"id": "...", "type": "...", "name": "..."}`

### PolicyRelation (`src/lexecon_core/policy/relations.py`)

An **edge** in the policy graph. Connects terms with a typed relationship.

| Type | Meaning |
|------|---------|
| `PERMITS` | Source actor may perform target action |
| `FORBIDS` | Source actor may not perform target action |
| `REQUIRES` | Source requires target as precondition |
| `IMPLIES` | Source implies target |
| `CONFLICTS` | Source conflicts with target |

```python
from lexecon_core.policy.relations import PolicyRelation

rel = PolicyRelation.permits(source="actor:ai_agent", target="action:read_data")
```

**Serialization supports three formats:**
- Full: `{"relation_id": ..., "relation_type": "permits", "source": ..., "target": ...}`
- Simplified: `{"type": "permits", "subject": ..., "action": ...}`
- Three-field: `{"type": "permits", "subject": ..., "action": ..., "object": ...}` (object stored in metadata)

### PolicyEngine (`src/lexecon_core/policy/engine.py`)

The evaluation core. Manages the policy graph and evaluates decision requests.

```python
from lexecon_core import PolicyEngine, PolicyMode

engine = PolicyEngine(mode=PolicyMode.STRICT)
engine.add_term(actor)
engine.add_term(action)
engine.add_relation(rel)

result = engine.evaluate(actor="actor:ai_agent", action="action:read_data")
# result.allowed → True/False
# result.reason  → Human-readable explanation
```

**Evaluation modes:**

| Mode | Behavior |
|------|----------|
| `STRICT` (default) | Deny unless explicitly permitted |
| `PERMISSIVE` | Allow unless explicitly forbidden |
| `PARANOID` | Deny high-risk unless human confirmation |

**`PolicyDecision`** supports both attribute access (`result.allowed`) and dict-style access (`result["allowed"]`) for backwards compatibility.

**Term matching** (`_term_matches`) checks: exact ID match → label match → substring match (for backwards compatibility).

**Policy hashing** uses deterministic SHA-256 over canonical JSON (`sort_keys=True`). The hash is invalidated on any `add_term` or `add_relation` call.

### LedgerChain (`src/lexecon_core/ledger/chain.py`)

An **append-only, hash-chained audit log**. Each `LedgerEntry` contains a SHA-256 hash of itself and a link to the previous entry's hash.

```python
from lexecon_core import LedgerChain

ledger = LedgerChain()                          # Starts with a genesis entry
entry = ledger.append("decision", {"actor": "x", "action": "y"})
report = ledger.generate_audit_report()
check  = ledger.verify_integrity()              # {"valid": True, "chain_intact": True, ...}
```

- Genesis entry uses `previous_hash = "0" * 64`
- Entry IDs are sequential: `genesis`, `entry_1`, `entry_2`, ...
- Optional `storage` parameter accepts a `LedgerStorage` instance for persistence (interface defined but not implemented in Core)

---

## API Server (`src/lexecon_core/api/server.py`)

FastAPI application with global in-memory state.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info and version |
| `/health` | GET | Node health + uptime |
| `/decide` | POST | Evaluate governance decision |
| `/ledger/entries` | GET | Query ledger entries |

### `POST /decide`

Request body:
```json
{
  "actor": "ai_agent:customer_service",
  "action": "access_customer_data",
  "resource": "optional-resource-id",
  "context": {"purpose": "support_ticket"}
}
```

Response:
```json
{
  "decision_id": "dec_1706553600000",
  "decision": "allow",
  "reason": "Permitted by 1 rule(s), no conflicts",
  "timestamp": "2026-01-29T18:00:00.000000"
}
```

### `GET /ledger/entries`

Query params: `?event_type=decision&limit=50`

**Global state initialized on startup:**
- `policy_engine` — lazily initialized `PolicyEngine(mode=STRICT)` with one sample rule: `ai_agent:default` may `access_data`
- `ledger` — fresh `LedgerChain()` (in-memory, reset on server restart)
- `node_id` — UUID generated at import time
- `startup_time` — Unix timestamp

**CORS:** `allow_origins=["*"]` — all origins allowed. Add your own auth layer.

---

## Public API Surface (`src/lexecon_core/__init__.py`)

```python
from lexecon_core import (
    PolicyEngine,
    PolicyMode,
    PolicyTerm,
    PolicyRelation,
    RelationType,
    LedgerChain,
    LedgerEntry,
)
```

---

## Code Conventions

- **Line length:** 100 characters (black)
- **Naming:** `PascalCase` for classes/enums, `snake_case` for methods/variables, `UPPER_CASE` for enum values
- **Imports:** Always use `lexecon_core.*` — never `lexecon.*`
- **Type hints:** Required throughout; mypy enforced
- **Docstrings:** Triple-quoted module and class docstrings expected
- **Dataclasses:** Used for immutable data structures (`LedgerEntry`, `PolicyTerm`, `PolicyRelation`)
- **Enums:** Use `Enum` for all typed categorical values
- **Serialization:** Every model implements `to_dict()` / `from_dict()` classmethods

---

## Known Issues & Gaps

### Critical Bug — Wrong Import Path
`src/lexecon_core/policy/engine.py` (lines 11–12) and `src/lexecon_core/ledger/__init__.py` (line 3) import from `lexecon.*` instead of `lexecon_core.*`. These will raise `ModuleNotFoundError` at runtime:

```python
# engine.py — WRONG (causes ImportError)
from lexecon.policy.relations import PolicyRelation, RelationType
from lexecon.policy.terms import PolicyTerm

# ledger/__init__.py — WRONG (causes ImportError)
from lexecon.ledger.chain import LedgerChain, LedgerEntry
```

**Fix:** Change all `lexecon.` imports to `lexecon_core.` in those two files.

### No Tests
`pytest` is in dev dependencies but no test files exist. No `tests/` directory. The quickstart example (`src/lexecon_core/examples/quickstart.py`) serves as the only smoke test.

### No CI for Tests/Lint
`.github/workflows/greetings.yml` only greets first-time contributors. No automated test, lint, or build checks run on PRs.

### No Persistence
`LedgerChain` is in-memory only. The `storage` parameter interface exists in `chain.py` but no concrete `LedgerStorage` implementation is provided in Core.

### Missing Docs
`README.md` links to `docs/API.md`, `docs/POLICY.md`, and `docs/LEDGER.md` — none of these files exist.

### `PolicyTerm` Factory Method Naming Inconsistency
`server.py` calls `PolicyTerm.actor(...)` and `PolicyTerm.action(...)` but the actual factory methods are named `PolicyTerm.create_actor(...)` and `PolicyTerm.create_action(...)`. This will raise `AttributeError` at startup.

---

## What Belongs in Enterprise (Not This Repo)

- Evidence bundles (signed ZIP with manifest)
- Chain integrity verification UI
- Multi-tenancy / tenant isolation
- SOC2 / EU AI Act compliance artifacts
- SIEM integration (Splunk, Datadog)
- Board-level compliance dashboards
- SQLite-backed `LedgerStorage` implementation

See `docs/ENTERPRISE.md` for the full feature matrix.

---

## Git Workflow

- Default branch: `main`
- Feature branches follow pattern: `claude/<description>`
- Commits are direct; no PR template currently enforced
- GitHub Actions currently does not run tests on push

---

## Quick Reference — Decision Flow

```
POST /decide
    │
    ▼
initialize()              ← lazy-creates PolicyEngine if None
    │
    ▼
policy_engine.evaluate(actor, action, context)
    │
    ├── _find_relations(PERMITS, actor, action)
    ├── _find_relations(FORBIDS, actor, action)
    ├── Apply mode logic (STRICT / PERMISSIVE / PARANOID)
    └── Return PolicyDecision(allowed, reason, ...)
    │
    ▼
ledger.append("decision", {...})   ← hash-chained log entry
    │
    ▼
Return DecisionResponse
```
