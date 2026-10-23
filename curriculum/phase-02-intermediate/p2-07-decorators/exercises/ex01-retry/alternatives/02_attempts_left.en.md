# Count down the attempts left

A `while True` loop keeps a counter `attempts_left`. Each pass lowers it and tries the call. When the call raises and nothing is left, `raise error` passes the error on; otherwise the loop simply goes around again. It makes the "how many tries remain" idea very visible and also works if you later want to log each attempt, but you need to be careful that the loop always ends: if you forget to lower the counter, it never stops.
