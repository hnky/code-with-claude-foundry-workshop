## Part 4 - Step 1: Hello World Agent

Start with a minimal agent that just talks to the model. No tools, no
persona - just confirm we can reach Foundry. Three pieces show up here
that you'll see in every agent you build:

- **Chat client** - the connection to the model. 'AnthropicFoundryClient'
  knows how to call your Claude deployment on Foundry using the values
  from '.env'.
- **Agent** - wraps the chat client (and later, tools and instructions).
- **Session** - holds the conversation history so the agent remembers
  what was said earlier in the chat.

Paste this into 'agent.py':

```python-notype
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

In the VS Code terminal at the bottom of the editor, run:

```bash
python agent.py
```

Send the message `Hello!` to the agent.

If you see a 404 error, check that the endpoint URL in your '.env' file ends with "/anthropic" and not with "/v1/messages".

Type **exit** when you're done to stop the agent.

---

✅ **In this step you have:** wired up an 'AnthropicFoundryClient', wrapped
it in an 'Agent', and chatted with your Claude deployment from your own
code.

➡️ Click **Next** to give the agent some real tools via MCP.
