# Changelog

## 2026-04-27

### Added

- **OpenAI/GPT model support** — `agent.py` now supports both Anthropic (Claude) and OpenAI (GPT) models hosted in Microsoft Foundry via a `MODEL_PROVIDER` environment variable.
- **`azure-identity`** added to `requirements.txt` for `DefaultAzureCredential` authentication with OpenAI-based Foundry deployments.
- **`.env.sample`** updated with documented configuration blocks for both Anthropic and OpenAI providers.
- **Workshop implementation files** — Added `agent-framework/agent.py` and `agent-framework/instructions.md` so learners have the completed Microsoft Agent Framework cupcake-ordering agent in the working folder.

### Changed

- `agent.py` — Extracted client creation into `_create_chat_client()` which switches between `AnthropicFoundryClient` and `FoundryChatClient` based on `MODEL_PROVIDER` env var. Defaults to `anthropic` for backwards compatibility.
- `open("instructions.md")` now uses `encoding="utf-8"` for cross-platform robustness.
- `.gitignore` now ignores local environment files, virtual environments, logs, and scratch command outputs while keeping `.env.sample` templates shareable.

### Removed

- Stopped tracking `agent-framework/.env`; local `.env` files are ignored so API keys, endpoints, and workshop-specific resource values are not included in public commits.

### Validated

- E2E tested with `gpt-5-1` deployment on `leestott-build-resource` (Sweden Central):
  - Hello world (no tools) — PASS
  - MCP Cupcake Store connection — PASS
  - Tool-calling (list flavours, place order) — PASS
- Placed a live Cupcake Store MCP order for one `foundry-special` cupcake and confirmed the order status endpoint returned the pending order.
