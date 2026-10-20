# JAPAN NOW: live-first monetization workflow

Main priority: embedded live camera → running route → verified local restaurants → optional relevant booking links. The player is never covered with popup ads.

### Affiliate setup (approval required)

`assets/affiliate-config.js` contains empty arrays for Korean, English, Chinese and Japanese. Add links ONLY when the respective affiliate partner has approved the website and issued the correctly tracked HTTPS link. Example syntax exists in the file. Put `city: 'osaka'` or `city: 'all'` for broad travel utilities. Affiliate cards stay hidden by default. `assets/affiliate.js` adds rel=sponsored and a clear disclosure. Do not label untracked links as commissions or claim bookings happened.

### Ads and content quality

Keep monetization below the player and RUN & EAT section, where it does not block the camera. AdSense is not configured until the site is approved. Restaurant information must be periodically reviewed for closure/hours. Search/maps buttons are not affiliate links.

### Key official local guide references
- Osaka Castle run 2.9/3.5 km: https://www.osakacastlepark.jp/images/sports/jogging/map.pdf
- Kyoto Kamogawa run 2.5/4.3/9.2 km: https://www.city.kyoto.lg.jp/bunshi/page/0000160807.html
- Tokyo Imperial Palace run roughly 5 km: https://www.gotokyo.org/jp/story/guide/running-course-guide-for-runners/index.html

### Reversible demo banners (visible for UI test)

The demonstration banner module is **separate from approved affiliate links**. It renders
three responsive mockup cards (Klook travel activities, Agoda hotels, Airalo eSIM)
on the four-language homepages and RUN & EAT pages, below the core live/running/food content.
Each card opens the brand's general official website **without a referral tracking code**.
The UI clearly labels these as *demo only, not approved partnerships*. No commission is earned.

**Disable all demo banners instantly** by changing `window.JAPAN_NOW_SHOW_DEMO_BANNERS = true;`
to `false;` in `assets/demo-banners-config.js` and committing to `main`.
The banner sections are empty and invisible when disabled; no original site content is touched.
`assets/demo-banners.js` and `assets/demo-banners.css` contain only the demo UI.
Per-page Close buttons temporarily hide the demonstration on the open page.

When legitimate affiliate links are issued later, enter them only into
`assets/affiliate-config.js`; the separate existing affiliate module handles attribution disclosure.


UPDATE: the old affiliate mockup banners were replaced with Google AdSense demo placements. See README_ADSENSE.md. No real AdSense publisher or unit ID is configured yet.
