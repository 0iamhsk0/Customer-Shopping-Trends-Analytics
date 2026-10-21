from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).resolve().parent / "customer_shopping_trends.csv"


def load_shopping_data(csv_path: str | Path | None = None) -> pd.DataFrame:
    """Load and normalize the customer shopping dataset."""
    path = Path(csv_path) if csv_path else DATA_FILE
    df = pd.read_csv(path)

    # Handle BOM / stray whitespace in headers.
    df.columns = [col.strip().replace("\ufeff", "") for col in df.columns]

    # Normalize numeric fields.
    if "Purchase Amount (USD)" in df.columns:
        df["Purchase Amount (USD)"] = pd.to_numeric(
            df["Purchase Amount (USD)"], errors="coerce"
        )
    if "Review Rating" in df.columns:
        df["Review Rating"] = pd.to_numeric(df["Review Rating"], errors="coerce")

    # Fill missing values for simple analysis.
    for col in ["Shipping Type", "Subscription Status", "Category", "Gender", "Location"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    if "Age" in df.columns:
        df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

    return df


def age_group_label(age: float) -> str:
    if pd.isna(age):
        return "Unknown"
    if age < 25:
        return "18-24"
    if age < 35:
        return "25-34"
    if age < 45:
        return "35-44"
    if age < 55:
        return "45-54"
    if age < 65:
        return "55-64"
    return "65+"


def add_age_group(df: pd.DataFrame) -> pd.DataFrame:
    if "Age" in df.columns:
        df = df.copy()
        df["Age Group"] = df["Age"].apply(age_group_label)
    return df
