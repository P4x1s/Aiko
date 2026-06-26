"""Token counting service for AI providers."""

# Approximate token counts per character for different languages
# English: ~4 chars per token, Chinese: ~1.5 chars per token
CHARS_PER_TOKEN = {
    "en": 4,
    "zh": 1.5,
    "default": 3,
}


def estimate_tokens(text: str) -> int:
    """Estimate token count from text."""
    # Simple heuristic: count Chinese chars vs English chars
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    total_chars = len(text)
    english_chars = total_chars - chinese_chars

    chinese_tokens = chinese_chars / CHARS_PER_TOKEN["zh"]
    english_tokens = english_chars / CHARS_PER_TOKEN["en"]

    return int(chinese_tokens + english_tokens) + 1  # +1 for message overhead


def count_message_tokens(messages: list[dict]) -> int:
    """Count tokens in a list of messages."""
    total = 0
    for msg in messages:
        content = msg.get("content", "")
        total += estimate_tokens(content)
        total += 4  # message framing tokens
    total += 2  # reply priming
    return total


# Pricing per 1K tokens (in CNY)
MODEL_PRICING = {
    # OpenAI
    "gpt-4": {"input": 0.21, "output": 0.42},
    "gpt-4-turbo": {"input": 0.07, "output": 0.21},
    "gpt-4o": {"input": 0.035, "output": 0.105},
    "gpt-4o-mini": {"input": 0.0035, "output": 0.014},
    "gpt-3.5-turbo": {"input": 0.0035, "output": 0.007},
    # Anthropic
    "claude-3-opus": {"input": 0.105, "output": 0.525},
    "claude-3-opus-20240229": {"input": 0.105, "output": 0.525},
    "claude-3-sonnet": {"input": 0.021, "output": 0.105},
    "claude-3-sonnet-20240229": {"input": 0.021, "output": 0.105},
    "claude-3-haiku": {"input": 0.00175, "output": 0.00875},
    "claude-3-haiku-20240307": {"input": 0.00175, "output": 0.00875},
    # Google
    "gemini-pro": {"input": 0.0035, "output": 0.0105},
    "gemini-1.5-pro": {"input": 0.035, "output": 0.105},
    "gemini-1.5-flash": {"input": 0.0035, "output": 0.0105},
}


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate cost in CNY for a request."""
    pricing = MODEL_PRICING.get(model, {"input": 0.01, "output": 0.03})
    input_cost = (input_tokens / 1000) * pricing["input"]
    output_cost = (output_tokens / 1000) * pricing["output"]
    return round(input_cost + output_cost, 6)
