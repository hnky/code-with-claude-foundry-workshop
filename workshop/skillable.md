# Build AI Agents using Claude in Microsoft Foundry

Welcome to **Sparkles**, the friendliest little cupcake shop on the
internet. Sparkles has a problem most bakeries would love to have: too
many customers, too many flavors, and not enough hands behind the
counter. So today, you're going to hire some help - an AI agent that can
greet guests, walk them through the day's flavors, take their order, and
hand them a freshly baked cupcake on the way out.

You'll start by logging in to **Microsoft Foundry**, where you'll meet
**Claude Sonnet** waiting for you in the Playground. After a quick chat
to make sure you two get along, you'll grab the deployment's endpoint and
key and bring them home to your code editor.

From there, you'll build the agent up one small step at a time using the
**Microsoft Agent Framework**. First, a bare-bones "hello world" agent
that proves you can reach the model. Next, you'll plug it into the
**Cupcake Store MCP server** so it gains real superpowers - listing
flavors, checking stock, placing orders. Finally, you'll let the MCP
server hand the agent its own persona and welcome banner, turning a
generic chatbot into Sparkles itself.

By the end, you'll have ordered a cupcake from an agent you built from
scratch - and learned how Foundry, the Agent Framework, and MCP fit
together along the way. 

> **What is Microsoft Foundry?** Foundry is Microsoft's hosted platform
> for shipping AI applications. It's where you deploy models (OpenAI,
> Anthropic, Mistral, your own fine-tunes), give them an endpoint and a
> key, and then wire them into your code. Think of it as the cloud
> control panel for the brains of your agent.
> [Learn more about Microsoft Foundry](https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry?

## Login into the Machine
Everything you'll do today happens on the Windows 11 lab VM on the left
of your screen - browser, code editor, terminal, the lot. Sign in once
and you're set for the rest of the workshop. Click inside the VM,
unlock it, and use the credentials below .

**Username:** +++@lab.VirtualMachine(Windows11).Username+++   
**Password:** +++@lab.VirtualMachine(Windows11).Password+++  

===

## Part 1 - Log in to Microsoft Foundry

1. Open <https://ai.azure.com> in your browser.
2. Sign in with the details below:    
    **Username**: +++@lab.CloudPortalCredential(User1).Username+++    
    **Password (TAP)**:  +++@lab.CloudPortalCredential(User1).AccessToken+++     
3. In the top bar, toggle the **New Foundry** switch on.
4. Your **project** is selected by default - no need to pick one.

![Foundry landing page with the New Foundry toggle on and the project selected](images/01-foundry-home.png)

===

## Part 2 - Find a Model and Test It

A quick word on vocabulary before you click around: a **model** (like
claude-sonnet-4) is the underlying AI. A **deployment** is your
personal, named instance of that model running in your project, with its
own endpoint, key, and rate limits. Your code talks to the *deployment
name*, not the model name - that's the bit you'll wire into your '.env'
in a moment.

1. In the top navigation, make sure **Build** is selected.
2. In the left-hand navigation, click **Models**.
3. On the **Deployments** tab you'll see all models deployed to this project.
   For this workshop, pick **claude-sonnet-4-6**.
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
     'You are a pirate. Answer every question in pirate slang.' and chat
     again to see the effect.
   - **Chat** - the main conversation area. Type 'Hello world' and verify
     the model responds. Use it to iterate on prompts before committing
     them to code.
   - **View code** - opens a side panel with ready-to-paste snippets
     (Python, curl, etc.) that show exactly how to call this deployment
     from your own app, including the endpoint and headers.

![Deployed models](images/02b-playground-hello.png)

===

## Part 3 - Get the Endpoint and API Key

Now that you know the model works, you need three things to call it from
your own code: the **endpoint** (where to send requests), the **API key**
(proof you're allowed to), and the **deployment name** (which model
instance to use). All three live one click away.

1. In the playground - click the **Details** tab at the top.
2. On the **Details** tab, copy:
   - **Target URI** - the endpoint, e.g. "https://<your-resource>.services.ai.azure.com/anthropic"
   - **Key** - click the eye icon to reveal it, then the copy icon next to it
   - **Name** of the deployment (e.g. claude-sonnet-4-6) - shown under **Deployment info**

![Endpoint keys](images/03-endpoint-keys.png)

> 🔐 Treat the API key like a password. Don't paste it into chats,
> screenshots, or commits. The '.env' file you'll edit next is already
> listed in '.gitignore' so it stays on your machine.

3. Open the existing ".env" file in the "sparkles-agent/" folder and replace
   the placeholder values with the ones you just copied:

   ```env
   FOUNDRY_ENDPOINT="https://<your-resource>.services.ai.azure.com/anthropic"
   FOUNDRY_API_KEY="<your-api-key>"
   FOUNDRY_MODEL_DEPLOYMENT="<your-deployment-name>"
   ```

===

## Part 4 - Build the Agent

With Foundry on the line, time to write some code. You'll be using the
**Microsoft Agent Framework** - a small Python library that wraps a chat
model, a session (the conversation history), and any tools you give it
into a single 'Agent' object you can talk to.

### Setup

Open a terminal in the 'sparkles-agent/' folder of this repo:

```bash
cd sparkles-agent
```

The folder already contains a 'requirements.txt' with the dependencies you need:

```
agent-framework
agent-framework-foundry
python-dotenv
```

- 'agent-framework' - the core 'Agent', sessions, and tool plumbing.
- 'agent-framework-foundry' - the Foundry-specific chat clients (this is
  what knows how to talk to your Anthropic deployment on Foundry).
- 'python-dotenv' - loads your '.env' file into environment variables.

Install them:

```bash
pip install -r requirements.txt
```

> 💡 **Tip:** if you're working locally, create a virtual environment
> first ('python -m venv .venv && source .venv/bin/activate') so these
> packages don't pollute your global Python. In Codespaces this is
> already taken care of.

Create an empty 'agent.py' file in the same folder. You'll build it up in
three small steps - run it after each step to see the agent grow.


### Step 1 - Hello World Agent

Start with a minimal agent that just talks to the model. No tools, no
persona - just confirm we can reach Foundry. Three pieces show up here
that you'll see in every agent you build:

- **Chat client** - the connection to the model. 'AnthropicFoundryClient'
  knows how to call your Claude deployment on Foundry using the values
  from '.env'.
- **Agent** - wraps the chat client (and later, tools and instructions).
- **Session** - holds the conversation history so the agent remembers
  what was said earlier in the chat.

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

**Try it:**

```bash
python agent.py
```

```
You:
Hello!

Assistant:
Hi there! How can I help you today?
```

![Hello world](images/04-step1-hello.png)



### Step 2 - Connect to the Cupcake Store MCP Server

A chatbot that only chats is just an expensive parrot. To actually *do*
things - check what flavors are in stock, place an order, mark it ready
for pickup - the agent needs **tools**.

> **What is MCP?** The **Model Context Protocol** is an open standard
> for letting AI agents talk to external systems. An MCP server publishes
> a set of tools (functions the agent can call), prompts (reusable
> instruction snippets), and resources (data) over HTTP. Your agent just
> needs the URL - the framework handles discovery and invocation. The
> Cupcake Store team already runs an MCP server with all the cupcake
> tools you need.

Two changes to your 'agent.py':

1. Import 'MCPStreamableHTTPTool', point it at the server's URL, and call 'connect()'.
2. Pass it to the 'Agent' via 'tools='.

The agent will discover the available tools automatically and decide when
to call them based on what you ask.

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

**Run it:**

```bash
python agent.py
```

**Try it:**

```
You:
What flavors do you have today?

Assistant:
Here's what we have in stock today: ...
```

![](images/05-step2-mcp.png)

The agent is now calling MCP tools on the Cupcake Store server. But it's
still acting like a generic assistant - it has no persona yet.



### Step 3 - Load Instructions and a Welcome Banner from MCP

The agent works, but it still sounds like a generic assistant. The
Cupcake Store has *opinions* about how its agent should behave - tone,
upsells, allergy warnings, the works - and it doesn't want every
developer to copy-paste the latest version of that persona into their
code. So those instructions live on the **server**, not in your repo.

MCP servers can expose **prompts** - reusable text snippets curated by
the server owner. When the persona changes, the server updates; your
code keeps working without a redeploy. The Cupcake Store exposes two:

- 'agent_instructions' - the persona / system prompt
- 'welcome_banner' - a friendly greeting to print at startup

Fetch both from the server, pass 'agent_instructions' to the 'Agent', and
print the banner before the chat starts.

```python
"""Sparkles - The Cupcake ordering agent"""

import asyncio
import os

from dotenv import load_dotenv

from agent_framework import Agent, MCPStreamableHTTPTool  
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

if __name__ == "__main__":
    asyncio.run(main())
```

The agent now also kicks off the conversation itself by sending a 'hello',
so the user sees the persona greet them right away.

**Run it:**

```bash
python agent.py
```

**Try it:** Now it's time to order your cupcake! 

```
Assistant:
Hi there! Ready to pick out a cupcake? ...
```

![](images/06-step3-prompts.png)


- Answer the questions of the agent
- Select your favorite cupcake
- Place your order
- Look at the screen in the room
- When your order is ready for pickup, go to the front of the room to pick it up


![](images/07-dashboard.png)

===

## Recap

In under a hundred lines of Python, you built an AI agent that:

- ✅ Uses a model deployment from Microsoft Foundry
- ✅ Calls live tools through an MCP server
- ✅ Loads its persona and welcome banner from MCP **prompts** and greets
  the user automatically

The pattern you just used - **Foundry for the model, Agent Framework for
the glue, MCP for tools and prompts** - is the same one you'd use to
build a support bot, a coding assistant, or an internal company helper.
Swap the MCP server, change the persona, and you have a different agent.

The full source is in ['sample/agent.py'](../sample/agent.py).

### Where to go next

- **Add another MCP server.** The framework can connect to multiple at
  once - try giving the agent a weather server or a calendar server in
  addition to the cupcake store.
- **Swap the model.** Deploy a different model on Foundry, change
  'FOUNDRY_MODEL_DEPLOYMENT', and see how the personality shifts.
- **Stream the responses.** Use 'agent.run_stream(...)' for token-by-token
  output so the chat feels snappier.
- **Build your own MCP server.** Once you've consumed one, writing one
  is the natural next step - and now your agent can use it.


## Troubleshooting

| Problem | Fix |
| -- | -- |
| 'Missing required environment variable' | Check '.env' is in the 'sparkles-agent/' folder and the variable names match |
| '401 Unauthorized' | Wrong API key or endpoint - re-copy from Foundry |
| 'DeploymentNotFound' | 'FOUNDRY_MODEL_DEPLOYMENT' must match the **deployment** name, not the model name |
| 'ImportError: cannot import name 'Agent'' | Run 'pip install -r requirements.txt' again |