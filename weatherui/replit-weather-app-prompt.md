Build an MCP App to display the current weather at a station

# FUNCTIONAL REQUIREMENTS

## MCP APP

### MCP Server
Name the server `airport-weather`
- Expose a single `get_airport_weather` tool with title `Get Airport Weather`
- Set the tool description to `Displays the latest aviation weather report for an airport or weather station. Data source is the US National Weather Service. Uses the 4-character ICAO location ID as input - match the closest airport to the user's location. Use when the user says "get the latest weather" for an airport. Do not use for locations outside the USA or for city weather or when the user wants a weather forecast`
- Set `readOnlyHint` to true
- Set `destructiveHint` to false
- Set `openWorldHint` to false
- Set `idemotontHint` to true

### MCP UI
- Generate a single compact inline card per the MCP App spec
- If an NWS field is missing or null, return it as missing. Never use a fallback.
- Fields to display:
  - temperatureC: Celsius
  - dewPoint: Celsius
  - windSpeedKt: knots
  - windDirection: numeric degrees
  - visibilityMi: statute miles
  - barometric pressure: NWS barometric pressure converted to inHg when present
- Show missing values as “Not reported”.
- Format wind direction as a three-digit bearing at presentation time, e.g. 005°, 090°, 270°.
- Register an MCP Apps `ui://` HTML resource linked to the tool.
- Include station code and name, timestamp in UTC, and NWS source as a link.

2. SEPARATE SAMPLE UI
- Create a standalone React/Vite sample web UI in its own artifact.
- Do not make the sample UI part of the MCP transport or MCP resource implementation.
- Provide an ICAO input and “Check weather” action.
- Consume the REST weather endpoint directly, not the MCP endpoint.
- Include loading, empty, error, and success states.
- Use the exact smae presentation as the MCP UI

# NON-FUNCTIONAL REQUIREMENTS

## MCP server
- Use TypeScript and the official MCP TypeScript SDK v2:
  - `createMcpHandler`
  - per-request `McpServer` factory
  - `toNodeHandler`
- Expose only `/mcp`.
- Use MCP protocol version `2026-07-28`.
- Serve the UI resource as `text/html;profile=mcp-app`.
- Include standard MCP Apps UI metadata and OpenAI/Claude output-template compatibility metadata.
- Validate Origin headers and preserve cache metadata.

## Project architecture
- Keep the MCP server and sample UI as separate concerns/artifacts.
- Define REST contracts in OpenAPI first, then generate Zod schemas and React Query clients.
- Bind services to the workflow-provided `PORT`.
- Use explicit numeric fields and unit names in the API contract.

Verification
- Run code generation, library typechecks, API typecheck/build, and sample UI typecheck.
- Live-check KSFO, KOAK, KLVK, KSJC, KORD, KLAS, KJFK, and KTEB.
