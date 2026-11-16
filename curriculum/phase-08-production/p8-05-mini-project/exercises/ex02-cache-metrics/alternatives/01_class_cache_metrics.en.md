# Separate TTLCache and MetricsTracker classes

**How it works:** Rather than storing a raw dictionary and record list directly inside `create_app`'s closure, this alternative delegates caching and metrics to two dedicated classes (`TTLCache` and `MetricsTracker`) instantiated once per factory call.

**When to choose it:** Separating cache expiration and metric aggregation into their own classes makes each piece easy to unit-test independently and swap out later (for example replacing `TTLCache` with a Redis client), at the cost of a bit more code than closure variables.
