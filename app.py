from __future__ import annotations

from typing import Any, Dict

import pandas as pd

from data_loader import add_age_group, load_shopping_data


def summarize_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute a compact metrics summary for business use."""
    df = add_age_group(df)

    total_customers = int(df.shape[0])
    total_revenue = round(float(df["Purchase Amount (USD)"].sum()), 2)
    avg_purchase = round(float(df["Purchase Amount (USD)"].mean()), 2)
    avg_rating = round(float(df["Review Rating"].mean()), 2)

    category_revenue = (
        df.groupby("Category", dropna=False)["Purchase Amount (USD)"].sum().sort_values(ascending=False)
    )
    top_category = category_revenue.index[0] if not category_revenue.empty else "N/A"
    top_category_value = round(float(category_revenue.iloc[0]), 2) if not category_revenue.empty else 0.0

    age_revenue = (
        df.groupby("Age Group", dropna=False)["Purchase Amount (USD)"].sum().sort_values(ascending=False)
    )
    top_age_group = age_revenue.index[0] if not age_revenue.empty else "N/A"
    top_age_group_value = round(float(age_revenue.iloc[0]), 2) if not age_revenue.empty else 0.0

    shipping_pref = (
        df["Shipping Type"].value_counts().sort_values(ascending=False)
    )
    top_shipping = shipping_pref.index[0] if not shipping_pref.empty else "N/A"

    subscription = df["Subscription Status"].value_counts(normalize=True) if "Subscription Status" in df.columns else pd.Series({"Unknown": 1.0})
    sub_label = subscription.index[0] if not subscription.empty else "N/A"
    sub_share = round(float(subscription.iloc[0] * 100), 1) if not subscription.empty else 0.0

    return {
        "total_customers": total_customers,
        "total_revenue": total_revenue,
        "avg_purchase_amount": avg_purchase,
        "avg_review_rating": avg_rating,
        "top_category": top_category,
        "top_category_revenue": top_category_value,
        "top_age_group": top_age_group,
        "top_age_group_revenue": top_age_group_value,
        "top_shipping_type": top_shipping,
        "top_subscription_status": sub_label,
        "subscription_share_pct": sub_share,
    }


def generate_business_summary(df: pd.DataFrame) -> str:
    kpis = summarize_kpis(df)
    return (
        f"This dataset contains {kpis['total_customers']} customers with total revenue of ${kpis['total_revenue']:.2f}. "
        f"Average purchase amount is ${kpis['avg_purchase_amount']:.2f}, and the average review rating is {kpis['avg_review_rating']:.2f}. "
        f"The strongest category is {kpis['top_category']} with ${kpis['top_category_revenue']:.2f} in sales. "
        f"The highest-spending age group is {kpis['top_age_group']} with ${kpis['top_age_group_revenue']:.2f}. "
        f"Most customers prefer {kpis['top_shipping_type']} shipping, and {kpis['top_subscription_status']} accounts for {kpis['subscription_share_pct']}% of the customer base."
    )


def answer_question(df: pd.DataFrame, question: str) -> str:
    """Answer a small set of business questions from the dataset."""
    q = question.lower().strip()
    df = add_age_group(df)

    if not q:
        return "Please ask a question about revenue, category, age group, subscription, shipping, or trends."

    if any(word in q for word in ["trend", "summary", "overview", "insight"]):
        return generate_business_summary(df)

    if "category" in q and ("revenue" in q or "sales" in q or "spend" in q):
        revenue = df.groupby("Category")["Purchase Amount (USD)"].sum().sort_values(ascending=False)
        top = revenue.iloc[0]
        cat = revenue.index[0]
        return f"{cat} generates the most revenue, totaling ${float(top):.2f}."

    if "age" in q and ("spend" in q or "revenue" in q or "purchase" in q):
        revenue = df.groupby("Age Group")["Purchase Amount (USD)"].sum().sort_values(ascending=False)
        top = revenue.iloc[0]
        group = revenue.index[0]
        return f"{group} has the highest total spending, with ${float(top):.2f}."

    if "subscription" in q:
        status = df["Subscription Status"].value_counts(normalize=True)
        label = status.index[0]
        pct = round(float(status.iloc[0] * 100), 1)
        return f"The most common subscription status is {label}, accounting for {pct}% of customers."

    if "shipping" in q:
        shipping = df["Shipping Type"].value_counts().sort_values(ascending=False)
        label = shipping.index[0]
        count = int(shipping.iloc[0])
        return f"The most preferred shipping method is {label}, used by {count} customers."

    if "category" in q:
        counts = df["Category"].value_counts().sort_values(ascending=False)
        top_cat = counts.index[0]
        return f"The most common category is {top_cat}."

    if "recommend" in q or "should" in q:
        kpis = summarize_kpis(df)
        return (
            f"Recommendation: focus on {kpis['top_category']} and target the {kpis['top_age_group']} cohort. "
            f"The strongest growth opportunity is to increase engagement among the most active customer segment while improving the {kpis['top_shipping_type']} shipping experience."
        )

    return "I can answer questions about revenue, age groups, categories, subscriptions, shipping, and overall trends."
