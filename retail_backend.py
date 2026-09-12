"""Local retail queries extracted from Phase 8. No notebook execution or API calls."""
from pathlib import Path
from datetime import datetime
import re
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "processed"
dim_product = pd.read_csv(DATA / "dim_product.csv")
fact_sales = pd.read_csv(DATA / "fact_sales.csv")
fact_stock = pd.read_csv(DATA / "fact_stock.csv")
fact_soa = pd.read_csv(DATA / "fact_soa.csv")
inventory_decision = pd.read_csv(DATA / "phase5_inventory_intelligence" / "inventory_decision_layer.csv")
for column in ["In_Sales", "In_Stock", "In_SOA"]:
    dim_product[column] = dim_product[column].astype(str).str.lower().isin(["true", "1", "1.0"])


def normalize_model(value):
    """
    Normalize model numbers for comparison.

    Rules:
    - convert to uppercase
    - remove spaces
    - remove hyphens
    - remove underscores
    - remove other non-alphanumeric characters
    """

    if pd.isna(value):
        return None

    value = str(value).upper().strip()
    value = re.sub(r"[^A-Z0-9]", "", value)

    return value

model_columns = [
    "Product_Key",
    "Sales_Stock_Code",
    "Stock_Model",
    "SOA_Model"
]

for col in model_columns:
    dim_product[f"{col}_Normalized"] = (
        dim_product[col]
        .apply(normalize_model)
    )

def lookup_product(model_number, product_df=dim_product):

    query = normalize_model(model_number)

    if not query:
        return {
            "status": "invalid_input",
            "match_confidence": "none",
            "message": "No valid model number was provided."
        }

    match_columns = [
        "Product_Key_Normalized",
        "Sales_Stock_Code_Normalized",
        "Stock_Model_Normalized",
        "SOA_Model_Normalized"
    ]

    mask = False

    for col in match_columns:
        mask = mask | (product_df[col] == query)

    matches = product_df[mask].copy()

    if len(matches) == 0:
        return {
            "status": "not_matched",
            "match_confidence": "none",
            "message": "Product could not be confidently matched."
        }

    if len(matches) > 1:
        return {
            "status": "multiple_matches",
            "match_confidence": "medium",
            "match_count": len(matches),
            "matches": matches[
                [
                    "Product_ID",
                    "Product_Key",
                    "Product_Description",
                    "Product_Category"
                ]
            ]
        }

    row = matches.iloc[0]

    return {
        "status": "matched",
        "match_confidence": "high",
        "Product_ID": row["Product_ID"],
        "Product_Key": row["Product_Key"],
        "Product_Description": row["Product_Description"],
        "Product_Category": row["Product_Category"],
        "In_Sales": row["In_Sales"],
        "In_Stock": row["In_Stock"],
        "In_SOA": row["In_SOA"]
    }

def build_product_profile(product_id):

    profile = {
        "Product_ID": int(product_id)
    }

    # --------------------------------------------------
    # Product master
    # --------------------------------------------------

    product_row = dim_product[
        dim_product["Product_ID"] == product_id
    ]

    if not product_row.empty:
        row = product_row.iloc[0]

        profile["Product"] = {
            "Product_Key": row["Product_Key"],
            "Description": row["Product_Description"],
            "Category": row["Product_Category"],
            "In_Sales": bool(row["In_Sales"]),
            "In_Stock": bool(row["In_Stock"]),
            "In_SOA": bool(row["In_SOA"])
        }

    # --------------------------------------------------
    # Sales
    # --------------------------------------------------

    sales_rows = fact_sales[
        fact_sales["Product_ID"] == product_id
    ]

    if not sales_rows.empty:

        profile["Sales"] = {
            "Records": int(len(sales_rows)),
            "Units_Sold": float(
                sales_rows["Sold Period"].fillna(0).sum()
            ),
            "Revenue": float(
                sales_rows["Sales Value"].fillna(0).sum()
            ),
            "Profit": float(
                sales_rows["Profit"].fillna(0).sum()
            )
        }

    else:
        profile["Sales"] = None

    # --------------------------------------------------
    # Stock
    # --------------------------------------------------

    stock_rows = fact_stock[
        fact_stock["Product_ID"] == product_id
    ]

    if not stock_rows.empty:

        profile["Stock"] = {
            "Total_Quantity": float(
                stock_rows["Quantity"].fillna(0).sum()
            ),

            "Stores": stock_rows[
                [
                    "Store",
                    "Quantity",
                    "Stock_Status",
                    "Outstanding_Order_Qty"
                ]
            ].to_dict("records")
        }

    else:
        profile["Stock"] = None

    # --------------------------------------------------
    # SOA
    # --------------------------------------------------

    soa_rows = fact_soa[
        fact_soa["Product_ID"] == product_id
    ]

    if not soa_rows.empty:

        profile["SOA"] = soa_rows[
            [
                "Model",
                "Starts",
                "Ends",
                "Window_Days",
                "SOA"
            ]
        ].to_dict("records")

    else:
        profile["SOA"] = None

    # --------------------------------------------------
    # Inventory intelligence
    # --------------------------------------------------

    inv_rows = inventory_decision[
        inventory_decision["Product_ID"] == product_id
    ]

    if not inv_rows.empty:

        profile["Inventory_Intelligence"] = inv_rows[
            [
                "Store",
                "ABC_Class",
                "Velocity_Band",
                "Demand_Status",
                "Stock_Band",
                "Reorder_Recommendation",
                "Slow_Mover_Action",
                "Inventory_Decision",
                "Decision_Priority",
                "Inventory_Segment"
            ]
        ].to_dict("records")

    else:
        profile["Inventory_Intelligence"] = None

    return profile

def generate_product_summary(profile):

    product = profile.get("Product", {})
    sales = profile.get("Sales")
    stock = profile.get("Stock")
    soa = profile.get("SOA")
    inventory = profile.get("Inventory_Intelligence")

    lines = []

    # Product identity
    lines.append(
        f"{product.get('Description')} "
        f"({product.get('Product_Key')}) "
        f"is in the {product.get('Category')} category."
    )

    # Sales
    if sales:
        lines.append(
            f"It has sold {sales['Units_Sold']:.0f} unit(s), "
            f"generating £{sales['Revenue']:.2f} in revenue "
            f"and £{sales['Profit']:.2f} in profit."
        )
    else:
        lines.append(
            "No governed sales information is available for this product."
        )

    # Stock
    if stock:
        lines.append(
            f"Total stock in the saved dataset is "
            f"{stock['Total_Quantity']:.0f} unit(s)."
        )
    else:
        lines.append(
            "No governed stock information is available for this product."
        )

    # SOA
    if soa:
        lines.append(
            f"{len(soa)} SOA record(s) are available for this product."
        )
    else:
        lines.append(
            "No governed SOA information is available for this product."
        )

    # Inventory intelligence
    if inventory:
        lines.append(
            "Inventory intelligence recommendations are available."
        )
    else:
        lines.append(
            "No inventory intelligence recommendation is available."
        )

    return " ".join(lines)

fact_soa["Starts"] = pd.to_datetime(
    fact_soa["Starts"],
    dayfirst=True,
    errors="coerce"
)

fact_soa["Ends"] = pd.to_datetime(
    fact_soa["Ends"],
    dayfirst=True,
    errors="coerce"
)

def active_soa(as_of_date=None):

    if as_of_date is None:
        as_of_date = pd.Timestamp.today().normalize()
    else:
        as_of_date = pd.to_datetime(as_of_date)

    return fact_soa[
        (fact_soa["Starts"] <= as_of_date)
        &
        (fact_soa["Ends"] >= as_of_date)
    ].copy()

NON_MERCHANDISE_CATEGORIES = [
    "INSTALLATION",
    "DELIVERY CHARGE",
    "MISC"
]

merchandise_sales = fact_sales[
    ~fact_sales["Category"].isin(NON_MERCHANDISE_CATEGORIES)
].copy()

def top_selling_products(n=10):

    df = merchandise_sales[
        merchandise_sales["Transaction_Status"]
        == "POSITIVE_SALES_ACTIVITY"
    ]

    return (
        df.groupby(
            ["Product_ID", "Stock Code", "Description", "Category"],
            dropna=False
        )["Sold Period"]
        .sum()
        .reset_index()
        .sort_values("Sold Period", ascending=False)
        .head(n)
    )

def top_revenue_products(n=10):

    return (
        merchandise_sales.groupby(
            ["Product_ID", "Stock Code", "Description", "Category"],
            dropna=False
        )["Sales Value"]
        .sum()
        .reset_index()
        .sort_values("Sales Value", ascending=False)
        .head(n)
    )

def top_profit_products(n=10):

    return (
        merchandise_sales.groupby(
            ["Product_ID", "Stock Code", "Description", "Category"],
            dropna=False
        )["Profit"]
        .sum()
        .reset_index()
        .sort_values("Profit", ascending=False)
        .head(n)
    )

def reorder_candidates():

    return inventory_decision[
        inventory_decision["Reorder_Recommendation"].isin(
            [
                "REORDER",
                "REORDER - HIGH PRIORITY"
            ]
        )
    ].copy()

def high_priority_reorders():

    return inventory_decision[
        inventory_decision["Reorder_Recommendation"]
        == "REORDER - HIGH PRIORITY"
    ].copy()

def slow_movers():

    return inventory_decision[
        inventory_decision["Slow_Mover_Action"]
        == "SLOW MOVER REVIEW"
    ].copy()

def route_query(question):

    q = question.lower().strip()

    # --------------------------------------------------
    # Product lookup
    # --------------------------------------------------

    if any(term in q for term in [
        "model",
        "product lookup",
        "product details",
        "product information"
    ]):
        return "product_lookup"

    # --------------------------------------------------
    # Sales
    # --------------------------------------------------

    if any(term in q for term in [
        "top selling",
        "best selling",
        "most sold",
        "highest selling"
    ]):
        return "top_selling"

    if any(term in q for term in [
        "highest revenue",
        "top revenue",
        "most revenue"
    ]):
        return "top_revenue"

    if any(term in q for term in [
        "highest profit",
        "top profit",
        "most profitable product"
    ]):
        return "top_profit"

    if any(term in q for term in [
        "category performance",
        "best category",
        "category revenue"
    ]):
        return "category_performance"

    # --------------------------------------------------
    # Inventory
    # --------------------------------------------------

    if any(term in q for term in [
        "high priority reorder",
        "urgent reorder"
    ]):
        return "high_priority_reorder"

    if any(term in q for term in [
        "reorder",
        "replenish",
        "needs stock"
    ]):
        return "reorder"

    if any(term in q for term in [
        "slow mover",
        "slow moving",
        "slow stock"
    ]):
        return "slow_mover"

    # --------------------------------------------------
    # SOA
    # --------------------------------------------------

    if any(term in q for term in [
        "active soa",
        "current soa"
    ]):
        return "active_soa"

    return "unsupported"

def execute_query(question, n=10):

    intent = route_query(question)

    if intent == "top_selling":
        return top_selling_products(n)

    if intent == "top_revenue":
        return top_revenue_products(n)

    if intent == "top_profit":
        return top_profit_products(n)

    if intent == "category_performance":
        return category_performance()

    if intent == "reorder":
        return reorder_candidates()

    if intent == "high_priority_reorder":
        return high_priority_reorders()

    if intent == "slow_mover":
        return slow_movers()

    if intent == "active_soa":
        return active_soa()

    if intent == "product_lookup":
        return (
            "Product lookup detected. "
            "A model number is required."
        )

    return (
        "This question is not currently supported by "
        "the governed AI question set."
    )

def format_top_selling(df, n=5):

    if df.empty:
        return "No selling-product records are available."

    lines = ["Top-selling products:"]

    for i, row in df.head(n).iterrows():
        lines.append(
            f"- {row['Description']} "
            f"({row['Stock Code']}): "
            f"{int(row['Sold Period'])} units"
        )

    return "\n".join(lines)

def format_top_revenue(df, n=5):

    if df.empty:
        return "No revenue records are available."

    lines = ["Highest-revenue products:"]

    for i, row in df.head(n).iterrows():
        lines.append(
            f"- {row['Description']} "
            f"({row['Stock Code']}): "
            f"£{row['Sales Value']:.2f}"
        )

    return "\n".join(lines)

def format_top_profit(df, n=5):

    if df.empty:
        return "No profit records are available."

    lines = ["Highest-profit products:"]

    for i, row in df.head(n).iterrows():
        lines.append(
            f"- {row['Description']} "
            f"({row['Stock Code']}): "
            f"£{row['Profit']:.2f}"
        )

    return "\n".join(lines)

def format_reorders(df, n=10):

    if df.empty:
        return "No reorder candidates are currently available."

    lines = [
        f"{len(df)} reorder candidate(s) found."
    ]

    for _, row in df.head(n).iterrows():

        lines.append(
            f"- {row['Description']} | "
            f"{row['Store']} | "
            f"{row['Reorder_Recommendation']}"
        )

    return "\n".join(lines)

def format_slow_movers(df, n=10):

    if df.empty:
        return "No slow-moving products are currently flagged."

    lines = [
        f"{len(df)} slow-mover record(s) found."
    ]

    for _, row in df.head(n).iterrows():

        lines.append(
            f"- {row['Description']} | "
            f"{row['Store']} | "
            f"{row['Slow_Mover_Action']}"
        )

    return "\n".join(lines)

def format_active_soa(df, n=10):

    if df.empty:
        return "No active SOA records were found."

    lines = [
        f"{len(df)} active SOA record(s) found."
    ]

    for _, row in df.head(n).iterrows():

        lines.append(
            f"- {row['Description']} "
            f"({row['Model']}): "
            f"SOA £{row['SOA']:.2f}, "
            f"valid {row['Starts'].date()} "
            f"to {row['Ends'].date()}"
        )

    return "\n".join(lines)

def category_performance():
    return (merchandise_sales.groupby("Category", dropna=False)[["Sales Value", "Profit"]]
            .sum().sort_values("Sales Value", ascending=False).reset_index())


def retail_assistant(question, n=5):

    intent = route_query(question)

    if intent == "category_performance":
        rows = category_performance().head(n)
        return "Category performance (saved merchandise sales):\n" + "\n".join(
            f"- {row['Category']}: revenue {row['Sales Value']:,.2f}; profit {row['Profit']:,.2f}"
            for _, row in rows.iterrows()
        )

    if intent == "top_selling":
        return format_top_selling(
            top_selling_products(n),
            n
        )

    if intent == "top_revenue":
        return format_top_revenue(
            top_revenue_products(n),
            n
        )

    if intent == "top_profit":
        return format_top_profit(
            top_profit_products(n),
            n
        )

    if intent == "reorder":
        return format_reorders(
            reorder_candidates(),
            n
        )

    if intent == "high_priority_reorder":
        return format_reorders(
            high_priority_reorders(),
            n
        )

    if intent == "slow_mover":
        return format_slow_movers(
            slow_movers(),
            n
        )

    if intent == "active_soa":
        return format_active_soa(
            active_soa(),
            n
        )

    if intent == "product_lookup":
        return (
            "Please provide a product model number "
            "for the product lookup."
        )

    return (
        "This question is not supported by the current "
        "governed AI question set."
    )

source_metadata = {
    "top_selling": {
        "source": "fact_sales.csv",
        "layer": "Governed Sales Layer"
    },

    "top_revenue": {
        "source": "fact_sales.csv",
        "layer": "Governed Sales Layer"
    },

    "top_profit": {
        "source": "fact_sales.csv",
        "layer": "Governed Sales Layer"
    },

    "category_performance": {
        "source": "fact_sales.csv",
        "layer": "Governed Sales Layer"
    },

    "reorder": {
        "source": "inventory_decision_layer.csv",
        "layer": "Phase 5 Inventory Intelligence"
    },

    "high_priority_reorder": {
        "source": "inventory_decision_layer.csv",
        "layer": "Phase 5 Inventory Intelligence"
    },

    "slow_mover": {
        "source": "inventory_decision_layer.csv",
        "layer": "Phase 5 Inventory Intelligence"
    },

    "active_soa": {
        "source": "fact_soa.csv",
        "layer": "Governed SOA Layer"
    },

    "product_lookup": {
        "source": "dim_product.csv",
        "layer": "Governed Product Master"
    }
}

def get_source_metadata(intent):

    metadata = source_metadata.get(intent)

    if metadata is None:
        return None

    return {
        "Source": metadata["source"],
        "Layer": metadata["layer"],
        "Retrieved_At": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

def retail_assistant_with_metadata(question, n=5):

    intent = route_query(question)

    answer = retail_assistant(
        question,
        n=n
    )

    metadata = get_source_metadata(intent)

    if metadata is None:
        return answer

    metadata_text = (
        "\n\n"
        f"Source: {metadata['Source']}\n"
        f"Layer: {metadata['Layer']}\n"
        f"Retrieved: {metadata['Retrieved_At']}\n"
        f"Intent: {intent}"
    )

    return answer + metadata_text
