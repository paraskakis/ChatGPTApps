Build an Airport Weather MCP server plus a separate sample UI.

FUNCTIONAL REQUIREMENTS

1. MCP SERVER

Weather data
- Accept a 3–8 character ICAO station identifier, such as KJFK.
- Use only the NWS API:
  GET https://api.weather.gov/stations/{ICAO}/observations/latest
- If an NWS field is missing or null, return it as missing. Never use METAR, AviationWeather.gov, or another fallback.
- Normalize:
  - temperatureC: Celsius
  - windSpeedKt: knots
  - windDirection: numeric degrees
  - visibilityMi: statute miles
  - barometric pressure: NWS barometric pressure converted to inHg when present
- Expose a `get_airport_weather` tool with readable text and structured JSON.
- Show missing values as “Not reported”.
- Format wind direction as a three-digit bearing at presentation time, e.g. 005°, 090°, 270°.

MCP rendering
- Register an MCP Apps `ui://` HTML resource linked to the tool.
- The resource should render the structured tool result as an interactive weather card.
- Include station, temperature, condition, wind, direction, visibility, pressure, timestamp, and NWS source.

2. SEPARATE SAMPLE UI

- Create a standalone React/Vite sample web UI in its own artifact.
- Do not make the sample UI part of the MCP transport or MCP resource implementation.
- Provide an ICAO input and “Check weather” action.
- Consume the REST weather endpoint directly, not the MCP endpoint.
- Include loading, empty, error, and success states.
- Use a responsive aviation dashboard/card layout.
- Display °C, kt, statute miles, in, and three-digit wind direction.
- Clearly label the source as NWS.
- Include observation time and an NWS station link.

NON-FUNCTIONAL REQUIREMENTS

MCP server
- Use TypeScript and the official MCP TypeScript SDK v2:
  - `createMcpHandler`
  - per-request `McpServer` factory
  - `toNodeHandler`
- Expose only `/mcp`.
- Do not create or preserve `/api/mcp`; that is a legacy route.
- Use MCP protocol version `2026-07-28`.
- Use stateless modern MCP transport.
- Serve the UI resource as `text/html;profile=mcp-app`.
- Include standard MCP Apps UI metadata and OpenAI output-template compatibility metadata.
- Validate Origin headers and preserve cache metadata.

Project architecture
- Keep the MCP server and sample UI as separate concerns/artifacts.
- Define REST contracts in OpenAPI first, then generate Zod schemas and React Query clients.
- Bind services to the workflow-provided `PORT`.
- Use explicit numeric fields and unit names in the API contract.

Verification
- Run code generation, library typechecks, API typecheck/build, and sample UI typecheck.
- Live-check KSFO, KOAK, KLVK, KSJC, KORD, KLAS, KJFK, and KTEB.
