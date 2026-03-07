#!/usr/bin/env python3
"""
Council — Get second opinions from competing AI models via OpenRouter.

Usage:
    # Single model consultation
    python council.py consult --category bug_fix --context "description of the problem"

    # Explicit model override
    python council.py consult --model google/gemini-3.1-pro-preview --context "question here"

    # Fan out to all competitors
    python council.py consult --fan-out --context "question here"

    # Discover latest models from OpenRouter
    python council.py models

    # Show current config
    python council.py config
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "references" / "council_config.json"
OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"
OPENROUTER_CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"


def get_api_key():
    key = os.environ.get("OPENROUTER_API_KEY")

    # Check ~/.env
    if not key:
        env_file = Path.home() / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("OPENROUTER_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break

    # Check project .env
    if not key:
        project_env = Path.cwd() / ".env"
        if project_env.exists():
            for line in project_env.read_text().splitlines():
                if line.startswith("OPENROUTER_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break

    if not key:
        _setup_api_key()

    return key


def _setup_api_key():
    """First-run setup: create ~/.env template and guide the user."""
    env_file = Path.home() / ".env"

    # Create or append to ~/.env with a placeholder if not already there
    if env_file.exists():
        content = env_file.read_text()
        if "OPENROUTER_API_KEY" not in content:
            with open(env_file, "a") as f:
                f.write(
                    "\n# Council Skill — get your key at https://openrouter.ai/keys\n"
                )
                f.write("OPENROUTER_API_KEY=your-key-here\n")
    else:
        env_file.write_text(
            "# Council Skill — get your key at https://openrouter.ai/keys\n"
            "OPENROUTER_API_KEY=your-key-here\n"
        )

    print("\n" + "=" * 60)
    print("  COUNCIL SKILL — FIRST TIME SETUP")
    print("=" * 60)
    print()
    print("You need a free OpenRouter API key to use this skill.")
    print()
    print("  1. Go to: https://openrouter.ai/keys")
    print("  2. Sign up (free) and create an API key")
    print("  3. Open this file:")
    print(f"       {env_file}")
    print("  4. Replace 'your-key-here' with your actual key")
    print("  5. Come back and try again")
    print()
    print("OpenRouter gives you access to GPT, Gemini, and 200+ other")
    print("models through one key. You only pay for what you use.")
    print()
    print(f"  Template created at: {env_file}")
    print("=" * 60 + "\n")
    sys.exit(0)


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Config saved to {CONFIG_PATH}")


def fetch_models():
    """Fetch all available models from OpenRouter."""
    req = urllib.request.Request(OPENROUTER_MODELS_URL)
    req.add_header("Accept", "application/json")
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    return data.get("data", [])


def discover_latest(provider_filter=None):
    """Discover latest flagship models, optionally filtered by provider."""
    models = fetch_models()
    config = load_config()
    tracked_providers = {p["id"] for p in config["providers"]}

    results = {}
    for model in models:
        model_id = model.get("id", "")
        provider = model_id.split("/")[0] if "/" in model_id else ""

        if provider_filter and provider != provider_filter:
            continue
        if not provider_filter and provider not in tracked_providers:
            continue

        if provider not in results:
            results[provider] = []
        results[provider].append(
            {
                "id": model_id,
                "name": model.get("name", model_id),
                "context_length": model.get("context_length", 0),
                "pricing": model.get("pricing", {}),
            }
        )

    # Sort: flagship models first (gemini, gpt-5, codex), then by ID descending
    def sort_key(m):
        mid = m["id"].lower()
        # Prioritize flagship model families
        if "codex" in mid or "gpt-5" in mid:
            return (0, mid)
        if "gemini" in mid:
            return (0, mid)
        if "claude" in mid:
            return (0, mid)
        return (1, mid)

    for provider in results:
        results[provider].sort(key=sort_key)

    return results


def resolve_model(category):
    """Resolve a category to a concrete model ID using config defaults."""
    config = load_config()
    defaults = config.get("defaults", {})

    if category not in defaults:
        print(f"Unknown category: {category}", file=sys.stderr)
        print(f"Available: {', '.join(defaults.keys())}", file=sys.stderr)
        sys.exit(1)

    return defaults[category]


def get_fan_out_models():
    """Get the list of models for multi-opinion fan-out."""
    config = load_config()
    return config.get("fan_out", [])


def consult_model(model_id, context, system_prompt=None):
    """Send a consultation request to a model via OpenRouter."""
    api_key = get_api_key()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": context})

    payload = json.dumps(
        {
            "model": model_id,
            "messages": messages,
            "temperature": 0.3,
        }
    ).encode()

    req = urllib.request.Request(OPENROUTER_CHAT_URL, data=payload, method="POST")
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")
    req.add_header("HTTP-Referer", "https://claude-code-council.local")
    req.add_header("X-Title", "Claude Code Council")

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode())
        choice = data.get("choices", [{}])[0]
        message = choice.get("message", {})
        content = message.get("content", "")
        usage = data.get("usage", {})
        model_used = data.get("model", model_id)
        return {
            "model": model_used,
            "content": content,
            "usage": {
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
            },
        }
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        return {
            "model": model_id,
            "content": f"ERROR ({e.code}): {error_body}",
            "usage": {"prompt_tokens": 0, "completion_tokens": 0},
        }


def cmd_models(args):
    """Show latest available models from tracked providers."""
    provider = getattr(args, "provider", None)
    results = discover_latest(provider)

    if not results:
        print("No models found.")
        return

    for provider, models in sorted(results.items()):
        print(f"\n{'='*60}")
        print(f"  {provider.upper()}")
        print(f"{'='*60}")
        for m in models[:8]:  # Show top 8 per provider
            price_in = m["pricing"].get("prompt", "?")
            price_out = m["pricing"].get("completion", "?")
            ctx = f"{m['context_length']:,}" if m["context_length"] else "?"
            print(f"  {m['id']:<45} ctx:{ctx:<10} ${price_in}/{price_out}")


def cmd_config(args):
    """Show current council config."""
    config = load_config()
    print(json.dumps(config, indent=2))


def cmd_consult(args):
    """Consult one or more models."""
    context = args.context
    if not context:
        # Read from stdin if no context provided
        context = sys.stdin.read().strip()
    if not context:
        print(
            "ERROR: No context provided. Use --context or pipe via stdin.",
            file=sys.stderr,
        )
        sys.exit(1)

    system_prompt = (
        "You are a senior engineer giving a second opinion. "
        "Be direct, specific, and actionable. "
        "If you see issues, call them out. "
        "If the approach is sound, say so briefly and suggest any improvements. "
        "Keep your response concise and focused."
    )

    if args.fan_out:
        # Fan out to all competitor models
        models = get_fan_out_models()
        print(f"\n--- COUNCIL: Consulting {len(models)} models ---\n")
        for model_id in models:
            print(f">> Asking {model_id}...")
            result = consult_model(model_id, context, system_prompt)
            print(f"\n{'='*60}")
            print(f"  MODEL: {result['model']}")
            print(
                f"  TOKENS: {result['usage']['prompt_tokens']} in / {result['usage']['completion_tokens']} out"
            )
            print(f"{'='*60}")
            print(result["content"])
            print()
    elif args.model:
        # Explicit model override
        model_id = args.model
        print(f"\n>> Asking {model_id}...")
        result = consult_model(model_id, context, system_prompt)
        print(f"\n{'='*60}")
        print(f"  MODEL: {result['model']}")
        print(
            f"  TOKENS: {result['usage']['prompt_tokens']} in / {result['usage']['completion_tokens']} out"
        )
        print(f"{'='*60}")
        print(result["content"])
    elif args.category:
        # Route by category
        model_id = resolve_model(args.category)
        print(f"\n>> Category '{args.category}' → {model_id}")
        result = consult_model(model_id, context, system_prompt)
        print(f"\n{'='*60}")
        print(f"  MODEL: {result['model']}")
        print(
            f"  TOKENS: {result['usage']['prompt_tokens']} in / {result['usage']['completion_tokens']} out"
        )
        print(f"{'='*60}")
        print(result["content"])
    else:
        print("ERROR: Specify --category, --model, or --fan-out", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Council — Multi-model second opinions"
    )
    sub = parser.add_subparsers(dest="command")

    # consult
    p_consult = sub.add_parser("consult", help="Consult a model for a second opinion")
    p_consult.add_argument(
        "--category",
        "-c",
        help="Task category (bug_fix, frontend, architecture, refactor, general, quick_check)",
    )
    p_consult.add_argument(
        "--model",
        "-m",
        help="Explicit model ID override (e.g., google/gemini-3.1-pro-preview)",
    )
    p_consult.add_argument(
        "--fan-out", "-f", action="store_true", help="Consult all competitor models"
    )
    p_consult.add_argument(
        "--context",
        "-x",
        help="The question or context to send. Can also pipe via stdin.",
    )
    p_consult.set_defaults(func=cmd_consult)

    # models
    p_models = sub.add_parser("models", help="Discover latest models from OpenRouter")
    p_models.add_argument(
        "--provider", "-p", help="Filter by provider (openai, google, anthropic)"
    )
    p_models.set_defaults(func=cmd_models)

    # config
    p_config = sub.add_parser("config", help="Show current council config")
    p_config.set_defaults(func=cmd_config)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
