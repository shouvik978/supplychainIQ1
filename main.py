import math
from datetime import datetime

# ==========================================
# SUPPLYCHAINIQ - AUTONOMOUS SUPPLY CHAIN AGENT
# ==========================================

SAFETY_DAYS = 2

# Simulated warehouse data
products = {
    "Wireless Mouse": {
        "stock": 15,
        "sales": [9, 10, 11, 10, 9, 10, 11],
        "suppliers": [
            {"name": "Alpha Supplies", "cost": 320, "days": 2},
            {"name": "Beta Traders", "cost": 290, "days": 5}
        ]
    },
    "Keyboard": {
        "stock": 80,
        "sales": [5, 6, 5, 7, 6, 5, 6],
        "suppliers": [
            {"name": "TechSource", "cost": 450, "days": 3},
            {"name": "KeyWorld", "cost": 420, "days": 6}
        ]
    },
    "USB Cable": {
        "stock": 20,
        "sales": [8, 7, 9, 8, 10, 8, 9],
        "suppliers": [
            {"name": "ConnectPro", "cost": 80, "days": 2},
            {"name": "WireHub", "cost": 70, "days": 4}
        ]
    },
    "Monitor": {
        "stock": 30,
        "sales": [2, 2, 3, 2, 2, 3, 2],
        "suppliers": [
            {"name": "DisplayTech", "cost": 6500, "days": 4},
            {"name": "ScreenWorld", "cost": 6200, "days": 7}
        ]
    }
}


# ==========================================
# TOOL 1: INVENTORY LOOKUP
# ==========================================

def inventory_lookup(product):

    data = products[product]
    stock = data["stock"]

    print("\n[TOOL 1] Inventory Lookup")
    print("Product:", product)
    print("Available Stock:", stock)

    return stock


# ==========================================
# TOOL 2: SALES HISTORY ANALYSIS
# ==========================================

def sales_analysis(product):

    sales = products[product]["sales"]

    average = sum(sales) / len(sales)

    print("\n[TOOL 2] Sales History Analysis")
    print("Last 7 days sales:", sales)
    print("Average Daily Demand:", round(average, 2))

    return average


# ==========================================
# TOOL 3: SUPPLIER COMPARISON
# ==========================================

def supplier_comparison(product, stock, demand):

    suppliers = products[product]["suppliers"]

    days_cover = stock / demand if demand > 0 else float("inf")

    options = []

    print("\n[TOOL 3] Supplier Comparison")

    for supplier in suppliers:

        lead = supplier["days"]

        quantity = max(
            0,
            math.ceil(demand * (lead + SAFETY_DAYS) - stock)
        )

        total_cost = quantity * supplier["cost"]

        feasible = lead <= days_cover

        options.append({
            "name": supplier["name"],
            "cost": supplier["cost"],
            "days": lead,
            "quantity": quantity,
            "total": total_cost,
            "feasible": feasible
        })

        print(
            supplier["name"],
            "| Unit Cost:", supplier["cost"],
            "| Delivery:", lead, "days",
            "| Feasible:", feasible
        )

    return options, days_cover


# ==========================================
# TOOL 4: REORDER CALCULATOR
# ==========================================

def reorder_calculator(stock, demand, delivery_days):

    expected_demand = demand * delivery_days

    safety_stock = demand * SAFETY_DAYS

    reorder_quantity = max(
        0,
        math.ceil(expected_demand + safety_stock - stock)
    )

    print("\n[TOOL 4] Reorder Calculation")

    print("Expected Delivery Demand:",
          round(expected_demand, 2))

    print("Safety Stock:", round(safety_stock, 2))

    print("Recommended Quantity:", reorder_quantity)

    return reorder_quantity


# ==========================================
# MAIN AGENT CONTROLLER
# ==========================================

def run_agent(product):

    print("\n" + "=" * 48)
    print("       SUPPLYCHAINIQ AUTONOMOUS AGENT")
    print("=" * 48)

    print("\nAgent started...")
    print("Analyzing product:", product)

    # Step 1: Inventory
    stock = inventory_lookup(product)

    # Step 2: Sales analysis
    demand = sales_analysis(product)

    # Step 3: Supplier analysis
    options, days_cover = supplier_comparison(
        product, stock, demand
    )

    # Step 4: Risk assessment
    fastest = min(options, key=lambda x: x["days"])

    if days_cover < fastest["days"]:
        risk = "CRITICAL"
    elif days_cover < fastest["days"] + 2:
        risk = "HIGH"
    elif days_cover < fastest["days"] + 5:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    # Select supplier
    feasible = [s for s in options if s["feasible"]]

    if feasible:
        selected = min(feasible, key=lambda x: x["cost"])
        reason = "Lowest unit cost among suppliers able to deliver before stockout."
    else:
        selected = fastest
        reason = "No supplier can arrive before stockout. Selected fastest delivery."

    # Step 5: Reorder
    quantity = reorder_calculator(
        stock, demand, selected["days"]
    )

    total_cost = quantity * selected["cost"]

    # Step 6: Procurement report
    print("\n" + "=" * 48)
    print("          PROCUREMENT DECISION REPORT")
    print("=" * 48)

    print("Product:", product)
    print("Current Stock:", stock)
    print("Daily Demand:", round(demand, 2))
    print("Stock Coverage:", round(days_cover, 2), "days")
    print("Stockout Risk:", risk)

    print("\nRECOMMENDED SUPPLIER:", selected["name"])
    print("Delivery Time:", selected["days"], "days")
    print("Purchase Quantity:", quantity)
    print("Estimated Total Cost: Rs.", total_cost)
    print("Decision Reason:", reason)

    # Compare alternative strategies
    print("\n--- ALTERNATIVE PROCUREMENT STRATEGIES ---")

    cheapest = min(options, key=lambda x: x["cost"])

    print(
        "Fastest Supplier:",
        fastest["name"],
        "| Delivery:", fastest["days"],
        "days | Cost:", fastest["quantity"] * fastest["cost"]
    )

    print(
        "Cheapest Supplier:",
        cheapest["name"],
        "| Delivery:", cheapest["days"],
        "days | Cost:", cheapest["quantity"] * cheapest["cost"]
    )

    print("\nFINAL ACTION:")

    if quantity > 0:
        print("Place an order for", quantity,
              "units from", selected["name"])
    else:
        print("No immediate purchase required.")

    print("\nReport Generated:",
          datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

    print("\nAgent execution completed.")
    print("=" * 48)


# ==========================================
# USER INTERFACE
# ==========================================

def main():

    print("\nWELCOME TO SUPPLYCHAINIQ")
    print("AI-Based Inventory Decision System")

    product_list = list(products.keys())

    print("\nAvailable Products:")

    for i, product in enumerate(product_list, 1):
        print(i, ".", product)

    try:
        choice = int(input("\nSelect Product (1-4): "))

        if choice < 1 or choice > len(product_list):
            print("Invalid product selection.")
            return

        selected_product = product_list[choice - 1]

        run_agent(selected_product)

    except ValueError:
        print("Please enter a valid number.")


if __name__ == "__main__":
    main()