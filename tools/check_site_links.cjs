'use strict';
// JAPULSE same-origin links and foreign-language route integrity.
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const xml=fs.readFileSync(path.join(root,'sitemap.xml'),'utf8');
const pages=new Set([...xml.matchAll(/<loc>(https:\/\/japulse\.com\/[^<]*)<\/loc>/g)].map(m=>new URL(m[1]).pathname));
const failures=[];let links=0,foreign=0;
const fileFor=p=>path.join(root,p.endsWith('/')?p.slice(1)+'index.html':p.slice(1));
for(const page of pages){
 const file=fileFor(page);
 if(!fs.existsSync(file)){failures.push(page+' missing file');continue;}
 const html=fs.readFileSync(file,'utf8');
 if(/^\/(?:en|ja|zh-cn)\//.test(page))foreign++;
 for(const match of html.matchAll(/\b(?:href|src)=["']([^"'<>]+)["']/g)){
  const raw=match[1].replace(/&amp;/g,'&');let u;
  try{u=new URL(raw,'https://japulse.com'+page);}catch{failures.push(page+' malformed URL '+raw);continue;}
  if(u.hostname!=='japulse.com'||!['http:','https:'].includes(u.protocol))continue;
  if(u.protocol!=='https:')failures.push(page+' insecure same-origin URL '+raw);
  const target=u.pathname;const isAsset=/\.(?:css|js|png|jpe?g|webp|svg|gif|ico|xml|json|webmanifest|pdf|txt|woff2?|mp4)$/i.test(target);
  if(target==='/'||target===page&&u.hash==='') {links++;continue;}
  if(isAsset){if(!fs.existsSync(path.join(root,target.slice(1))))failures.push(page+' missing asset '+raw);}
  else if(target.endsWith('/')){if(!pages.has(target))failures.push(page+' unlisted page '+raw);}
  else if(!fs.existsSync(path.join(root,target.slice(1))))failures.push(page+' missing path '+raw);
  if(u.hash&&target.endsWith('/')&&pages.has(target)){
   const frag=decodeURIComponent(u.hash.slice(1));
   if(frag&&!fs.readFileSync(fileFor(target),'utf8').includes('id="'+frag+'"')&&!fs.readFileSync(fileFor(target),'utf8').includes("id='"+frag+"'"))failures.push(page+' missing anchor '+raw);
  }
  links++;
 }
}
if(failures.length){console.error('FAIL same-origin links: '+failures.length);for(const e of failures.slice(0,100))console.error(e);process.exitCode=1;}
else console.log('PASS same-origin links: '+pages.size+' indexed pages; '+foreign+' localized pages; '+links+' links/assets/anchors checked');
