## Part 3 - Get the Endpoint and API Key

Now that you know the model works, you need three things to call it from
your own code: the **endpoint** (where to send requests), the **API key**
(proof you're allowed to), and the **deployment name** (which model
instance to use). All three live one click away.

1. In the playground - click the **Details** tab at the top.
2. On the **Details** tab, find the following information:
   - **Target URI** - a URI starting with "https://(your-resource).services.ai.azure.com/"
   - **Key** - click the eye icon to reveal it or the copy icon to copy it
   - **Name** of the deployment (e.g. "claude-sonnet-4-6") - shown under **Deployment info**

   ![Endpoint keys](../images/03-endpoint-keys.png)

   > 🔐 Treat the API key like a password. Don't paste it into chats,
   > screenshots, or commits. The '.env' file you'll edit next is already
   > listed in '.gitignore' so it stays on your machine.

3. On the lab VM, open **Visual Studio Code** from the Start menu or the
   taskbar. It opens 'c:\agents' by default - that's where the workshop
   code lives.

4. In the VS Code Explorer, open the existing '.env' file and replace
   placeholder values with the ones you just found. Shorten the copied endpoint URI so that it ends with "/anthropic" - not with "/v1/messages".

   ```env
   FOUNDRY_ENDPOINT="https://<your-resource>.services.ai.azure.com/anthropic"
   FOUNDRY_API_KEY="<your-api-key>"
   FOUNDRY_MODEL_DEPLOYMENT="claude-sonnet-4-6"
   ```

---

✅ **In this step you have:** copied the **Target URI**, **Key**, and
**deployment name** from Foundry, opened 'c:\agents' in Visual Studio
Code, and pasted the values into the '.env' file.

➡️ Click **Next** to start building the agent in code.
