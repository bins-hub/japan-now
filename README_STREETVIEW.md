# Embedded Street View setup

JAPAN NOW already includes the modal, locations, route cards and translations, but a Google Maps Embed API key has not been connected yet. The modal will show a transparent setup placeholder and a working outbound Google Street View link until the key is present.

1. In Google Cloud, select or create a project and link a billing account.
2. Enable **Maps Embed API** and create a browser API key.
3. Restrict the key to the Maps Embed API and **HTTP referrer** `https://bins-hub.github.io/*` (add your custom domain if applicable).
4. In `assets/maps-config.js`, fill in `window.JAPAN_NOW_MAPS_EMBED_KEY = "YOUR_KEY";` and commit to main.
5. After GitHub Pages deployment, use the 360° buttons to inspect a panorama inside JAPAN NOW. Some places may not have nearby imagery. Do not use an unrestricted key.

Google Maps Embed API currently charges nothing for unlimited embed requests but requires an API key with Google Cloud billing enabled. The YouTube live-camera player is separate and unchanged.

Docs: https://developers.google.com/maps/documentation/embed/quickstart and https://developers.google.com/maps/documentation/embed/embedding-map#streetview_mode
