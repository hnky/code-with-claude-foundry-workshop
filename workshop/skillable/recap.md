## Recap

Nice work - you just shipped a working AI agent. In under a hundred
lines of Python, you built something that:

- ✅ Talks to a **Claude Sonnet** deployment hosted on **Microsoft
  Foundry**, using nothing more than an endpoint, a key, and a
  deployment name from your '.env' file.
- ✅ Calls **live tools** through an **MCP server** - listing flavors,
  checking stock, and placing real orders against the Cupcake Store
  backend.
- ✅ Pulls its **persona** and **welcome banner** straight from the MCP
  server's **prompts**, so the same code becomes a different agent the
  moment the server changes its mind.

The pattern you just used - **Foundry for the model, the Agent
Framework for the glue, MCP for tools and prompts** - is exactly the
one you'd use to build a customer-support bot, an internal company
helper, a coding assistant, or pretty much any agent that needs both a
brain and hands. Swap the MCP server for a different one, point at a
different model, tweak the persona, and you have an entirely new agent
without rewriting the plumbing.

### Where to go next

Now that the basic loop works, here are a few directions to push it:

- **Add another MCP server.** The framework can connect to several at
  once. Try giving the agent a weather server, a calendar, or a search
  tool alongside the cupcake store and watch it pick the right tool
  for each question.
- **Swap the model.** Deploy a different model on Foundry (like Opus or Haiku),
  change 'FOUNDRY_MODEL_DEPLOYMENT' in your '.env', and see how the personality, latency, and tool-calling style shift.
- **Stream the responses.** Replace 'agent.run(...)' with
  'agent.run_stream(...)' to print tokens as they arrive. Long answers
  feel dramatically snappier when the user sees the first words right
  away.
- **Persist the session.** Right now the conversation lives in memory.
  Save the session to disk (or a database) and your agent can remember
  yesterday's order the next time the customer walks in.
- **Build your own MCP server.** Now that you've consumed one, writing
  one is the natural next step - and the moment you do, every agent
  that speaks MCP (yours or someone else's) can use your tools.

**Thanks for building with us - now go eat your cupcake. 🧁**