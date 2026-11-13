# Normalise text classifier labels, drop blank texts and duplicates, and count labels.
import pandas as pd

dataset = pd.DataFrame({
    "text": [
        " Reset password ",
        "App crashes",
        "",
        "Reset password",
        "   ",
        "Login button broken",
        "Billing issue",
    ],
    "label": [
        " Account_Help ",
        "bug-report",
        "spam",
        "account_help",
        "billing",
        " BUG_REPORT",
        "BILLING",
    ],
})

df = dataset.copy()
df["text"] = df["text"].str.strip()
df["label"] = (
    df["label"]
    .str.strip()
    .str.lower()
    .str.replace("_", " ", regex=False)
    .str.replace("-", " ", regex=False)
)

df = df[df["text"] != ""]
df = df.drop_duplicates(subset=["text"], keep="last").reset_index(drop=True)

print("Clean dataset:")
print(df)
print("Label counts:")
print(df["label"].value_counts())
