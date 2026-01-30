"""Lexecon Core Quickstart

Run this to see the policy engine and ledger in action.
"""

from lexecon_core.policy.engine import PolicyEngine, PolicyMode
from lexecon_core.policy.terms import PolicyTerm
from lexecon_core.policy.relations import PolicyRelation
from lexecon_core.ledger.chain import LedgerChain


def main():
    print("=" * 60)
    print("Lexecon Core - Quickstart Demo")
    print("=" * 60)
    
    # Initialize policy engine
    print("\n1. Initializing policy engine...")
    engine = PolicyEngine(mode=PolicyMode.STRICT)
    
    # Define terms
    actor = PolicyTerm.actor("ai_agent:customer_service")
    action = PolicyTerm.action("access_customer_data")
    constraint = PolicyTerm.constraint("purpose", "support")
    
    # Add policy: customer service can access data for support purposes
    engine.add_relation(
        PolicyRelation.permits(actor, action, [constraint])
    )
    print("   ✓ Policy loaded: customer_service can access_customer_data for support")
    
    # Initialize ledger
    print("\n2. Initializing tamper-evident ledger...")
    ledger = LedgerChain()
    print(f"   ✓ Ledger initialized with genesis entry")
    print(f"     Genesis hash: {ledger.entries[0].entry_hash[:16]}...")
    
    # Make decisions
    print("\n3. Evaluating decisions...")
    
    test_cases = [
        {
            "actor": "ai_agent:customer_service",
            "action": "access_customer_data",
            "context": {"purpose": "support"},
            "expected": "allow"
        },
        {
            "actor": "ai_agent:marketing",
            "action": "access_customer_data",
            "context": {"purpose": "advertising"},
            "expected": "deny"
        },
    ]
    
    for i, test in enumerate(test_cases, 1):
        result = engine.evaluate(
            actor=test["actor"],
            action=test["action"],
            context=test["context"],
        )
        
        decision = "allow" if result.allowed else "deny"
        status = "✓" if decision == test["expected"] else "✗"
        
        print(f"\n   Decision {i}:")
        print(f"     Actor:  {test['actor']}")
        print(f"     Action: {test['action']}")
        print(f"     Context: {test['context']}")
        print(f"     Result: {decision} {status}")
        print(f"     Reason: {result.reason}")
        
        # Log to ledger
        entry = ledger.append(
            "decision",
            {
                "actor": test["actor"],
                "action": test["action"],
                "decision": decision,
                "context": test["context"],
            }
        )
        print(f"     Ledger: Entry #{len(ledger.entries)-1} ({entry.entry_hash[:16]}...)")
    
    # Show ledger stats
    print("\n4. Ledger status:")
    print(f"   Total entries: {len(ledger.entries)}")
    print(f"   Chain intact: {ledger.verify_integrity()['valid']}")
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  - Run the API: python -m lexecon_core.api.server")
    print("  - Read docs: https://github.com/Lexicoding-systems/lexecon-core")
    print("  - Enterprise: https://lexecon.ai/enterprise")


if __name__ == "__main__":
    main()
