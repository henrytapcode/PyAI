import pytest
from exercise import DEFAULT_SYSTEM, REFUSAL, ChatBot
from pyai_llm import FakeLLM, count_tokens


class SpyClient:
    def __init__(self, embed_dim: int = 256, script: list[str] | None = None) -> None:
        self._inner = FakeLLM(embed_dim=embed_dim, script=script)
        self.embed_calls = 0
        self.embed_batch_sizes: list[int] = []
        self.chat_calls = 0
        self.last_messages: list[dict] | None = None
        self.chat_kwargs: list[dict] = []

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.embed_calls += 1
        self.embed_batch_sizes.append(len(texts))
        return self._inner.embed(texts)

    def chat(self, messages: list[dict], *args, **kwargs):
        self.chat_calls += 1
        self.last_messages = [dict(msg) for msg in messages]
        recorded = dict(kwargs)
        if args:
            recorded["temperature"] = args[0]
        self.chat_kwargs.append(recorded)
        return self._inner.chat(messages, *args, **kwargs)


@pytest.fixture
def faq_docs() -> list[dict]:
    return [
        {
            "source": "refunds.md",
            "text": (
                "Refunds are issued within 30 days of purchase. "
                "Keep your original receipt for any return. "
                "Opened software is not eligible for a refund."
            ),
        },
        {
            "source": "shipping.md",
            "text": (
                "Standard shipping takes 5 business days across the country. "
                "Express delivery arrives next day for 12 dollars. "
                "Free shipping applies on orders over 50 dollars."
            ),
        },
        {
            "source": "warranty.md",
            "text": (
                "Hardware warranty covers factory defects for 12 months. "
                "Water damage and dropped screens are not covered. "
                "Battery wear after 6 months is excluded."
            ),
        },
        {
            "source": "payment.md",
            "text": (
                "Accepted payment methods are Visa, Mastercard, and cash on delivery. "
                "Gift cards cannot be redeemed for cash. "
                "Invoices are emailed right after checkout."
            ),
        },
        {
            "source": "accounts.md",
            "text": (
                "Password resets are sent by email within 5 minutes. "
                "Two-factor login can be turned on in security settings. "
                "Inactive accounts remain open for 24 months."
            ),
        },
        {
            "source": "support.md",
            "text": (
                "Support agents work Monday to Friday from 9 AM to 6 PM. "
                "Weekend messages receive replies on Monday morning. "
                "Urgent outage tickets get a 2 hour target."
            ),
        },
        {
            "source": "pickup.md",
            "text": (
                "Store pickup is ready 2 hours after order confirmation. "
                "Unclaimed orders are held at the counter for 7 days. "
                "Bring a photo ID at pickup."
            ),
        },
        {
            "source": "discounts.md",
            "text": (
                "Student discounts give 15 percent off eligible laptops. "
                "Promo codes cannot be combined on one order. "
                "Loyalty points expire after 12 months."
            ),
        },
    ]


def test_faq_question_returns_expected_source_and_citation(faq_docs):
    bot = ChatBot(faq_docs, SpyClient())
    res = bot.ask("  How many days are refunds issued within?  ")
    assert isinstance(res, dict)
    assert res["rewritten"] == "How many days are refunds issued within?"
    assert res["sources"] == ["refunds.md"]
    assert "[1]" in res["answer"]
    assert res["answer"] != REFUSAL


def test_out_of_faq_refuses_without_calling_chat(faq_docs):
    spy = SpyClient()
    bot = ChatBot(faq_docs, spy)
    res = bot.ask("Do you offer cryptocurrency billing?")
    assert isinstance(res, dict)
    assert res["answer"] == REFUSAL
    assert res["sources"] == []
    assert spy.chat_calls == 0, "out-of-scope queries must refuse before calling client.chat"
    assert len(bot.history) == 2, "refused turns must still be recorded in history"


def test_chat_called_once_with_temperature_zero_on_hit(faq_docs):
    spy = SpyClient()
    bot = ChatBot(faq_docs, spy)
    res = bot.ask("How many days are refunds issued within?")
    assert res["sources"] == ["refunds.md"]
    assert spy.chat_calls == 1
    assert spy.chat_kwargs == [{"temperature": 0.0}], (
        "chat must be called once with temperature=0.0 when retrieval returns hits"
    )


def test_followup_what_about_express_rewrites_and_returns_shipping(faq_docs):
    bot = ChatBot(faq_docs, SpyClient())
    # Turn 1 is refused by FakeLLM, yet still enters history for turn 2 rewriting
    bot.ask("How much does delivery cost?")
    res = bot.ask("What about express?")
    assert isinstance(res, dict)
    assert res["rewritten"] == "How much does delivery cost? What about express?"
    assert res["sources"] == ["shipping.md"]
    assert "Express delivery" in res["answer"]


def test_consecutive_followups_rewrite_from_original_user_question(faq_docs):
    bot = ChatBot(faq_docs, SpyClient())
    # Turn 1 is refused, yet still enters history as the original user question
    bot.ask("How much does delivery cost?")
    r2 = bot.ask("What about express?")
    r3 = bot.ask("And free shipping?")
    assert isinstance(r2, dict) and isinstance(r3, dict)
    assert r2["rewritten"] == "How much does delivery cost? What about express?"
    assert r3["rewritten"] == "What about express? And free shipping?", (
        "follow-up rewriting must use the original previous user question, not the rewritten query"
    )
    assert r3["sources"] == ["shipping.md"]


def test_long_standalone_and_android_prefix_are_not_rewritten(faq_docs):
    bot = ChatBot(faq_docs, SpyClient())
    bot.ask("How long are store pickup orders held?")
    r_android = bot.ask("Android app discounts apply on laptops?")
    r_long = bot.ask("How long is hardware warranty for factory defects?")
    assert isinstance(r_android, dict) and isinstance(r_long, dict)
    assert r_android["rewritten"] == "Android app discounts apply on laptops?", (
        "words starting with 'and' like 'Android' must not trigger follow-up rewriting"
    )
    assert r_long["rewritten"] == "How long is hardware warranty for factory defects?"


def test_long_questions_with_followup_prefixes_are_rewritten(faq_docs):
    bot = ChatBot(faq_docs, SpyClient())
    bot.ask("How long are store pickup orders held?")
    r_what_about = bot.ask("What about the photo ID needed at the counter?")
    r_how_about = bot.ask("How about unclaimed orders after order confirmation?")
    r_and = bot.ask("And does express delivery arrive the next day?")
    assert r_what_about["rewritten"] == (
        "How long are store pickup orders held? What about the photo ID needed at the counter?"
    )
    assert r_what_about["sources"] == ["pickup.md"]
    assert r_how_about["rewritten"] == (
        "What about the photo ID needed at the counter? "
        "How about unclaimed orders after order confirmation?"
    )
    assert r_and["rewritten"] == (
        "How about unclaimed orders after order confirmation? "
        "And does express delivery arrive the next day?"
    )


def test_followup_prefix_matching_is_case_insensitive(faq_docs):
    bot = ChatBot(faq_docs, SpyClient())
    bot.ask("How long are store pickup orders held?")
    r_what = bot.ask("WHAT ABOUT the photo ID needed at the counter?")
    r_and = bot.ask("AND is a photo ID required at pickup?")
    assert r_what["rewritten"] == (
        "How long are store pickup orders held? WHAT ABOUT the photo ID needed at the counter?"
    )
    assert r_and["rewritten"] == (
        "WHAT ABOUT the photo ID needed at the counter? AND is a photo ID required at pickup?"
    )
    assert r_and["sources"] == ["pickup.md"]


def test_trims_oldest_turns_within_token_budget_and_pins_system(faq_docs):
    spy = SpyClient()
    bot = ChatBot(faq_docs, spy, max_history_tokens=50)
    bot.ask("How many days are refunds issued within?")
    bot.ask("How long does standard shipping take?")
    bot.ask("When do support messages get replies?")
    total_tokens = count_tokens(DEFAULT_SYSTEM) + sum(
        count_tokens(msg["content"]) for msg in bot.history
    )
    assert len(bot.history) >= 2
    assert len(bot.history) < 6, "oldest turns must be evicted once budget is exceeded"
    assert total_tokens <= 50, "system prompt plus kept history must stay within max_history_tokens"
    assert spy.last_messages is not None
    assert spy.last_messages[0]["role"] == "system", "system prompt must stay pinned at index 0"
    assert spy.last_messages[0]["content"].startswith(DEFAULT_SYSTEM)


def test_invalid_and_duplicate_citations_are_filtered_preserving_order(faq_docs):
    spy = SpyClient(
        script=["See details [2], bad [9], zero [0], repeat [2], and first [1]."]
    )
    bot = ChatBot(faq_docs, spy, k=2)
    res = bot.ask("How many days are refunds issued within?")
    assert isinstance(res, dict)
    assert res["sources"] == ["payment.md", "refunds.md"], (
        "sources must keep only unique valid [n] citations in appearance order"
    )
    assert res["answer"] == "See details [2], bad [9], zero [0], repeat [2], and first [1]."


def test_separate_bots_isolate_history_and_embed_docs_once(faq_docs):
    spy = SpyClient()
    bot_a = ChatBot(faq_docs, spy)
    bot_b = ChatBot(faq_docs, spy)
    assert spy.embed_calls == 2, "each ChatBot should embed chunks exactly once in __init__"
    assert spy.embed_batch_sizes == [24, 24]
    bot_a.ask("How long does standard shipping take?")
    assert len(bot_a.history) == 2
    assert bot_b.history == [], "separate ChatBot instances must not share history"
    assert spy.embed_calls == 3, "ask should only embed the user query"


@pytest.mark.parametrize("bad_question", ["", "   ", "\n\t  "])
def test_empty_or_whitespace_question_raises_value_error(faq_docs, bad_question):
    bot = ChatBot(faq_docs, SpyClient())
    with pytest.raises(ValueError):
        bot.ask(bad_question)


def test_tiny_token_budget_keeps_latest_turn_pair(faq_docs):
    bot = ChatBot(faq_docs, SpyClient(), max_history_tokens=5)
    bot.ask("How many days are refunds issued within?")
    r2 = bot.ask("How long does standard shipping take?")
    assert isinstance(r2, dict)
    assert len(bot.history) == 2, (
        "even when budget is tiny, trimming must keep the latest user/assistant turn pair"
    )
    assert bot.history == [
        {"role": "user", "content": "How long does standard shipping take?"},
        {"role": "assistant", "content": r2["answer"]},
    ]


def test_k_parameter_limits_retrieved_context_chunks(faq_docs):
    spy = SpyClient()
    bot = ChatBot(faq_docs, spy, k=1)
    bot.ask("How many days are refunds issued within?")
    assert spy.last_messages is not None
    system_content = spy.last_messages[0]["content"]
    assert "[1] " in system_content
    assert "[2] " not in system_content, "k=1 must include only [1] in system context, not [2]"
