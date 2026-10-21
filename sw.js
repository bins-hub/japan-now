/* JAPULSE reversible PWA test v1. No weather/video/analytics response caches. */
"use strict";
const CACHE="japulse-pwa-offline-v1";
const PREFIX="japulse-pwa-offline-";
self.addEventListener("install",event=>{
 event.waitUntil(caches.open(CACHE).then(c=>c.add("/offline.html")));
 self.skipWaiting();
});
self.addEventListener("activate",event=>{
 event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith(PREFIX)&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));
});
self.addEventListener("fetch",event=>{
 if(event.request.mode!=="navigate"||new URL(event.request.url).origin!==self.location.origin)return;
 event.respondWith(fetch(event.request).catch(async()=>await caches.match("/offline.html")||Response.error()));
});