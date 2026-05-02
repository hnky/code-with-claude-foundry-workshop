# Workshop: Build an AI Agent with Microsoft Foundry & Microsoft Agent Framework

In this lab you will:

1. Log in to **Microsoft Foundry** and find a chat model.
2. Grab the model's **endpoint** and **API key**.
3. Build a Python agent with the **Microsoft Agent Framework** step-by-step:
   - A minimal "hello world" agent
   - Connect to the **Cupcake Store MCP server** for tools
   - Load the agent's **instructions** and **welcome banner** as MCP prompts

**Prerequisites**
- Access to an Azure subscription with Microsoft Foundry
- Python 3.10+ installed
- This repository cloned locally (or opened in a Codespace)



## Part 1 - Log in to Microsoft Foundry

1. Open <https://ai.azure.com> in your browser.
2. Sign in with the account provided for the workshop.
3. In the top bar, toggle the **New Foundry** switch on.
4. Your **project** is selected by default - no need to pick one.

![Foundry landing page with the New Foundry toggle on and the project selected](images/01-foundry-home.png)


## Part 2 - Find a Model and Test It

1. In the top navigation, make sure **Build** is selected.
2. In the left-hand navigation, click **Models**.
3. On the **Deployments** tab you'll see all models deployed to this project.
   For this workshop, pick **`claude-sonnet-4-6`**.
   The **Name** column is the **deployment name** - you'll need it later.
4. Click the deployment - you'll land directly in the **Playground** and can
   chat with it right there.
![Deployed models](images/02-models-deployments.png)

5. Take a moment to explore the **Playground** - it's the fastest way to
   sanity-check a model before you wire it into code:

   - **Model** (top of the panel) - shows which deployment you're chatting
     with. You can switch deployments here without leaving the page.
   - **Instructions** (system prompt) - the box on the left where you set
     the agent's persona and rules. Try pasting
     `You are a pirate. Answer every question in pirate slang.` and chat
     again to see the effect.
   - **Chat** - the main conversation area. Type `Hello world` and verify
     the model responds. Use it to iterate on prompts before committing
     them to code.
   - **View code** - opens a side panel with ready-to-paste snippets
     (Python, curl, etc.) that show exactly how to call this deployment
     from your own app, including the endpoint and headers.

![Deployed models](images/02b-playground-hello.png)



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

Create an empty `agent.py` file in the same folder. You'll build it up in
three small steps. After each step, run:

```bash
python agent.py
```



### Step 1 - Hello World Agent

Start with a minimal agent that just talks to the model. No tools, no
persona - just confirm we can reach Foundry.

```python
"""Sparkles - The Cupcake ordering agent"""

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
        user_input = input("\033[1;35mYou:\033[0m\n")
        if user_input.lower() in ("exit", "quit"):
            break

        response = await agent.run(user_input, session=session)
        print(f"\n\033[1;35mAssistant:\033[0m\n{response.text}\n")


if __name__ == "__main__":
    asyncio.run(main())
```

The `\033[1;35m...\033[0m` escape codes print `You:` and `Assistant:` in
bold magenta so the transcript is easier to read.

**Try it:**

```
You:
Hello!

Assistant:
Hi there! How can I help you today?
```

> 📸 **Screenshot placeholder:** Terminal showing the first "Hello" exchange.
> Save as `workshop/images/04-step1-hello.png`.



### Step 2 - Connect to the Cupcake Store MCP Server

Now give the agent **real tools** by connecting to the Cupcake Store MCP
server. The server exposes tools the agent can call (list flavors, place an
order, etc.).

Two changes:

1. Import `MCPStreamableHTTPTool`, create it, and `connect()`.
2. Pass it to the `Agent` via `tools=`.

```python
"""Sparkles - The Cupcake ordering agent"""

import asyncio
import os

from dotenv import load_dotenv

from agent_framework import Agent, MCPStreamableHTTPTool   # 👈 updated
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

    # 3. Connect to the Cupcake Store MCP server                 👈 new
    mcp_tool = MCPStreamableHTTPTool(
        name="cupcake-store",
        url="https://ca-cupcake-mcp.jollyplant-ed217b0d.eastus.azurecontainerapps.io/mcp/",
    )
    await mcp_tool.connect()

    # 4. Create the agent
    agent = Agent(
        client=chat_client,
        name="cupcake-agent",
        tools=mcp_tool,                                          # 👈 new
    )

    # 5. Start a chat session and talk to the agent
    session = agent.create_session()
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("\033[1;35mYou:\033[0m\n")
        if user_input.lower() in ("exit", "quit"):
            break

        response = await agent.run(user_input, session=session)
        print(f"\n\033[1;35mAssistant:\033[0m\n{response.text}\n")

    await mcp_tool.close()


if __name__ == "__main__":
    asyncio.run(main())
```

**Try it:**

```
You:
What flavors do you have today?

Assistant:
Here's what we have in stock today: ...
```

The agent is now calling MCP tools on the Cupcake Store server. But it's
still acting like a generic assistant - it has no persona yet.

> 📸 **Screenshot placeholder:** Terminal showing the agent listing flavors and placing an order.
> Save as `workshop/images/05-step2-mcp.png`.



### Step 3 - Load Instructions and a Welcome Banner from MCP

MCP servers can also expose **prompts** - pre-written text the server owner
curates. The Cupcake Store exposes two:

- `agent_instructions` - the persona / system prompt
- `welcome_banner` - a friendly greeting to print at startup

Fetch both from the server, pass `agent_instructions` to the `Agent`, and
print the banner before the chat starts.

```python
async def main() -> None:
    # 2. Configure the chat model (Claude on Microsoft Foundry)
    chat_client = AnthropicFoundryClient(
        model=os.environ["FOUNDRY_MODEL_DEPLOYMENT"],
        api_key=os.environ["FOUNDRY_API_KEY"],
        base_url=os.environ["FOUNDRY_ENDPOINT"],
    )

    # 3. Connect to the Cupcake Store MCP server
    mcp_tool = MCPStreamableHTTPTool(
        name="cupcake-store",
        url="https://ca-cupcake-mcp.jollyplant-ed217b0d.eastus.azurecontainerapps.io/mcp/",
    )
    await mcp_tool.connect()

    # 4. Get the instructions and welcome banner from the MCP server   👈 new
    instructions = await mcp_tool.get_prompt("agent_instructions")
    banner = await mcp_tool.get_prompt("welcome_banner")

    # 5. Create the agent
    agent = Agent(
        client=chat_client,
        name="cupcake-agent",
        instructions=instructions,                                     # 👈 new
        tools=mcp_tool,
    )

    # 6. Start a chat session and talk to the agent
    session = agent.create_session()
    print(banner)                                                      # 👈 new
    print("Type 'exit' to quit.\n")

    # Kick things off automatically                                    👈 new
    response = await agent.run("hello", session=session)
    print(f"\033[1;35mAssistant:\033[0m\n{response.text}\n")

    while True:
        user_input = input("\033[1;35mYou:\033[0m\n")
        if user_input.lower() in ("exit", "quit"):
            break

        response = await agent.run(user_input, session=session)
        print(f"\n\033[1;35mAssistant:\033[0m\n{response.text}\n")

    await mcp_tool.close()
```

The agent now also kicks off the conversation itself by sending a `"hello"`,
so the user sees the persona greet them right away.

**Try it:** You should now see the welcome banner first, then the agent
greeting you in-character as a friendly cupcake-shop concierge.

```
🧁 Welcome to the Cupcake Store! ...

Assistant:
Hi there! Ready to pick out a cupcake? ...
```

That's it - your `agent.py` now matches the final sample in
[`sample/agent.py`](../sample/agent.py).

> 📸 **Screenshot placeholder:** Terminal showing the banner and the agent greeting in-character.
> Save as `workshop/images/06-step3-prompts.png`.



## Recap

You built an AI agent that:

- ✅ Uses a model deployment from Microsoft Foundry
- ✅ Calls live tools through an MCP server
- ✅ Loads its persona and welcome banner from MCP **prompts** and greets
  the user automatically

The final, complete source is in [`sample/agent.py`](../sample/agent.py).



## Troubleshooting

| Problem | Fix |
|||
| `Missing required environment variable` | Check `.env` is in the `agent-framework/` folder and the variable names match |
| `401 Unauthorized` | Wrong API key or endpoint - re-copy from Foundry |
| `DeploymentNotFound` | `FOUNDRY_MODEL_DEPLOYMENT` must match the **deployment** name, not the model name |
| `ImportError: cannot import name 'Agent'` | Run `pip install -r requirements.txt` again |













