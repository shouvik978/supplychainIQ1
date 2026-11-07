import streamlit as st
import pandas as pd
import math

from main import products, SAFETY_DAYS
from agent import agent

# PAGE CONFIG
st.set_page_config(
    page_title="SupplyChainIQ",
    page_icon="📦",
    layout="wide"
)

# CUSTOM STYLE
st.markdown("""
<style>
.stApp {
    background-color: #101827;
}
[data-testid="stMetric"] {
    background-color: #1d293b;
    padding: 18px;
    border-radius: 12px;
}
h1, h2, h3 {
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.title("📦 SupplyChainIQ")
st.caption("AI-Powered Inventory & Supply Chain Intelligence")

st.divider()

# SIDEBAR
st.sidebar.title("⚙️ Control Panel")

product = st.sidebar.selectbox(
    "Select Product",
    list(products.keys())
)

data = products[product]

stock = data["stock"]
sales = data["sales"]
demand = sum(sales) / len(sales)

# SUPPLIER ANALYSIS
days_cover = stock / demand if demand > 0 else float("inf")

supplier_data = []

for supplier in data["suppliers"]:

    lead = supplier["days"]

    quantity = max(
        0,
        math.ceil(demand * (lead + SAFETY_DAYS) - stock)
    )

    feasible = lead <= days_cover

    supplier_data.append({
        "Supplier": supplier["name"],
        "Unit Price (Rs)": supplier["cost"],
        "Delivery Days": lead,
        "Order Quantity": quantity,
        "Total Cost (Rs)": quantity * supplier["cost"],
        "Can Arrive Before Stockout": feasible
    })

suppliers = pd.DataFrame(supplier_data)

# SELECT SUPPLIER
fastest = suppliers.sort_values(
    "Delivery Days"
).iloc[0]

feasible_suppliers = suppliers[
    suppliers["Can Arrive Before Stockout"]
]

if not feasible_suppliers.empty:
    selected = feasible_suppliers.sort_values(
        "Unit Price (Rs)"
    ).iloc[0]
    reason = "Lowest-cost feasible supplier"
else:
    selected = fastest
    reason = "Fastest available delivery"

risk = (
    "CRITICAL" if days_cover < fastest["Delivery Days"]
    else "HIGH" if days_cover < fastest["Delivery Days"] + 2
    else "MEDIUM" if days_cover < fastest["Delivery Days"] + 5
    else "LOW"
)

# METRICS
st.subheader("📊 Inventory Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Current Stock", f"{stock} Units")
c2.metric("Daily Demand", f"{demand:.1f} Units")
c3.metric("Stock Coverage", f"{days_cover:.1f} Days")

c4.metric(
    "Stockout Risk",
    risk
)

st.divider()

# CHARTS
left, right = st.columns(2)

with left:
    st.subheader("📈 Sales History")

    sales_df = pd.DataFrame({
        "Day": [f"Day {i+1}" for i in range(len(sales))],
        "Sales": sales
    })

    st.bar_chart(
        sales_df.set_index("Day")
    )

with right:
    st.subheader("📦 Stock Information")

    st.progress(
        min(stock / max(stock + demand * 7, 1), 1.0)
    )

    st.write("Available Stock:", stock)
    st.write("Average Daily Demand:", round(demand, 2))

st.divider()

# SUPPLIER COMPARISON
st.subheader("🚚 Supplier Comparison")

st.dataframe(
    suppliers,
    use_container_width=True,
    hide_index=True
)

st.divider()

# AI AGENT INTEGRATION

st.subheader("🤖 SupplyChainIQ AI Agent")

result = agent.analyze_inventory({
    "name": product,
    **data
})

a, b, c = st.columns(3)

a.metric(
    "Recommended Supplier",
    result["supplier"]
)

b.metric(
    "Recommended Order",
    f'{result["order_quantity"]} Units'
)

c.metric(
    "Estimated Cost",
    f'₹{result["estimated_cost"]}'
)

st.metric(
    "Agent Stock Risk",
    result["risk"]
)

st.info(
    f'Agent Reasoning: {result["reason"]}'
)

if result["order_quantity"] > 0:
    st.success(
        f'Agent Recommendation: Order '
        f'{result["order_quantity"]} units from '
        f'{result["supplier"]}.'
    )
else:
    st.success("No immediate restocking required.")

# ALL INVENTORY
st.divider()

st.subheader("📋 Complete Warehouse Inventory")

inventory = []

for name, item in products.items():
    avg = sum(item["sales"]) / len(item["sales"])

    inventory.append({
        "Product": name,
        "Stock": item["stock"],
        "Daily Demand": round(avg, 2),
        "Stock Coverage": round(item["stock"] / avg, 2)
    })

st.dataframe(
    pd.DataFrame(inventory),
    use_container_width=True,
    hide_index=True
)

st.caption("SupplyChainIQ | Prototype v1.0 | Simulated Warehouse Data")
import streamlit as st
import pandas as pd
import math

from main import products, SAFETY_DAYS

# PAGE CONFIG
st.set_page_config(
    page_title="SupplyChainIQ",
    page_icon="📦",
    layout="wide"
)

# CUSTOM STYLE
st.markdown("""
<style>
.stApp {
    background-color: #101827;
}
[data-testid="stMetric"] {
    background-color: #1d293b;
    padding: 18px;
    border-radius: 12px;
}
h1, h2, h3 {
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# HEADER
# CUSTOMER STORE

st.divider()

st.header("🛒 Customer Shopping Store")

st.write("Select a product and purchase.")

for name, item in products.items():

    st.subheader(name)

    st.write("Available Stock:", item["stock"])

    quantity = st.number_input(
        "Select Quantity",
        min_value=1,
        max_value=max(1, item["stock"]),
        value=1,
        key=f"qty_{name}"
    )

    if st.button("Buy Now", key=f"buy_{name}"):

        if quantity <= item["stock"]:
            st.success(
                f"Purchase successful: {quantity} {name}"
            )
        else:
            st.error("Insufficient stock")