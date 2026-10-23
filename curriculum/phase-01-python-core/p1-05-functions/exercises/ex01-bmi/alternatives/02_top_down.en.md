# Check from the top down

Here `bmi` uses a named step (`height_squared`), which makes the formula easy to read aloud. `bmi_category` checks the limits from the **largest** down (`>= 30`, `>= 25`, `>= 18.5`) and ends with the leftover case. Because each `return` ends the function, the order of the checks is what makes it correct: swap them and `35` would be called "normal".
