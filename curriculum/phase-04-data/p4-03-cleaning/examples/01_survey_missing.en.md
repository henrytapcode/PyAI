# Cleaning a user survey with missing values

**What it shows:** counting missing cells per column, dropping rows missing a required key (`user`), and filling missing numeric scores with the column median.

**Step by step**
1. Lines 5–13 load an inline CSV survey into `df` using `pd.read_csv(io.StringIO(csv_text))`.
2. Lines 14–15 print `df.isna().sum()` so you see how many values are missing in each column (`user`: 1, `score`: 2).
3. Lines 17–19 drop the row with no `user`, reset the index, compute the median score (`4.0`), and fill missing `score` cells with it.
4. Lines 21–23 print the cleaned table and the final average score.

**Notice:** `dropna(subset=["user"])` runs before `median()` so a row without a valid user does not influence the fill value.

**Try it yourself:** change `cleaned["score"].median()` on line 18 to `cleaned["score"].mean()` and check whether the filled values change here.
