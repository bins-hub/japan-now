# JAPULSE multi-language content depth — 2026-10-27

## Scope and translation
- Expanded ten camera guides each in English, Japanese, and Simplified Chinese (30 detail pages).
- Unique location-specific **WATCH / RUN / EAT** text for every locale, with 3-step itineraries and cautions about what the camera can and cannot prove.
- Each localized guide links to the matching-language RUN & EAT and local food pages, a map search and the official source already cited on the camera page.
- New blocks are inserted after existing location-specific guides and before the related camera suggestions.
- Existing primary video players, camera sources, weather, ads, page headings, canonical URLs, hreflang tags and navigation were intentionally not changed.
- Reuses existing scoped responsive CSS `assets/experience-path.css`.

## Verification performed
- All 30 pages were fetched from the feature branch. Each has one new guide, one H1, a CSS reference, the old place guide and localized RUN/EAT links.
- For each page, div open/close counts are balanced in the resulting HTML.
- No pages were added; previously indexed URLs remain intact. GitHub Pages deployment still requires its normal run.
- Text describes location planning, but no access to a camera's current LIVE status, restaurant operating status, crowd estimates, or in-person route verification is claimed.
- Native-speaker editorial review and mobile screenshot checks are separate future quality gates, and AdSense approval is not guaranteed.

## Branches and rollback
- Original main before this phase: `f320d93869f423624315ab2cbd9fe1ec0a53c678`.
- Recovery branch: `backup/pre-multilingual-depth-20261027`.
- Feature branch: `feature/multilingual-depth-20261027`.

## Recommended next actions
- Inspect representative mobile pages, especially Haneda's alternative template.
- Review all localized copy with a fluent reviewer before major promotion.
- Prioritize original regional restaurant/route research, not unverified new claims.
- Check Google Search Console language and canonical coverage and monitor organic landings.
