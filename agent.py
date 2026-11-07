import math


class SupplyChainAgent:

    def __init__(self, safety_days=3):
        self.safety_days = safety_days

    def analyze_inventory(self, product):

        stock = product["stock"]
        sales = product["sales"]
        suppliers = product["suppliers"]

        # Analyze demand
        demand = sum(sales) / len(sales)

        # Predict stock coverage
        days_cover = (
            stock / demand if demand > 0 else float("inf")
        )

        # Analyze suppliers
        supplier_results = []

        for supplier in suppliers:

            lead = supplier["days"]

            quantity = max(
                0,
                math.ceil(
                    demand * (lead + self.safety_days) - stock
                )
            )

            feasible = lead <= days_cover

            supplier_results.append({
                "Supplier": supplier["name"],
                "Price": supplier["cost"],
                "Delivery Days": lead,
                "Order Quantity": quantity,
                "Total Cost": quantity * supplier["cost"],
                "Feasible": feasible
            })

        # Select supplier
        feasible = [
            s for s in supplier_results if s["Feasible"]
        ]

        if feasible:
            selected = min(
                feasible,
                key=lambda x: x["Price"]
            )
            reason = "Lowest-cost feasible supplier"

        else:
            selected = min(
                supplier_results,
                key=lambda x: x["Delivery Days"]
            )
            reason = "Fastest available supplier"

        # Risk analysis
        fastest = min(
            s["days"] for s in suppliers
        )

        if days_cover < fastest:
            risk = "CRITICAL"
        elif days_cover < fastest + 2:
            risk = "HIGH"
        elif days_cover < fastest + 5:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        # Agent report
        return {
            "product": product.get("name", "Selected Product"),
            "current_stock": stock,
            "daily_demand": round(demand, 2),
            "stock_coverage": round(days_cover, 2),
            "risk": risk,
            "supplier": selected["Supplier"],
            "order_quantity": selected["Order Quantity"],
            "estimated_cost": selected["Total Cost"],
            "reason": reason,
            "all_suppliers": supplier_results
        }


# Create Agent
agent = SupplyChainAgent(safety_days=3)