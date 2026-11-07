from agent import agent

test_product = {
    "name": "Wireless Mouse",
    "stock": 15,
    "sales": [8, 10, 12, 9, 11],
    "suppliers": [
        {
            "name": "Alpha Supplies",
            "cost": 320,
            "days": 2
        },
        {
            "name": "Beta Traders",
            "cost": 280,
            "days": 5
        }
    ]
}

result = agent.analyze_inventory(test_product)

print("\n===== SUPPLYCHAINIQ AI AGENT =====")

for key, value in result.items():
    if key != "all_suppliers":
        print(key, ":", value)