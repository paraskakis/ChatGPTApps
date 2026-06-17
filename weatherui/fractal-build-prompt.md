Build a ChatGPT app to show the current weather conditions at a specific US airport.
You'll use the NWS weather API, at https://api.weather.gov/openapi.json and we'll only need to read the output of the GET /stations/(stationid}/observations/latest endpoint, where stationid is the 4-letter ICAO airport code.

Build a clear Ul that has three modes:
1. (default). Human-readable depiction with diagram/picture of weather conditions, winds, ceiling, cloud layers, visibility, and temperature/dewpoint.
2. A diagnostic pane showing the MCP tool response.
3. A diagnostic pane showing the raw JSON response output from the NWS API call. Make the diagnostics pretty printed and readable.

The user can flip between these panes.
Single card is fine for now.
Make the UI readable but compact so users don't have to pan and scroll to see information at a glance.

UI Hints:
* Smaller padding and margins throughout
* Reduced font sizes while maintaining readability
* Horizontal header layout instead of centered vertical
* Cloud layers displayed inline instead of stacked
* Compact temperature displays
* Tighter grid spacing
* Limited height (400px) for diagnostic views with scrolling
* All key weather info visible at a glance without panning or scrolling

Implementation requirements:

1. In registerWidget, put `description` in the third argument (tool options), not the second (widget metadata). Only the third arg is exposed over MCP:
   registerWidget("name", { _meta: ... }, { description: "...", inputSchema: ..., annotations: ... }, handler)

2. Annotations: when readOnlyHint is true, set idempotentHint to false. idempotentHint is only meaningful for write operations; setting both to true is contradictory and fails MCP validation.

3. In middleware.ts, add two MCP spec checks before passing requests to the transport:
   - Origin validation (§2.0.1): if the Origin header is present and its host doesn't match the server host (use x-forwarded-host if set), return 403. Requests with no Origin header must be allowed through.
   - JSON-RPC validation (§2.1): verify the POST body is a non-null object with jsonrpc and method strings (or a non-empty array for batches). Return HTTP 400 for invalid bodies — the SDK transport returns 202 instead of an error status.
