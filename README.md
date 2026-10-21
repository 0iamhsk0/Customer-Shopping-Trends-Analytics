import streamlit as st

from ai_layer import answer_question, summarize_kpis
from data_loader import load_shopping_data


@st.cache_data
def load_data():
    return load_shopping_data("customer_shopping_trends.csv")


st.set_page_config(page_title="Customer Shopping AI Insights", layout="wide")

st.title("🛍 Customer Shopping AI Insights")

with st.sidebar:
    st.header("Quick questions")
    sample_questions = [
        "Which category has the highest revenue?",
        "Which age group spends the most?",
        "What is the most popular shipping type?",
        "Summarize the main trends in this dataset",
        "What recommendations would you suggest?",
    ]
    for question in sample_questions:
        if st.button(question, use_container_width=True):
            st.session_state["question"] = question

    st.markdown("---")
    st.caption("This is a lightweight AI layer on top of the existing retailer dataset.")


df = load_data()
kpis = summarize_kpis(df)

col1, col2, col3 = st.columns(3)
col1.metric("Customers", f"{kpis['total_customers']}")
col2.metric("Revenue", f"${kpis['total_revenue']:.2f}")
col3.metric("Avg Sale", f"${kpis['avg_purchase_amount']:.2f}")

question = st.text_input(
    "Ask a business question",
    value=st.session_state.get("question", "Which category has the highest revenue?"),
    placeholder="Example: Which category has the highest revenue?"
)

if question:
    answer = answer_question(df, question)
    st.info(answer)

st.markdown("---")

st.subheader("Key Business Highlights")

st.write(f"- Top category: {kpis['top_category']} (${kpis['top_category_revenue']:.2f})")
st.write(f"- Top age group: {kpis['top_age_group']} (${kpis['top_age_group_revenue']:.2f})")
st.write(f"- Preferred shipping: {kpis['top_shipping_type']}")
st.write(f"- Subscription concentration: {kpis['top_subscription_status']} ({kpis['subscription_share_pct']}%)")
