'use strict';
// Validate internal hyperlinks across sitemap-listed HTML, including cross-section discovery.
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const xml=fs.readFileSync(path.join(root,'sitemap.xml'),'utf8');
const urls=[...xml.matchAll(/<loc>(https:\/\/japulse\.com\/[^<]*)<\/loc>/g)].map(m=>m[1]);
const pages=new Set(urls.map(u=>new URL(u).pathname));
const failures=[];
let checked=0;
for(const pathname of pages){
 const file=path.join(root,pathname.endsWith('/')?pathname.slice(1)+'index.html':pathname.slice(1));
 if(!fs.existsSync(file))continue;
 const html=fs.readFileSync(file,'utf8');
 for(const match of html.matchAll(/\bhref="(\/[^"]*)"/g)){
   const href=match[1];
   if(href.startsWith('//'))continue;
   const target=href.split(/[?#]/,1)[0];
   if(!target||target==='/')continue;
   if(/\.(?:css|js|png|jpg|jpeg|webp|svg|gif|ico|xml|json|webmanifest|pdf|txt|woff2?)$/i.test(target)){
     const asset=path.join(root,target.slice(1));if(!fs.existsSync(asset))failures.push(pathname+' missing asset '+target);
   }else if(target.endsWith('/')){
     if(!pages.has(target))failures.push(pathname+' unlisted internal page '+target);
   }
   checked++;
 }
}
if(failures.length){console.error(failures.slice(0,30).join('\n'));process.exitCode=1;}
else console.log('PASS sitewide internal navigation: '+pages.size+' pages; '+checked+' internal links checked');