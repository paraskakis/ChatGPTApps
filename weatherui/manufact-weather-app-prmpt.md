Build an MCP app that displays the current weather conditions for a specific United States airport using the National Weather Service API.

API documentation:
https://api.weather.gov/openapi.json

Use only this endpoint:
GET https://api.weather.gov/stations/{stationid}/observations/latest

The `stationid` path parameter is a four-letter ICAO airport code, such as `KJFK`, `KLAX`, or `KSEA`.

Important API response-shape requirement:

The endpoint returns a GeoJSON `Feature` object. The weather observation is not stored at the top level of the response. It is nested under `properties`.

Use the equivalent of:
const payload = await response.json();

const observation = payload.properties;


Do not read weather fields directly from `payload`. Read them from `payload.properties`.

Read and map the following fields from `payload.properties`:

- `station` — station URI
- `stationName` — airport or station name
- `timestamp` — observation timestamp
- `textDescription` — current weather conditions
- `temperature.value` — temperature in degrees Celsius
- `dewpoint.value` — dew point in degrees Celsius
- `windSpeed.value` — wind speed in kilometers per hour
- `windDirection.value` — wind direction in degrees
- `visibility.value` — visibility in meters
- `relativeHumidity.value` — relative humidity percentage
- `barometricPressure.value` — barometric pressure in Pascals

The nested measurement values may be `null`. Handle null values gracefully. Do not throw errors, render empty fields, or display misleading zero values when a measurement is unavailable. Use `Unavailable` or an equivalent clear label.

Implementation requirements:

1. Create an MCP server tool named `get-airport-weather`.

2. The tool must accept one input:
   - `icao`: a four-letter ICAO airport code.

3. Normalize the input by:
   - trimming leading and trailing whitespace
   - converting it to uppercase

4. Validate that the normalized input contains exactly four alphabetic characters. Return a helpful MCP error result for invalid input.

5. Request:
   `https://api.weather.gov/stations/${icao}/observations/latest`

6. Include an appropriate `User-Agent` HTTP header when calling the NWS API. Use a descriptive application identifier and contact address if configuration allows it.

7. Check `response.ok`. If the request fails, return a helpful expected-error MCP result containing a concise explanation. Do not attempt to parse a failed response as a successful observation.

8. Parse the response as JSON and explicitly access the observation through:
   `payload.properties`

9. Return a standard MCP result envelope:
   - `content` containing concise, model-readable text
   - `structuredContent` containing typed data for the View
   - `outputSchema` matching the exact structure of `structuredContent`

10. The structured result should contain normalized, UI-ready fields such as:
    - `icao`
    - `station`
    - `stationName`
    - `timestamp`
    - `textDescription`
    - `temperatureC`
    - `dewPointC`
    - `windSpeedKmh`
    - `windDirectionDegrees`
    - `visibilityMeters`
    - `relativeHumidityPercent`
    - `barometricPressurePa`

    Nullable API measurements should remain `number | null` in the structured result. Do not convert missing values to zero.

11. Bind the tool to this View:
    `view: { name: "airport-weather" }`

12. Create the View at exactly:
    `views/airport-weather/view.tsx`

13. In the View, use the typed tool context:
    `useToolContext<"get-airport-weather">()`

14. Handle all View states:
    - pending/loading
    - successful result
    - tool error
    - missing or incomplete result data

15. Build a compact, readable single weather card. It should display:
    - airport ICAO code
    - station name
    - current conditions
    - temperature
    - dew point
    - wind speed and direction
    - visibility
    - humidity
    - pressure
    - observation time

16. Keep the layout compact enough to fit at a glance without horizontal panning or unnecessary scrolling. Use a responsive layout that remains readable at narrow widths.

17. Format values for people:
    - temperatures with `°C`
    - wind speed with `km/h`
    - wind direction with `°`
    - visibility with `m` or a readable converted unit
    - humidity with `%`
    - pressure with `Pa` or another clearly labeled unit
    - timestamp as a readable date and time, including the timezone or UTC label

18. Use clear labels and accessible text. Ensure sufficient color contrast and do not communicate information by color alone.

19. Do not assume the NWS response is flat anywhere in the implementation. Keep the API parsing boundary explicit and separate from the UI mapping boundary.

20. Make sure the development server configuration includes:
    `cors: { origin: "*" }`

21. Use current mcp-use APIs:
    - import server APIs from `mcp-use`
    - import React View APIs from `mcp-use/react`
    - use `inputSchema`, not a legacy tool `schema`
    - return raw MCP result objects
    - export the View-bound tool reference
    - default-export the MCP server
    - do not use legacy widget APIs, `useWidget`, `McpUseProvider`, or a `resources/` widget path

Verification requirements:

1. Inspect the existing project structure and installed mcp-use version before choosing APIs.
2. Verify that the tool compiles successfully.
3. Run the project's type check or lint command and fix all errors.
4. List the exposed MCP tools.
5. Call `get-airport-weather` with a valid airport code such as `KJFK` and verify that:
   - the request succeeds
   - the returned data is populated
   - the values come from `payload.properties`
   - `structuredContent` matches `outputSchema`
6. Test invalid input such as `JFK`, `KJFK1`, or `ABC` and verify that the tool returns a helpful error.
7. Test or account for nullable NWS measurement values and verify that the UI displays `Unavailable` rather than blank or zero values.
8. Render the View through a natural-language request that asks for the current weather at KJFK.
9. Check the rendered View for runtime errors and confirm that the intended airport weather card is displayed rather than a starter placeholder.
10. Enable Widget-Declared CSP mode before rendering the View.
11. Run the CSP audit after rendering. If it reports blocked external origins, add only the exact required origins to the View's declared CSP and re-test.
12. Do not consider the implementation complete until compilation, type checking, tool execution, View rendering, runtime checks, and the Widget-Declared CSP audit all pass.
