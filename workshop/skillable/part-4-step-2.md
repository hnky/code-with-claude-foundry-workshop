## Part 4 - Step 2: Connect to the Cupcake Store MCP Server

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

```python-notype
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

In the VS Code terminal at the bottom of the editor, run:

```bash
python agent.py
```

**Try it:**

Send the message `What flavors do you have today?` to the agent.

Do *not* order a cupcake yet! This step is just to confirm that the agent can call the MCP tools to check inventory and answer questions about flavors. Don't worry, you'll get to order a cupcake in the next step!

Type 'exit' when you're done to stop the agent.

The agent is now calling MCP tools on the Cupcake Store server. But it's
still acting like a generic assistant - it has no persona yet.

---

✅ **In this step you have:** connected your agent to the Cupcake Store
MCP server, and watched it call live tools to answer real cupcake
questions.

➡️ Click **Next** to give the agent its persona and welcome banner.
