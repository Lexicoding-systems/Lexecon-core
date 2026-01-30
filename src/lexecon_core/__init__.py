"""Lexecon Core - The governance control plane for AI decisions.

Kick the tires in 5 minutes:
    pip install lexecon-core
    python -m lexecon_core.examples.quickstart

For evidence bundles, compliance automation, and enterprise deployment:
    https://lexecon.ai/enterprise
"""

__version__ = "0.1.0"

from lexecon_core.policy.engine import PolicyEngine, PolicyMode
from lexecon_core.policy.terms import PolicyTerm
from lexecon_core.policy.relations import PolicyRelation, RelationType
from lexecon_core.ledger.chain import LedgerChain, LedgerEntry

__all__ = [
    "PolicyEngine",
    "PolicyMode", 
    "PolicyTerm",
    "PolicyRelation",
    "RelationType",
    "LedgerChain",
    "LedgerEntry",
]
