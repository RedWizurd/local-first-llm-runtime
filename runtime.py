import argparse
import json
import os
from datetime import datetime, timezone


def getenv_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def build_runtime_plan(mode: str, prompt: str) -> dict:
    local_provider = os.getenv("LOCAL_PROVIDER", "ollama")
    local_model = os.getenv("LOCAL_DEFAULT_MODEL", "qwen2.5:7b")
    allow_cloud = getenv_bool("ALLOW_CLOUD_FALLBACK", False)

    local_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    if local_provider == "llama_cpp":
        local_url = os.getenv("LLAMA_CPP_BASE_URL", "http://127.0.0.1:8080")

    fallback = {
        "provider": "blocked",
        "reason": "Cloud fallback disabled by default for privacy.",
    }
    if allow_cloud:
        fallback = {
            "provider": os.getenv("CLOUD_PROVIDER", "openai"),
            "reason": "Explicitly allowed via ALLOW_CLOUD_FALLBACK=true.",
        }

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "prompt_preview": prompt[:80],
        "primary": {
            "provider": local_provider,
            "model": local_model,
            "base_url": local_url,
        },
        "fallback": fallback,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Local-first LLM runtime planner")
    parser.add_argument("--mode", default="chat", choices=["chat", "builder", "researcher"])
    parser.add_argument("--prompt", default="hello")
    args = parser.parse_args()

    plan = build_runtime_plan(args.mode, args.prompt)
    print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    main()
