"""C4a LLM provider layer (owner B): free-tier chain Groq -> Gemini over one OpenAI-compatible client.

Moves to the next provider on rate limit (429), timeout, connection error, auth error or 5xx.
No key for a provider = that provider is skipped.
"""
from __future__ import annotations

import logging
import os
import time

from app import config

log = logging.getLogger(__name__)

PROVIDERS: dict[str, dict] = {
    "groq": {"base_url": "https://api.groq.com/openai/v1", "key": "GROQ_API_KEY",
             "model_env": "GROQ_MODEL", "default": "openai/gpt-oss-120b"},
    "gemini": {"base_url": "https://generativelanguage.googleapis.com/v1beta/openai/", "key": "GEMINI_API_KEY",
               "model_env": "GEMINI_MODEL", "default": "gemini-3.5-flash"},
}


class LLMUnavailable(Exception):
    """Every provider in LLM_CHAIN failed or has no key."""


def available() -> list[str]:
    return [p for p in config.LLM_CHAIN if p in PROVIDERS and os.getenv(PROVIDERS[p]["key"], "").strip()]


def model_for(provider: str, overrides: dict[str, str] | None = None) -> str:
    p = PROVIDERS[provider]
    return (overrides or {}).get(provider) or os.getenv(p["model_env"], "").strip() or p["default"]


_clients: dict[str, object] = {}


def _client(provider: str):
    if provider not in _clients:
        from openai import OpenAI
        p = PROVIDERS[provider]
        _clients[provider] = OpenAI(api_key=os.getenv(p["key"]), base_url=p["base_url"],
                                    timeout=config.LLM_TIMEOUT, max_retries=0)
    return _clients[provider]


def chat_json(messages: list[dict], overrides: dict[str, str] | None = None,
              max_tokens: int = config.LLM_MAX_TOKENS) -> tuple[str, str, str]:
    """Return (content, provider, model). Raises LLMUnavailable if the whole chain fails."""
    import openai

    errors = []
    chain = available()
    if not chain:
        raise LLMUnavailable("no API key set for any provider in LLM_CHAIN")
    for provider in chain:
        model = model_for(provider, overrides)
        kwargs = dict(model=model, messages=messages, temperature=0, max_tokens=max_tokens,
                      response_format={"type": "json_object"})
        if "gpt-oss" in model:          # reasoning model: keep hidden reasoning short (speed + token budget)
            kwargs["extra_body"] = {"reasoning_effort": "low"}
        waited = False
        for attempt in range(3):
            try:
                t = time.time()
                r = _client(provider).chat.completions.create(**kwargs)
                content = r.choices[0].message.content or ""
                log.info("LLM %s/%s answered in %.1fs", provider, model, time.time() - t)
                return content, provider, model
            except openai.BadRequestError as e:
                if "response_format" in str(e) and "response_format" in kwargs:   # provider without JSON mode
                    kwargs.pop("response_format")
                    continue
                if "reasoning_effort" in str(e) and "extra_body" in kwargs:
                    kwargs.pop("extra_body")
                    continue
                errors.append(f"{provider}: {e}")
                break
            except (openai.RateLimitError, openai.InternalServerError) as e:
                # free tiers: "slow down" (429) or "busy" (503) -> wait once if the wait is short, else next provider
                delay = _retry_after(e)
                if not waited and delay <= config.LLM_MAX_WAIT:
                    log.info("LLM %s %s, retrying in %.1fs", provider, type(e).__name__, delay)
                    time.sleep(delay)
                    waited = True
                    continue
                errors.append(f"{provider}: {type(e).__name__}: {str(e)[:200]}")
                break
            except (openai.APITimeoutError, openai.APIConnectionError,
                    openai.AuthenticationError, openai.PermissionDeniedError, openai.NotFoundError,
                    openai.InternalServerError, openai.APIStatusError) as e:
                errors.append(f"{provider}: {type(e).__name__}: {str(e)[:200]}")
                break
    raise LLMUnavailable("; ".join(errors))


def _retry_after(e) -> float:
    """Seconds the provider asks us to wait (Retry-After header, or 'try again in 4.2s' in the message)."""
    import re
    try:
        h = e.response.headers.get("retry-after")
        if h:
            return float(h)
    except Exception:
        pass
    m = re.search(r"try again in (?:(\d+)m)?([\d.]+)s", str(e))
    if m:
        return 60 * float(m.group(1) or 0) + float(m.group(2))
    return 2.0
