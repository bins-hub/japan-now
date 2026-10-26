# JAPULSE validation — 2026-10-26

## Coverage

- All 116 public sitemap pages rendered at 390px and 1366px viewport widths (232 cases).
- Checked text contrast on solid backgrounds, horizontal overflow, clipped text, missing control labels, image alternatives and failed image loads. Gradient backgrounds were excluded from automated contrast scoring and inspected separately on representative page families.
- The 65 cases with findings were rechecked against fresh deployed HTML after corrections; all 65 passed with no remaining findings in those checks.
- All 119 HTML source files checked for missing internal files and fragment targets: none found. No duplicate IDs found.
- All 116 public pages have one H1, a description, a matching canonical URL and no unintended noindex directive.
- 67 production inline/external JavaScript blocks passed syntax checks; 117 JSON-LD blocks parsed successfully.

## Corrections

- Darkened localized camera-card labels and camera action buttons that were difficult to read against their backgrounds.
- Added a local SVG fallback when third-party YouTube thumbnails fail to load.
- Added a 20-second startup watchdog to the shared video player and a pre-ready watchdog to the homepage player, preventing an indefinite loading screen.
- Kept a localized original YouTube link available in the shared player, including error states.
- Refreshed asset URLs so older mobile caches do not retain the previous styles or scripts.

## Interaction checks

- Homepage search for Osaka opens the nationwide directory with the query applied.
- Regional filtering changes the camera results; expanding Kanto shows 14 camera entries.
- Homepage camera selection updates the selected state, camera name and original-source link.
- Failed homepage thumbnails successfully load the local fallback image.
- The shared player displays recovery controls and its original-source link after a stalled startup.
- `node tools/check_player_fallbacks.cjs` passes in Korean, English, Japanese and Simplified Chinese: playback success, stalled startup, stale callback protection, source-link persistence and teardown.

## Limits

- These are browser viewport checks, not tests on every physical phone or browser.
- Third-party broadcasts can end, restrict embedding or fail in this browsing environment. This validation does not certify that all listed videos are currently live. It checks the site's recovery behavior as well as the accessible original-source route.
- This does not certify approval by Google AdSense or inclusion in Google's index.

## Recovery

The pre-validation version is preserved at `backup/before-full-validation-20261026` (`b05411b22e33a5450167a62f1166bab37f9276fb`).
The temporary noindex viewport-validation page is removed after the final checks.
