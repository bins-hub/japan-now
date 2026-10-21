# JAPULSE concurrent viewer badge — activation checklist
This deployment ships an **inactive** UI component. It deliberately displays nothing until a verified live count endpoint exists. No visitor data is collected by the current badge.
To activate, operate a backend which tracks distinct active anonymous visitors, accounts for disconnects/timeouts, prevents automated count injection and exposes a public read-only HTTPS JSON endpoint with CORS enabled for https://japulse.com.
Example verified response: {"active": 28, "verified": true}; do not use fixed/sample counts as production responses.
Inject a script before /assets/presence.js setting window.JAPULSE_PRESENCE_ENDPOINT to your HTTPS endpoint URL. Restrict browser requests to this endpoint; keep authentication secrets and write endpoints server-side.
Realtime Firebase implementation option: Firebase Realtime Database Presence (onDisconnect, auth, restrictive security rules) plus Cloud Function aggregating distinct active user IDs. Configure authentication, CORS, App Check, privacy notice and rate limits before enabling.
Disable by deleting the endpoint configuration line, or remove /assets/presence.js from pages. Existing site layout and analytics are unaffected.
