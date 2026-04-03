TASKS = [
    {
        "id": 0,
        "observation": {
            "ticket_id": "T1",
            "message": "I want a refund for my order",
            "customer_tier": "basic",
            "history": [],
            "status": "open"
        },
        "expected": {
            "category": "billing",
            "priority": "medium",
            "route_to": "billing_team"
        }
    },
    {
        "id": 1,
        "observation": {
            "ticket_id": "T2",
            "message": "My app crashes every time I login",
            "customer_tier": "premium",
            "history": ["restart didn't work"],
            "status": "open"
        },
        "expected": {
            "category": "technical",
            "priority": "high",
            "route_to": "engineering"
        }
    },
    {
        "id": 2,
        "observation": {
            "ticket_id": "T3",
            "message": "Charged twice and app not working",
            "customer_tier": "enterprise",
            "history": ["previous complaint unresolved"],
            "status": "open"
        },
        "expected": {
            "category": "multi_issue",
            "priority": "critical",
            "route_to": "priority_support"
        }
    }
]