Prompts that come from users are messy: extra spaces, odd capital letters, and rows that are empty. Write `clean_prompts(prompts)`. Try to use a list comprehension. It returns a new list with every prompt cleaned, and the empty ones removed. Write your code inside the function and `return` the answer.

**Example**

| input | output |
|---|---|
| `["  Hello   WORLD ", "", "   ", "What IS AI?"]` | `["hello world", "what is ai?"]` |

**Rules**
- Make each prompt lowercase.
- Remove spaces at both ends, and squeeze any run of spaces, tabs or new lines inside the text into a single space.
- Drop prompts that are empty or contain only whitespace.
- Keep the original order, and keep duplicates.
- Do not change the list that was passed in. Return a new list.
