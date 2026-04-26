from __future__ import annotations

import json
from urllib import error, request
from typing import Any


POSITIVE_WORDS = {
    "good", "great", "excellent", "amazing", "beautiful", "love", "loved",
    "perfect", "happy", "satisfied", "quality", "premium", "fast", "smooth",
}
NEGATIVE_WORDS = {
    "bad", "poor", "late", "broken", "slow", "disappointed", "worst", "issue",
    "issues", "damaged", "refund", "delay", "difficult", "cheap",
}


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _sentiment_label(review_texts: list[str], avg_rating: float | None) -> str:
    if avg_rating is not None:
        if avg_rating >= 4.2:
            return "strongly positive"
        if avg_rating >= 3.5:
            return "mostly positive"
        if avg_rating >= 2.8:
            return "mixed"
        return "negative"

    pos = 0
    neg = 0
    for text in review_texts:
        words = {w.strip(".,!?;:()[]{}\"'").lower() for w in text.split()}
        pos += len(words.intersection(POSITIVE_WORDS))
        neg += len(words.intersection(NEGATIVE_WORDS))

    if pos > neg * 1.5:
        return "mostly positive"
    if neg > pos * 1.5:
        return "negative"
    return "mixed"


def build_artist_fallback(metrics: dict[str, Any], review_texts: list[str]) -> tuple[str, str]:
    total_revenue = _safe_float(metrics.get("total_revenue"))
    total_orders = _safe_int(metrics.get("total_orders"))
    total_views = _safe_int(metrics.get("catalogue_views"))
    avg_engagement = _safe_float(metrics.get("avg_story_engagement_pct"))
    review_count = _safe_int(metrics.get("review_count"))
    avg_rating = metrics.get("avg_rating")
    avg_rating = _safe_float(avg_rating) if avg_rating is not None else None

    if total_orders > 0:
        aov = round(total_revenue / total_orders, 2)
    else:
        aov = 0

    perf = (
        f"Your catalogues have generated ₹{total_revenue:,.0f} across {total_orders} orders "
        f"with {total_views:,} views. Average order value is ₹{aov:,.0f}, and story engagement "
        f"is around {avg_engagement:.1f}%."
    )

    label = _sentiment_label(review_texts, avg_rating)
    if review_count == 0:
        sentiment = "There are no buyer reviews yet, so sentiment insights will improve as new reviews come in."
    else:
        rating_part = f"average rating is {avg_rating:.1f}/5" if avg_rating is not None else "ratings are still sparse"
        sentiment = (
            f"Buyer sentiment appears {label}: {review_count} reviews analyzed, and the {rating_part}. "
            "Use frequent concerns to guide product and fulfilment improvements."
        )

    return perf, sentiment


def build_platform_fallback(metrics: dict[str, Any]) -> str:
    total_revenue = _safe_float(metrics.get("total_revenue"))
    total_orders = _safe_int(metrics.get("total_orders"))
    registered_artists = _safe_int(metrics.get("registered_artists"))
    registered_buyers = _safe_int(metrics.get("registered_buyers"))
    recent_months = metrics.get("recent_months", [])

    month_revenues = [_safe_float(m.get("revenue")) for m in recent_months if isinstance(m, dict)]
    growth = None
    if len(month_revenues) >= 2 and month_revenues[-2] > 0:
        growth = ((month_revenues[-1] - month_revenues[-2]) / month_revenues[-2]) * 100.0

    trend_line = ""
    if growth is not None:
        direction = "up" if growth >= 0 else "down"
        trend_line = f" Latest month revenue is {direction} {abs(growth):.1f}% from the previous month."

    if total_orders == 0:
        return (
            f"You’re all set for launch with {registered_artists} artist account(s) and {registered_buyers} buyer account(s) onboarded. "
            f"Revenue is currently ₹{total_revenue:,.0f}, and orders are yet to begin.{trend_line} "
            "Next best move: run your first campaign drop and track conversion in this panel."
        )

    return (
        f"Momentum check: the platform has processed ₹{total_revenue:,.0f} across {total_orders} orders, "
        f"with {registered_artists} artists and {registered_buyers} buyers active.{trend_line} "
        "Keep leaning into top-performing categories and tighten fulfilment speed to sustain the pace."
    )


def _extract_text(response: Any) -> str | None:
    text = getattr(response, "text", None)
    if text:
        return text.strip()
    candidates = getattr(response, "candidates", None) or []
    for candidate in candidates:
        content = getattr(candidate, "content", None)
        parts = getattr(content, "parts", None) or []
        for part in parts:
            ptext = getattr(part, "text", None)
            if ptext:
                return ptext.strip()
    return None


def _call_gemini(prompt: str, api_key: str, model: str) -> str | None:
    try:
        import google.generativeai as genai
    except ImportError:
        print("AI ERROR: google-generativeai package not installed")
        return None

    try:
        genai.configure(api_key=api_key)
        llm = genai.GenerativeModel(model)
        response = llm.generate_content(prompt)
        text = _extract_text(response)
        if not text:
             print("AI ERROR (Gemini): Empty response from model")
        return text
    except Exception as e:
        print(f"AI ERROR (Gemini): {str(e)}")
        return None


def _call_groq(prompt: str, api_key: str, model: str) -> str | None:
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.35,
        "max_tokens": 260,
    }
    req = request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) KalaAnalytics/1.0"
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8")
            data = json.loads(body)
            choices = data.get("choices", [])
            if not choices:
                return None
            message = choices[0].get("message", {})
            content = message.get("content")
            return content.strip() if isinstance(content, str) else None
    except Exception as e:
        print(f"AI ERROR (Groq): {str(e)}")
        return None


def _call_model(prompt: str, provider: str, api_key: str, model: str) -> str | None:
    normalized = (provider or "").strip().lower()
    if normalized == "groq":
        return _call_groq(prompt, api_key, model)
    return _call_gemini(prompt, api_key, model)


def _format_review_block(review_texts: list[str], max_items: int = 12) -> str:
    if not review_texts:
        return "No review text available."
    trimmed = [r.strip().replace("\n", " ") for r in review_texts if r and r.strip()]
    trimmed = trimmed[:max_items]
    return "\n".join(f"- {text[:240]}" for text in trimmed)


def generate_artist_summaries(
    metrics: dict[str, Any],
    review_texts: list[str],
    *,
    provider: str = "groq",
    api_key: str | None,
    model: str,
) -> tuple[str, str]:
    fallback_summary, fallback_sentiment = build_artist_fallback(metrics, review_texts)
    if not api_key:
        return fallback_summary, fallback_sentiment

    perf_prompt = (
        "You are generating a short analytics summary for an artist dashboard.\n"
        "Rules:\n"
        "1) Keep it between 80 and 130 words.\n"
        "2) Mention performance trend, key strength, and one practical recommendation.\n"
        "3) Stay factual and do not invent numbers.\n\n"
        f"Metrics JSON:\n{metrics}\n"
    )
    sentiment_prompt = (
        "You are generating a short buyer sentiment summary for an artist dashboard.\n"
        "Rules:\n"
        "1) Keep it between 60 and 110 words.\n"
        "2) Mention tone (positive/mixed/negative), common praise, and one improvement area.\n"
        "3) Base response only on review texts and rating stats.\n\n"
        f"Metrics JSON:\n{metrics}\n\n"
        "Recent review excerpts:\n"
        f"{_format_review_block(review_texts)}\n"
    )

    perf_ai = _call_model(perf_prompt, provider, api_key, model)
    sentiment_ai = _call_model(sentiment_prompt, provider, api_key, model)

    return perf_ai or fallback_summary, sentiment_ai or fallback_sentiment


def generate_platform_summary(
    metrics: dict[str, Any],
    *,
    provider: str = "groq",
    api_key: str | None,
    model: str,
) -> str:
    fallback = build_platform_fallback(metrics)
    if not api_key:
        return fallback

    prompt = (
        "You are generating a short executive analytics summary for an admin dashboard.\n"
        "Rules:\n"
        "1) Keep it between 90 and 140 words.\n"
        "2) Mention growth signal(s), risk/attention area, and one action recommendation.\n"
        "3) Keep tone energetic but professional.\n"
        "4) Do not invent numbers.\n\n"
        f"Metrics JSON:\n{metrics}\n"
    )

    ai_text = _call_model(prompt, provider, api_key, model)
    return ai_text or fallback


def build_review_fallback(metrics: dict[str, Any], review_texts: list[str]) -> str:
    review_count = _safe_int(metrics.get("review_count"))
    avg_rating = metrics.get("avg_rating")
    avg_rating = _safe_float(avg_rating) if avg_rating is not None else None
    label = _sentiment_label(review_texts, avg_rating)

    if review_count == 0:
        return "No reviews yet for this product. Once buyers start sharing feedback, this summary will highlight recurring praise and issues."

    rating_line = f"Average rating is {avg_rating:.1f}/5." if avg_rating is not None else "Rating data is limited."
    
    # Basic keyword extraction for a slightly better fallback
    all_text = " ".join(review_texts).lower()
    keywords = []
    if "quality" in all_text or "craft" in all_text: keywords.append("quality")
    if "fast" in all_text or "quick" in all_text or "delivery" in all_text: keywords.append("service")
    if "design" in all_text or "style" in all_text or "beautiful" in all_text: keywords.append("design")
    
    keyword_str = ""
    if keywords:
        keyword_str = f" with specific mention of {', '.join(keywords)}."

    return (
        f"Based on {review_count} buyer reviews, sentiment is currently {label}. "
        f"{rating_line} Buyers have shared their experiences regarding this product{keyword_str}, "
        "providing valuable insights for future customers."
    )


def generate_review_summary(
    *,
    metrics: dict[str, Any],
    review_texts: list[str],
    target_label: str,
    provider: str = "groq",
    api_key: str | None,
    model: str,
) -> str:
    fallback = build_review_fallback(metrics, review_texts)
    if not api_key:
        return fallback

    prompt = (
        f"You are generating a short buyer-facing review summary for a {target_label} page.\n"
        "Rules:\n"
        "1) Keep it between 55 and 95 words.\n"
        "2) Mention sentiment tone and one practical buyer insight.\n"
        "3) Use only provided review stats/text; do not invent facts.\n\n"
        f"Metrics JSON:\n{metrics}\n\n"
        "Recent review excerpts:\n"
        f"{_format_review_block(review_texts)}\n"
    )

    ai_text = _call_model(prompt, provider, api_key, model)
    return ai_text or fallback
