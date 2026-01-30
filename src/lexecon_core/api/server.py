"""Lexecon Core API - Minimal API for proof-of-concept.

Endpoints:
- POST /decide - Evaluate a decision request
- GET /ledger/entries - List ledger entries
- GET /health - Health check

For enterprise features (evidence export, verification, multi-tenancy):
    https://lexecon.ai/enterprise
"""

import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from lexecon_core.policy.engine import PolicyEngine, PolicyMode
from lexecon_core.ledger.chain import LedgerChain


# Pydantic models
class DecisionRequestModel(BaseModel):
    actor: str = Field(..., description="Actor requesting the action")
    action: str = Field(..., description="Action to perform")
    resource: Optional[str] = Field(None, description="Resource being accessed")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")


class DecisionResponse(BaseModel):
    decision_id: str
    decision: str
    reason: str
    timestamp: str


# Create FastAPI app
app = FastAPI(
    title="Lexecon Core",
    description="Governance control plane for AI decisions - Core API",
    version="0.1.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
policy_engine: Optional[PolicyEngine] = None
ledger: LedgerChain = LedgerChain()
node_id: str = str(uuid.uuid4())
startup_time: float = time.time()


def initialize():
    """Initialize the policy engine."""
    global policy_engine
    if policy_engine is None:
        policy_engine = PolicyEngine(mode=PolicyMode.STRICT)
    
    # Add a sample policy
    from lexecon_core.policy.terms import PolicyTerm
    from lexecon_core.policy.relations import PolicyRelation
    
    actor = PolicyTerm.actor("ai_agent:default")
    action = PolicyTerm.action("access_data")
    policy_engine.add_relation(PolicyRelation.permits(actor, action))


@app.on_event("startup")
async def startup():
    initialize()


@app.get("/health")
async def health():
    """Health check."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "node_id": node_id,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/decide", response_model=DecisionResponse)
async def decide(request: DecisionRequestModel):
    """Evaluate a governance decision.
    
    This is the core primitive. For evidence bundles and compliance automation,
    see https://lexecon.ai/enterprise
    """
    initialize()
    
    decision_id = f"dec_{int(time.time() * 1000)}"
    
    # Evaluate
    result = policy_engine.evaluate(
        actor=request.actor,
        action=request.action,
        context=request.context,
    )
    
    decision = "allow" if result.allowed else "deny"
    
    # Log to ledger
    entry = ledger.append(
        "decision",
        {
            "decision_id": decision_id,
            "actor": request.actor,
            "action": request.action,
            "decision": decision,
            "reason": result.reason,
        },
    )
    
    return DecisionResponse(
        decision_id=decision_id,
        decision=decision,
        reason=result.reason,
        timestamp=datetime.utcnow().isoformat(),
    )


@app.get("/ledger/entries")
async def list_entries(
    event_type: Optional[str] = None,
    limit: Optional[int] = None,
):
    """List ledger entries.
    
    For chain verification and evidence export, see enterprise distribution.
    """
    entries = ledger.entries
    
    if event_type:
        entries = [e for e in entries if e.event_type == event_type]
    
    if limit:
        entries = entries[-limit:]
    
    return {
        "entries": [e.to_dict() for e in entries],
        "total": len(ledger.entries),
        "note": "Core edition - basic ledger only",
    }


@app.get("/")
async def root():
    """API info."""
    return {
        "name": "Lexecon Core",
        "version": "0.1.0",
        "description": "Governance control plane for AI decisions",
        "endpoints": ["/health", "/decide", "/ledger/entries"],
        "enterprise": "https://lexecon.ai/enterprise",
    }
