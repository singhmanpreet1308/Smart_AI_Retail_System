import streamlit as st
import json
from pathlib import Path
from urllib.parse import urlparse

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Smart AI Retail Assistant",
    page_icon="🤖",
    layout="wide"
)

# =========================================================
# HEADER
# =========================================================

st.title("🤖 Smart AI Retail Assistant")

st.caption(
    "Grounded retail intelligence for sales, inventory, SOA, "
    "reorder decisions and product knowledge."
)

st.divider()

try:
    from retail_backend import (
        retail_assistant_with_metadata, lookup_product,
        build_product_profile, generate_product_summary,
    )
except (OSError, ValueError, KeyError) as exc:
    st.error(f"Unable to load the local retail datasets: {exc}")
    st.stop()

st.sidebar.caption("Local CSV and saved JSON data. No API calls or token usage.")
st.sidebar.caption("Figures reflect saved data, not a live stock feed.")

# =========================================================
# MODE SELECTOR
# =========================================================

mode = st.sidebar.radio(
    "Assistant Mode",
    [
        "Business Analytics",
        "Product Lookup",
        "Product Knowledge"
    ]
)

# =========================================================
# BUSINESS ANALYTICS
# =========================================================

if mode == "Business Analytics":

    st.subheader("Business Analytics Assistant")

    st.write(
        "Ask questions about sales, revenue, profit, inventory, "
        "reorder recommendations, slow movers and SOA."
    )

    st.caption("Examples: top selling products, highest revenue, highest profit, urgent reorder, slow movers, active SOA.")

    if "retail_messages" not in st.session_state:
        st.session_state.retail_messages = []
    for message in st.session_state.retail_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input(
        "Ask a retail business question..."
    )

    if question:

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            answer = retail_assistant_with_metadata(question)

            st.write(answer)
        st.session_state.retail_messages.extend([
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
        ])


# =========================================================
# PRODUCT LOOKUP
# =========================================================

elif mode == "Product Lookup":

    st.subheader("Product Retail Profile")

    model = st.text_input(
        "Enter Product Model Number",
        placeholder="Example: DV90DB8845"
    )

    if st.button("Search Product"):

        if not model.strip():
            st.warning("Enter a model number.")

        else:

            match = lookup_product(model)

            if match["status"] != "matched":

                st.error(
                    "Product could not be confidently matched."
                )
                if match.get("status") == "multiple_matches":
                    st.dataframe(match["matches"], hide_index=True)

            else:

                profile = build_product_profile(
                    match["Product_ID"]
                )

                product = profile["Product"]

                st.success(
                    f"{product['Description']} "
                    f"({product['Product_Key']})"
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Category",
                        product["Category"]
                    )

                with col2:
                    st.metric(
                        "Sales Data",
                        "Available"
                        if product["In_Sales"]
                        else "Unavailable"
                    )

                with col3:
                    st.metric(
                        "Stock Data",
                        "Available"
                        if product["In_Stock"]
                        else "Unavailable"
                    )

                st.divider()

                st.write(
                    generate_product_summary(profile)
                )
                for section in ["Sales", "Stock", "SOA", "Inventory_Intelligence"]:
                    if profile.get(section):
                        with st.expander(section.replace("_", " ")):
                            st.write(profile[section])


# =========================================================
# PRODUCT KNOWLEDGE
# =========================================================

elif mode == "Product Knowledge":

    st.subheader("Product Knowledge Assistant")

    st.write(
        "Look up saved product specifications by model number. "
        "These model-generated answers have not been independently verified."
    )

    model = st.text_input(
        "Product Model",
        placeholder="Example: 32LQ63006LA.AEK"
    )

    manufacturer = st.selectbox(
        "Manufacturer",
        [
            "Samsung",
            "LG",
            "Bosch",
            "Neff",
            "Miele",
            "Sony",
            "Ninja",
            "Shark",
            "Other"
        ]
    )

    if st.button("Load Saved Specifications"):

        if not model.strip():
            st.warning("Enter a product model.")

        else:

            path = Path(__file__).resolve().parent / "notebooks" / "Phase_8_AI Retail Assistant" / "euri_pilot_results.json"
            try:
                saved = json.loads(path.read_text(encoding="utf-8"))
                if not isinstance(saved, list):
                    raise ValueError("Expected a list of saved product results.")
            except (OSError, ValueError) as exc:
                st.error(f"Cannot load saved specifications: {exc}")
                st.stop()
            matches = [row for row in saved if isinstance(row, dict)
                       and str(row.get("requested_model", "")).strip().casefold() == model.strip().casefold()
                       and str(row.get("manufacturer", "")).strip().casefold() == manufacturer.casefold()]
            if len(matches) != 1:
                st.info("No unique saved result for this manufacturer and model. Check the exact model, including its suffix.")
                st.stop()
            saved_result = matches[0]
            result = saved_result.get("candidate_specs")
            if not isinstance(result, dict) or not result:
                st.warning("This saved request contains no usable specifications.")
                st.stop()

            if result.get("error"):

                st.error(
                    "Product specification retrieval failed."
                )

            else:

                st.warning("UNVERIFIED — saved model output; web-search grounding was not confirmed.")
                st.write(
                    f"Saved product: "
                    f"{result.get('product_name')}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Model",
                        result.get("official_model")
                        or result.get("requested_model")
                    )

                with col2:
                    st.metric(
                        "Model-reported confidence",
                        str(result.get("confidence") or "Unknown")
                    )

                with col3:
                    st.metric(
                        "Model-reported completeness",
                        str(result.get("data_completeness") or "Unknown")
                    )

                st.subheader("Specifications")

                st.json(result)

                source = result.get(
                    "primary_source_url"
                )

                if isinstance(source, str) and urlparse(source).scheme in {"http", "https"}:
                    st.link_button("Open candidate source (unverified)", source)
