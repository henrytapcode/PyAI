# Stop early inside a loop

Instead of slicing, walk through the words and add them to `kept` one by one. The moment `kept` already holds `limit` words and another word arrives, there is more text than fits, so return what you have plus `"..."`. If the loop ends without that happening, everything fitted. It is longer than the slice version, but the "stop as soon as it is too long" idea is useful when the input is huge or comes in one piece at a time.
