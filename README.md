# local-first-llm-runtime

Runs local LLMs by default via Ollama or llama.cpp, with cloud providers blocked unless explicitly enabled.

## Purpose
Provide a privacy-first runtime layer for assistant workloads where local inference is the default operating mode.

## Features
- Defaults to local providers (`ollama`, `llama.cpp`) for all core modes.
- Explicit cloud gate so remote providers are disabled by default.
- Provider fallback ordering for resilient local execution.
- Environment-driven endpoint/model selection.
- Startup validation checklist for model and endpoint readiness.

## Config
- `LOCAL_PROVIDER`: Primary local backend (`ollama` or `llama_cpp`).
- `OLLAMA_BASE_URL`: Ollama server URL (example: `http://127.0.0.1:11434`).
- `LLAMA_CPP_BASE_URL`: llama.cpp server URL (example: `http://127.0.0.1:8080`).
- `LOCAL_DEFAULT_MODEL`: Local model alias (example: `qwen2.5:7b`).
- `ALLOW_CLOUD_FALLBACK`: `false` by default; must be set to `true` to allow cloud.

## Quickstart
```bash
cp .env.example .env
# Set local provider, URL, and model in .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 runtime.py --mode chat
```

## Roadmap
- Add automatic local model health scoring for fallback routing.
- Add provider-specific timeout and retry policies.
- Add benchmark profiles for latency/quality tradeoff.
- Add deployment profiles for desktop and container runtime.
