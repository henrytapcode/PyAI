# Check first, then use

This version only uses `try` for the one thing that really can raise, `json.loads`. For everything else it checks the data before using it: `isinstance` asks "is this a dict?" and "is this a number?" (we preview it here, you will see it in later lessons), and `in` asks "does the key exist?". Checking first reads clearly and avoids `raise`, but the checks grow long when the data has many fields. The main solution is shorter because one `except` covers every kind of failure at once.
