# Quick build of an MCP Server to show data from my Lightning Lessons on Maven in ChatGPT or other LLMs that work with MCP.

## TL;DR use my running server at https://ll-mcp.replit.app/mcp

## Build it yourself:
1. Sign up for Replit and create a new app.
2. Attach two files:
- Requirements: https://github.com/paraskakis/ChatGPTApps/blob/main/MCPServerRequirements.md
- Sample Data: https://github.com/paraskakis/ChatGPTApps/blob/main/sample-lightning-lessons.json
3. Enter prompt from https://github.com/paraskakis/ChatGPTApps/blob/main/ReplitMCPServerPrompt.md
```
**Build an MCP (Model Context Protocol) server with the following specifications:**
1. **Transport:** Use the **Streamable HTTP transport** from @modelcontextprotocol/sdk/server/streamableHttp.js (NOT SSE - that's deprecated as of March 2025)
2. **Endpoint:** Create a single /mcp endpoint using app.all("/mcp", ...) that handles both GET and POST requests on the same path
3. **Tools:** Register the tools described in the attached requirements file
4. **Metadata:** Use the information in the requirements file
5. **Data:** Use the attached JSON file
6. **Session Management:** Use a Map to store transports by session ID. For new POST requests without a session ID, create a new StreamableHTTPServerTransport with a sessionIdGenerator that returns a UUID. For requests with an existing session ID header (mcp-session-id), reuse the existing transport.
7. **Server Setup:** Use McpServer from @modelcontextprotocol/sdk/server/mcp.js with name and version of this MCP Server
8. **Frontend:** A simple landing page showing the server status and the MCP endpoint URL
9. **Dependencies:** Install @modelcontextprotocol/sdk
```
4. Once Replit builds the MCP Server test in MCPJam and then add to ChaGPT in Developer Mode: https://developers.openai.com/apps-sdk/deploy/testing
5. Continue to refine descriptions and use Evals in MCPJam to make sure you are getting called by the right prompts: https://developers.openai.com/apps-sdk/guides/optimize-metadata
6. Submit to OpenAI: https://developers.openai.com/apps-sdk/app-submission-guidelines and https://developers.openai.com/apps-sdk/deploy/submission

NOTE: UI widgets are optional. An MCP server that meets their guidelines is a valid ChatGPT app: https://developers.openai.com/apps-sdk/quickstart
Troubleshooting guide: https://developers.openai.com/apps-sdk/deploy/troubleshooting
