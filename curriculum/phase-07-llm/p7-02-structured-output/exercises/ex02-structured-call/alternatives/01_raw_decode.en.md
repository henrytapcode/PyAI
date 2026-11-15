# Using json.JSONDecoder().raw_decode

This approach uses `json.JSONDecoder().raw_decode(text, start)` starting at the first `{` instead of slicing up to the last `}`. It stops automatically as soon as the first complete JSON object finishes, so trailing notes containing extra `{` or `}` characters (for example `"Note: {see FAQ}"` after the JSON) do not break parsing. It is the better choice whenever the model adds chatter after the JSON block, though it still assumes the first `{` in the text begins the target object rather than an earlier prose example.
