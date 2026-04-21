"""Cupcake ordering agent - Microsoft Agent Framework demo."""

import asyncio
import os

from dotenv import load_dotenv

from agent_framework import Agent, MCPStreamableHTTPTool
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
        tools=mcp_tool,
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
