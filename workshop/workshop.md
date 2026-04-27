# Workshop: Build an AI Agent with Microsoft Foundry & Microsoft Agent Framework

In this lab you will:

1. Log in to **Microsoft Foundry** and find a chat model.
2. Grab the model's **endpoint** and **API key**.
3. Build a Python agent with the **Microsoft Agent Framework** step-by-step:
   - A minimal "hello world" agent
   - Give it **instructions** (a system prompt)
   - Extend it with an **MCP tool** (the Cupcake Store)

**Prerequisites**
- Access to an Azure subscription with Microsoft Foundry
- Python 3.10+ installed
- This repository cloned locally (or opened in a Codespace)



## Part 1 - Log in to Microsoft Foundry

1. Open <https://ai.azure.com> in your browser.
2. Sign in with the account provided for the workshop.
3. Select a **project**.

> 📸 **Screenshot placeholder:** Foundry landing page with the project selected.
> Save as `workshop/images/01-foundry-home.png`.



## Part 2 - Find a Model and Test It

1. In the top navigation, make sure **Build** is selected.
2. In the left-hand navigation, click **Models**.
3. On the **Deployments** tab you'll see all models deployed to this project.
   For this workshop, pick **`claude-sonnet-4-6`**.
   The **Name** column is the **deployment name** - you'll need it later.
4. Click the deployment - you'll land directly in the **Playground** and can
   chat with it right there.
5. Type `Hello world` and verify the model responds.

> 📸 **Screenshot placeholder:** Build > Models > Deployments list with a model selected.
> Save as `workshop/images/02-models-deployments.png`.

> 📸 **Screenshot placeholder:** Chat playground with "Hello world" and the model's reply.
> Save as `workshop/images/02b-playground-hello.png`.



## Part 3 - Get the Endpoint and API Key

1. Back on **Build > Models**, click your deployment to open the details panel on the right.
2. Copy:
   - **Target URI** - the endpoint, e.g. `https://<your-resource>.services.ai.azure.com/anthropic`
   - **Key** - click the eye icon to reveal it, then the copy icon
   - **Name** of the deployment (e.g. `claude-sonnet-4-6`)

> 📸 **Screenshot placeholder:** Deployment details panel showing Target URI and Key (blur the key!).
> Save as `workshop/images/03-endpoint-keys.png`.

3. Open the existing `.env` file in the `agent-framework/` folder and replace
   the placeholder values with the ones you just copied:

   ```env
   FOUNDRY_ENDPOINT="https://<your-resource>.services.ai.azure.com/anthropic"
   FOUNDRY_API_KEY="<your-api-key>"
   FOUNDRY_MODEL_DEPLOYMENT="<your-deployment-name>"
   ```



## Part 4 - Build the Agent

### Setup

Open a terminal in the `agent-framework/` folder:

```bash
cd agent-framework
```

The folder already contains a `requirements.txt` with the dependencies you need:

```txt
agent-framework
agent-framework-foundry
python-dotenv
```

Install them:

```bash
pip install -r requirements.txt
```

Create an empty `agent.py` file in the same folder. You'll build it up in three
steps. After each step, run:

```bash
python agent.py
```



### Step 1 - Hello World Agent

Start with a minimal agent that just talks to the model.

```python
"""Cupcake ordering agent - Microsoft Agent Framework demo."""

import asyncio
import os

from dotenv import load_dotenv

from agent_framework import Agent
from agent_framework.foundry import AnthropicFoundryClient

# 1. Load environment variables from .env
load_dotenv()


async def main() -> None:
    # 2. Configure the chat model (Claude on Microsoft Foundry)
    chat_client = AnthropicFoundryClient(
        model=os.environ["FOUNDRY_MODEL_DEPLOYMENT"],
        api_key=os.environ["FOUNDRY_API_KEY"],
        base_url=os.environ["FOUNDRY_ENDPOINT"],
    )

    # 3. Create the agent
    agent = Agent(
        client=chat_client,
        name="cupcake-agent",
    )

    # 4. Start a chat session and talk to the agent
    session = agent.create_session()
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            break

        response = await agent.run(user_input, session=session)
        print(f"Assistant: {response.text}\n")


if __name__ == "__main__":
    asyncio.run(main())
```

**Try it:**

```
You: Hello!
Assistant: Hi there! How can I help you today?
```

> 📸 **Screenshot placeholder:** Terminal showing the first "Hello" exchange.
> Save as `workshop/images/04-step1-hello.png`.



### Step 2 - Add Instructions

Give the agent a persona by loading a system prompt from `instructions.md`.

The repo already contains `agent-framework/instructions.md`:

```markdown
You are a friendly cupcake-shop concierge at a workshop demo booth. You help a
single customer order exactly ONE cupcake for in-person pickup, using the
tools provided by the "Cupcake Store" MCP server.
```

Update `agent.py` - read the instructions and pass them to the `Agent`:

```python
async def main() -> None:
    # Read the agent's instructions (system prompt)
    instructions = open("instructions.md").read()   # 👈 new

    chat_client = AnthropicFoundryClient(
        model=os.environ["FOUNDRY_MODEL_DEPLOYMENT"],
        api_key=os.environ["FOUNDRY_API_KEY"],
        base_url=os.environ["FOUNDRY_ENDPOINT"],
    )

    agent = Agent(
        client=chat_client,
        name="cupcake-agent",
        instructions=instructions,   # 👈 new
    )

    session = agent.create_session()
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            break

        response = await agent.run(user_input, session=session)
        print(f"Assistant: {response.text}\n")
```

**Try it:** Ask "What do you sell?" - the agent should now behave like a
cupcake-shop concierge. It doesn't have any real data yet, so it will improvise
politely.

> 📸 **Screenshot placeholder:** Terminal showing the agent responding in-character.
> Save as `workshop/images/05-step2-instructions.png`.



### Step 3 - Add the Cupcake Store MCP Server

Now give the agent **real tools** by connecting to the Cupcake Store MCP server.

Add the `MCPStreamableHTTPTool` import, connect to the server, pass it to the
agent, and close it when the chat ends:

```python
"""Cupcake ordering agent - Microsoft Agent Framework demo."""

import asyncio
import os

from dotenv import load_dotenv

from agent_framework import Agent, MCPStreamableHTTPTool   # 👈 updated
from agent_framework.foundry import AnthropicFoundryClient

# 1. Load environment variables from .env
load_dotenv()


async def main() -> None:
    # 2. Read the agent's instructions (system prompt)
    instructions = open("instructions.md").read()

    # 3. Configure the chat model (Claude on Microsoft Foundry)
    chat_client = AnthropicFoundryClient(
        model=os.environ["FOUNDRY_MODEL_DEPLOYMENT"],
        api_key=os.environ["FOUNDRY_API_KEY"],
        base_url=os.environ["FOUNDRY_ENDPOINT"],
    )

    # 4. Connect to the Cupcake Store MCP server
    mcp_tool = MCPStreamableHTTPTool(
        name="cupcake-store",
        url="https://ca-cupcake-mcp.jollyplant-ed217b0d.eastus.azurecontainerapps.io/mcp/",
    )
    await mcp_tool.connect()

    # 5. Create the agent
    agent = Agent(
        client=chat_client,
        name="cupcake-agent",
        instructions=instructions,
        tools=mcp_tool,   # 👈 new
    )

    # 6. Start a chat session and talk to the agent
    session = agent.create_session()
    print("Type 'exit' to quit.\n")

    try:
        while True:
            user_input = input("You: ")
            if user_input.lower() in ("exit", "quit"):
                break

            response = await agent.run(user_input, session=session)
            print(f"Assistant: {response.text}\n")
    finally:
        await mcp_tool.close()


if __name__ == "__main__":
    asyncio.run(main())
```

**Try it:**

```
You: What flavors do you have today?
Assistant: Here's what we have in stock today: ...
You: I'll take one chocolate cupcake.
Assistant: Great choice! I've placed the order ...
```

The agent is now calling MCP tools on the Cupcake Store server.

> 📸 **Screenshot placeholder:** Terminal showing the agent listing flavors and placing an order.
> Save as `workshop/images/06-step3-mcp.png`.



## Recap

You built an AI agent that:

- ✅ Uses a model deployment from Microsoft Foundry
- ✅ Follows a custom persona via a system prompt
- ✅ Calls live tools through an MCP server

The final, complete source is in [`agent-framework/agent.py`](../agent-framework/agent.py).



## Troubleshooting

| Problem | Fix |
|||
| `Missing required environment variable` | Check `.env` is in the `agent-framework/` folder and the variable names match |
| `401 Unauthorized` | Wrong API key or endpoint - re-copy from Foundry |
| `DeploymentNotFound` | `FOUNDRY_MODEL_DEPLOYMENT` must match the **deployment** name, not the model name |
| `ImportError: cannot import name 'Agent'` | Run `pip install -r requirements.txt` again |













