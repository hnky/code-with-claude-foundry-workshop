# Code with Claude - Microsoft Foundry Workshop

Build an AI agent with **Microsoft Foundry** and the **Microsoft Agent Framework** that uses a Claude model and calls tools through an MCP server.

## What you will build

A simple cupcake-ordering agent that:

- Uses **Claude Sonnet 4.6** deployed in Microsoft Foundry
- Follows a custom persona via a system prompt (`instructions.md`)
- Calls live tools from the **Cupcake Store MCP server**

## Repository layout

```
.
├── workshop/
│   └── workshop.md              # Step-by-step lab manual
└── sample/
    ├── agent.py                 # Final agent implementation
    ├── instructions.md          # System prompt for the agent
    ├── requirements.txt         # Python dependencies
    └── .env.sample              # Template for environment variables
```

## Prerequisites

- An Azure subscription with access to **Microsoft Foundry**
- A deployed Claude model (e.g. `claude-sonnet-4-6`)
- Python 3.10+

## Quick start

1. Follow the [workshop lab manual](workshop/workshop.md).
2. Or, to run the finished agent directly:

   ```bash
   cd sample
   cp .env.sample .env          # then fill in your Foundry endpoint + key
   pip install -r requirements.txt
   python agent.py
   ```

## Environment variables

Configured in `sample/.env` (see `.env.sample`):

| Variable | Description |
|---|---|
| `FOUNDRY_ENDPOINT` | Target URI of your Foundry deployment, e.g. `https://<resource>.services.ai.azure.com/anthropic` |
| `FOUNDRY_API_KEY` | API key for the Foundry deployment |
| `FOUNDRY_MODEL_DEPLOYMENT` | Deployment name (e.g. `claude-sonnet-4-6`) |
