// JAPAN NOW — Google AdSense banner configuration
// Hide preview-only mock ad banners during site review; keep AdSense verification tags on pages.
// Mock ads are not real advertising. The real AdSense site verification script remains in page headers.
window.JAPAN_NOW_ADSENSE = {
  enabled: false,
  mode: "preview",       // "preview" or "live" after AdSense approval
  client: "ca-pub-7823851906335189",            // actual ca-pub-... ID after approval
  slot: ""               // actual numeric AdSense ad unit slot ID
};
