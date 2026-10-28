'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),vm=require('node:vm');
const root=path.resolve(__dirname,'..'),prefixes=['en/','ja/','zh-cn/'];
const urls=[...fs.readFileSync(path.join(root,'sitemap.xml'),'utf8').matchAll(/<loc>([^<]+)<\/loc>/g)].map(m=>m[1]);
let anchors=0,scripts=0;
for(const url of urls){
 const route=new URL(url).pathname.slice(1),prefix=prefixes.find(p=>route.startsWith(p))||'',base=route.slice(prefix.length);
 const html=fs.readFileSync(path.join(root,route+'index.html'),'utf8');
 const langs=[...html.matchAll(/<link\b[^>]*hreflang="([^"]+)"/g)].map(m=>m[1]);
 assert.deepEqual(new Set(langs),new Set(['ko','en','ja','zh-CN','x-default']),url+' must expose reciprocal language metadata');
 let body=html;
 const languageNav=/<nav\b(?=[^>]*(?:class="(?:jp-lang|langs)"|aria-label="Language"))[^>]*>[\s\S]*?<\/nav>/g;
 if(base)assert.equal((body.match(languageNav)||[]).length,0,url+' internal language picker');
 else {assert.equal((body.match(languageNav)||[]).length,1,url+' homepage language picker');body=body.replace(languageNav,'');}
 if(prefix)for(const m of body.matchAll(/<a\b[^>]*href="([^"]+)"/g)){
  const u=new URL(m[1].replaceAll('&amp;','&'),url);
  if(u.origin!=='https://japulse.com'||!u.pathname.endsWith('/'))continue;
  anchors++;assert.ok(u.pathname.startsWith('/'+prefix),url+' escapes language: '+u.href);
 }
 for(const m of html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/g)){
  if(/src=|application\/ld\+json/.test(m[1])||!m[2].trim())continue;
  new vm.Script(m[2],{filename:route+'index.html'});scripts++;
 }
}
const homeIds=[];
for(const p of ['',...prefixes]){
 const html=fs.readFileSync(path.join(root,p+'index.html'),'utf8');
 homeIds.push(html.match(/data-video-id="([^"]+)"/)[1]);
 assert.ok(html.includes('home-live.js?v=20261028-audit')||p==='',p+' camera selector cache version');
 const menu=html.match(/<nav class="jp-menu"[^>]*>([\s\S]*?)<\/nav>/)[1];
 for(const section of ['live','now','run-eat','local-food','season','onsen','move'])assert.ok(menu.includes('/'+p+section+'/'),p+' missing menu '+section);
}
assert.equal(new Set(homeIds).size,1,'All homepages must start with the same camera');
console.log(`PASS locale navigation: ${urls.length} pages; ${anchors} localized anchors; ${scripts} inline scripts; homepage-only language pickers and camera/menu parity.`);
