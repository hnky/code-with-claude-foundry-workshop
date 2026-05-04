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
![Deployed models](../images/02-models-deployments.png)

5. Take a moment to explore the **Playground**, the fastest way to
   experiment with a model before you wire it into code:

   - **Model** (top of the panel) - shows which deployment you're chatting
     with. You can switch deployments here without leaving the page.
   - **Instructions** (system prompt) - the box on the left where you set
     the agent's persona and rules. Try pasting
     `You are a sentient cupcake. Answer every question with frosting-related puns.` and chat
     again to see the effect.
   - **Chat** - the main conversation area. Type `Hello world` and verify
     the model responds. Use it to iterate on prompts before committing
     them to code.
   - **View code** - opens a side panel with ready-to-paste snippets
     (Python, curl, etc.) that show exactly how to call this deployment
     from your own app, including the endpoint and headers.

![Deployed models](../images/02b-playground-hello.png)

---

✅ **In this step you have:** picked the **claude-sonnet-4-6** deployment,
opened the Playground, and chatted with the model to confirm it works.

➡️ Click **Next** to grab the endpoint, key, and deployment name you'll
need from your code.
