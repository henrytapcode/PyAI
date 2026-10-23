# Settings without shared state

**What it shows:** the safe default-argument pattern in a realistic job: model settings made from defaults plus optional overrides.

**Step by step**
1. Line 2 holds the default settings.
2. Line 5 gives `overrides` a default of `None`, not `{}`. The hint `dict[...] | None` says the same thing.
3. Line 6 copies `DEFAULTS` with `dict(DEFAULTS)`, so changing the copy never changes the original.
4. Lines 7–8 apply the overrides with `update` only when the caller passed some. `update` adds or replaces keys in the dict.
5. Lines 12–17 build two settings and show that they are separate and that `DEFAULTS` is untouched.

**Notice:** if line 5 said `overrides={}` and line 6 returned that same dict, `B006` would warn you. The bug would be real: one call could change the settings of every later call.

**Try it yourself:** change line 12 to `build_settings({"model": "big"})`. Line 14 should show `'model': 'big'`, and line 15 should still show `'model': 'small'`.
