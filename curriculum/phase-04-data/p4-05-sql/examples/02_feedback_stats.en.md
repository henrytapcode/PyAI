# Model feedback summary with GROUP BY and HAVING

**What it shows:** aggregating user ratings per model with `AVG` and `COUNT(*)`, filtering out small sample groups with `HAVING`, and rounding averages to 2 decimal places.

**Step by step**
1. Lines 4–11 create a `feedback` table with `model` and `rating` columns.
2. Lines 13–26 insert seven ratings across four models inside `with conn:`.
3. Lines 28–37 group rows by `model`, keep only models with `COUNT(*) >= 2`, round `AVG(rating)` to 2 decimals, and sort by `avg_rating DESC, model ASC`.
4. Lines 39–42 print each surviving model's rounded average and rating count, then close the connection.

**Notice:** `local-7b` only has 1 rating, so `HAVING COUNT(*) >= 2` excludes it *after* grouping, and `model ASC` breaks the 4.5 tie between `claude` and `gpt-4o`.

**Try it yourself:** add another rating `("local-7b", 5)` to `rows` and see where `local-7b` lands in the output.
