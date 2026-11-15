# Ticket extractor from customer emails

**What it shows:** Requesting schema-guided JSON from `FakeLLM`, checking keys and types, and building a validated `Ticket` dataclass while rejecting fake empty values.

**Step by step**
1. Lines 7–15 define `TICKET_SCHEMA` requiring `name` (`string`), `order_id` (`integer`), and `urgent` (`boolean`).
2. Lines 18–29 define the `Ticket` dataclass with `__post_init__` business checks that reject blank names and non-positive order IDs.
3. Lines 32–49 define `validate_ticket_dict()` to catch missing required keys and wrong types (checking `bool` before `int`).
4. Lines 59–74 loop over three customer emails, parse JSON, validate the dict, and either print the constructed `Ticket` or print why it was rejected.

**Notice:** Email 2 produces valid JSON (`{"name": "", "order_id": 0, "urgent": false}`) that passes type checks, so only the business check in `Ticket.__post_init__` catches that the email lacked ticket details.

**Try it yourself:** Change Email 2 to `"name: Hoa, order_id: 99, urgent: yes"` and run again to see all three emails succeed.
