"""Cupcake ordering agent - Microsoft Agent Framework demo."""

import asyncio
import os

from dotenv import load_dotenv

from agent_framework import Agent, MCPStreamableHTTPTool
from agent_framework.foundry import AnthropicFoundryClient

load_dotenv()


async def main() -> None:
    instructions = open("instructions.md", encoding="utf-8").read()

    chat_client = AnthropicFoundryClient(
        model=os.environ["FOUNDRY_MODEL_DEPLOYMENT"],
        api_key=os.environ["FOUNDRY_API_KEY"],
        base_url=os.environ["FOUNDRY_ENDPOINT"],
    )

    mcp_tool = MCPStreamableHTTPTool(
        name="cupcake-store",
        url="https://ca-cupcake-mcp.jollyplant-ed217b0d.eastus.azurecontainerapps.io/mcp/",
    )
    await mcp_tool.connect()

    agent = Agent(
        client=chat_client,
        name="cupcake-agent",
        instructions=instructions,
        tools=mcp_tool,
    )

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
