"use strict";
// JAPULSE index guard. Static pre-deploy checks; Google Search Console remains the source of actual index status.
const fs = require("node:fs");
const path = require("node:path");
const root = path.resolve(__dirname, "..");
const read = p => fs.readFileSync(path.join(root, p), "utf8");
const errors = [];
const fail = message => errors.push(message);
const xml = read("sitemap.xml");
const robots = read("robots.txt");
if (!xml.includes('xmlns:xhtml="http://www.w3.org/1999/xhtml"')) fail("Missing xhtml namespace");
if (!robots.includes("Sitemap: https://japulse.com/sitemap.xml")) fail("robots.txt sitemap reference missing");
if (/Disallow:\s*\//i.test(robots)) fail("Unexpected broad robots Disallow");
const blocks = [...xml.matchAll(/<url>([\s\S]*?)<\/url>/g)].map(x => x[1]);
const sitemap = new Map();
for (const block of blocks) {
  const loc = (block.match(/<loc>([^<]+)<\/loc>/) || [])[1];
  const lastmod = (block.match(/<lastmod>([^<]+)<\/lastmod>/) || [])[1];
  if (!loc || !loc.startsWith("https://japulse.com/")) { fail("Bad sitemap loc: " + loc); continue; }
  if (sitemap.has(loc)) fail("Duplicate sitemap URL: " + loc);
  if (lastmod && !/^\d{4}-\d{2}-\d{2}$/.test(lastmod)) fail("Invalid lastmod: " + loc);
  const alternates = new Map();
  for (const m of block.matchAll(/<xhtml:link\b[^>]*hreflang="([^"]+)"[^>]*href="([^"]+)"[^>]*\/>/g)) {
    if (alternates.has(m[1])) fail("Duplicate sitemap hreflang for " + loc + " " + m[1]);
    alternates.set(m[1], m[2]);
  }
  sitemap.set(loc, { alternates, lastmod });
}
if (sitemap.size < 40) fail("Unexpectedly small sitemap");
const canonicalOf = html => [...html.matchAll(/<link\b[^>]*rel="canonical"[^>]*href="([^"]+)"/g)].map(x => x[1]);
const hreflangOf = html => {
  const map = new Map();
  for (const match of html.matchAll(/<link\b[^>]*rel="alternate"[^>]*hreflang="([^"]+)"[^>]*href="([^"]+)"/g)) {
    if (map.has(match[1])) fail("Duplicate page hreflang " + match[1]);
    map.set(match[1], match[2]);
  }
  return map;
};
const titleSet = new Set();
for (const [url, meta] of sitemap) {
  const pathname = new URL(url).pathname;
  const filename = pathname.endsWith("/") ? pathname.slice(1) + "index.html" : pathname.slice(1);
  const localPath = path.join(root, filename);
  if (!fs.existsSync(localPath)) { fail("Sitemap points at absent file: " + url); continue; }
  const html = fs.readFileSync(localPath, "utf8");
  const title = (html.match(/<title>([\s\S]*?)<\/title>/) || [])[1];
  if (!title || !title.trim()) fail("Missing title: " + url);
  if (!/<meta\s+name="description"\s+content="[^"]+"/.test(html)) fail("Missing meta description: " + url);
  const canonical = canonicalOf(html);
  if (canonical.length !== 1 || canonical[0] !== url) fail("Canonical must match URL: " + url + " got=" + canonical);
  if (/<meta\b[^>]*content="[^"]*noindex/i.test(html)) fail("Unexpected noindex: " + url);
  if ((html.match(/<h1(?:\s[^>]*)?>/g) || []).length !== 1) fail("H1 count not one: " + url);
  const alt = hreflangOf(html);
  if (alt.size !== meta.alternates.size) fail("Page/sitemap hreflang count mismatch: " + url);
  for (const [language, href] of meta.alternates) if (alt.get(language) !== href) fail("Wrong page hreflang " + language + " for " + url);
  for (const [language, href] of alt) if (!sitemap.has(href)) fail("Alternate missing from sitemap: " + url + " " + language + " " + href);
  for (const item of html.matchAll(/<script\s+type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    try { JSON.parse(item[1]); } catch (e) { fail("Invalid JSON-LD: " + url + " " + e.message); }
  }
}
const ids = ["shibuya", "dotonbori", "fuji", "arashiyama", "hakata", "sapporo", "kabukicho", "sensoji", "osaka-sky", "haneda"];
const languages = [{prefix:"", code:"ko"}, {prefix:"en/",code:"en"}, {prefix:"ja/",code:"ja"}, {prefix:"zh-cn/",code:"zh-CN"}];
const localeRoutes = {ko:"",en:"en/",ja:"ja/","zh-CN":"zh-cn/"};
for (const id of ids) {
  for (const l of languages) {
    const url = "https://japulse.com/" + l.prefix + "cameras/" + id + "/";
    const meta = sitemap.get(url);
    if (!meta) { fail("Key camera missing from sitemap: " + url); continue; }
    if (meta.alternates.size !== 5) fail("Key camera missing 5 hreflang entries: " + url);
    for (const [code, prefix] of Object.entries(localeRoutes)) if (meta.alternates.get(code) !== "https://japulse.com/" + prefix + "cameras/" + id + "/") fail("Wrong reciprocal language link: " + url + " " + code);
    const file = read(l.prefix + "cameras/" + id + "/index.html");
    if (!file.includes("JAPULSE TRIP DEPTH START")) fail("Travel guide missing: " + url);
    const name = (file.match(/<title>([\s\S]*?)<\/title>/) || [])[1];
    if (titleSet.has(name)) fail("Duplicate key-camera title: " + name);
    titleSet.add(name);
    const internalLinks = [...file.matchAll(/href="(\/(?:en\/|ja\/|zh-cn\/)?(?:run-eat|local-food)\/(?:#[^"]*)?)"/g)].map(x => x[1]);
    for (const href of internalLinks) {
      const [destination, fragment] = href.slice(1).split("#");
      const targetFile = path.join(root, destination, "index.html");
      if (!fs.existsSync(targetFile)) { fail("Internal guide link points to absent page: " + url + " " + href); continue; }
      if (fragment && !fs.readFileSync(targetFile, "utf8").includes('id="' + fragment + '"')) fail("Missing guide anchor: " + url + " " + href);
    }
  }
}
if (errors.length) {
  console.error("Index integrity FAIL: " + errors.length + " issues");
  for (const e of errors) console.error(" - " + e);
  process.exitCode = 1;
} else {
  console.log("Index integrity PASS: " + sitemap.size + " sitemap URLs, " + (ids.length * languages.length) + " multilingual priority camera pages.");
  console.log("Checked canonical, noindex, title, description, H1, JSON-LD, sitemap hreflang, reciprocal locales and priority internal guide links.");
  console.log("Note: static checks cannot guarantee Google indexing or live broadcast/HTTP availability.");
}
