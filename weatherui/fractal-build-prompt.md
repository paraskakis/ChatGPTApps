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

## CRITICAL CHATGPT COMPATIBILITY RULES

These rules are NON-NEGOTIABLE. Violating ANY of them will cause blank widgets in ChatGPT:

1. **NO CSS IMPORTS** - Never `import` any CSS file in widget components. Use ONLY inline `style` props.

2. **Widget filename MUST match tool name exactly** - Use kebab-case (hyphens):
   - Tool: "get-weather" → File: `web/src/widgets/get-weather.tsx`

3. **Handle all 3 states explicitly**:
   ```tsx
   if (isPending) return <div style={{padding:"16px"}}>Loading...</div>;
   if (!output || output.error) return <div style={{padding:"16px",color:"red"}}>Error</div>;
   return <div style={{padding:"16px"}}>...content...</div>;
