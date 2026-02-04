**Build an MCP (Model Context Protocol) server with the following specifications:**
1. **Transport:** Use the **Streamable HTTP transport** from @modelcontextprotocol/sdk/server/streamableHttp.js (NOT SSE - that's deprecated as of March 2025)
2. **Endpoint:** Create a single /mcp endpoint using app.all("/mcp", ...) that handles both GET and POST requests on the same path
3. **Tool:** Register one tool called getEcho that returns the string "echo" in the standard MCP content format: { content: [{ type: "text", text: "echo" }] }
4. **Session Management:** Use a Map to store transports by session ID. For new POST requests without a session ID, create a new StreamableHTTPServerTransport with a sessionIdGenerator that returns a UUID. For requests with an existing session ID header (mcp-session-id), reuse the existing transport.
5. **Server Setup:** Use McpServer from @modelcontextprotocol/sdk/server/mcp.js with name and version of this MCP Server
6. **Frontend:** A simple landing page showing the server status and the MCP endpoint URL
7. **Dependencies:** Install @modelcontextprotocol/sdk
