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

## Widget Development Requirements (CRITICAL for ChatGPT compatibility)
- All styling MUST use React inline styles (style prop) only - NO external CSS files or CSS modules
- DO NOT import any CSS files into widget components
- All theme-aware styling must use the useLayout() hook for dark/light mode
- Widget must handle missing/null data gracefully with error states
- Always include isPending and error handling states

## CSP Configuration (CRITICAL for ChatGPT Developer Mode)
- **Resource Domains**: Explicitly list ALL external domains for images, fonts, or static resources that the widget loads (use https:// protocol)
- **Connect Domains**: List domains for client-side API calls made FROM the widget (leave empty if API calls are server-side only)
- **Frame Domains**: List domains if embedding iframes (leave empty if none)
- **Example**: If widget displays weather icons from api.weather.gov, add `resourceDomains: ["https://api.weather.gov"]`
