## Part 4 - Build the Agent

With Foundry on the line, time to write some code. You'll be using the
**Microsoft Agent Framework** - a small Python library that wraps a chat
model, a session (the conversation history), and any tools you give it
into a single 'Agent' object you can talk to.

You'll build the agent up over the next three steps - run it after each
step to see it grow.

### Setup

In Visual Studio Code, open a new terminal (**Terminal > New Terminal**).
It opens in 'c:\agents' - the folder where the workshop code lives.

The Python **dependencies are already installed** on the lab VM. For
reference, here's what's in 'requirements.txt':

- **agent-framework** - the core 'Agent', sessions, and tool plumbing.
- **agent-framework-foundry** - the Foundry-specific chat clients (this is
  what knows how to talk to your Anthropic deployment on Foundry).
- **python-dotenv** - loads your '.env' file into environment variables.

An empty **agent.py** file is already waiting for you in 'c:\agents'.

---

✅ **In this step you have:** opened the VS Code terminal in 'c:\agents'
and confirmed the Python dependencies and an empty 'agent.py' are ready.

➡️ Click **Next** to write your first Hello World agent.
