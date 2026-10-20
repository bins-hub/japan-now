# JAPAN NOW — Google AdSense banner layout and activation

The site contains ONE responsive AdSense placement on each of 4 localized homepages and 4 localized RUN & EAT pages, **after** the primary live video and running/restaurant content. Existing YouTube camera embeds stay untouched.

## Preview (current mode)
File: `assets/adsense-config.js`.

```js
window.JAPAN_NOW_ADSENSE = {
  enabled: true,
  mode: "preview",
  client: "",
  slot: ""
};
```

- Preview renders a grey responsive banner marked `AD · preview` / `광고 · 데모`.
- It does **not** contact Google's ad servers, show paid advertisements, or earn income. Visitors can close that preview.
- To remove **all** AdSense preview banners without editing pages, set `enabled: false` and commit to main.

## Real ads, only once approved
1. Sign up for Google AdSense and submit the JAPAN NOW site for approval.
2. After approval, obtain the actual `ca-pub-...` publisher client ID and numeric ad unit slot ID in the AdSense dashboard.
3. Set `mode: "live"`, and fill `client` and `slot` in `assets/adsense-config.js`. **Never invent IDs**.
4. Commit, wait for GitHub Pages deployment, then confirm ad serving and consent/cookie/privacy requirements for target countries. Ad blockers, account readiness, ad inventory and consent settings can affect visibility.
5. An AdSense script and responsive `<ins class="adsbygoogle">` are loaded **only** with real-looking configured IDs in live mode. Even then, actual ad delivery depends on Google's approval and serving.
6. Keep ad labels distinct from live-camera playback controls and do not induce clicks. Local legal disclosure/consent requirements may apply.

Affiliate banners and their code are not loaded. Existing affiliate config is left unused and the demo affiliate assets have been deleted.

Design notes: one nonsticky inline responsive ad placement per eligible page; no overlay on live player. The gray placeholder's approximate desktop dimension is up to 980×125px (plus labels), with compact mobile layout.

Google reference: https://support.google.com/adsense/answer/9274015
