"""Cupcake ordering agent - Microsoft Agent Framework demo."""

import asyncio
import os

from dotenv import load_dotenv

from agent_framework import Agent, MCPStreamableHTTPTool

# 1. Load environment variables from .env
load_dotenv()


def _create_chat_client():
    """Create the appropriate Foundry chat client based on MODEL_PROVIDER."""
    provider = os.environ.get("MODEL_PROVIDER", "anthropic").lower()

    if provider == "openai":
        from azure.identity import DefaultAzureCredential
        from agent_framework.foundry import FoundryChatClient

        return FoundryChatClient(
            project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
            model=os.environ["FOUNDRY_MODEL_DEPLOYMENT"],
            credential=DefaultAzureCredential(),
        )
    else:
        from agent_framework.foundry import AnthropicFoundryClient

        return AnthropicFoundryClient(
            model=os.environ["FOUNDRY_MODEL_DEPLOYMENT"],
            api_key=os.environ["FOUNDRY_API_KEY"],
            base_url=os.environ["FOUNDRY_ENDPOINT"],
        )


async def main() -> None:
    # 2. Read the agent's instructions (system prompt)
    instructions = open("instructions.md", encoding="utf-8").read()

    # 3. Configure the chat model
    chat_client = _create_chat_client()

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
