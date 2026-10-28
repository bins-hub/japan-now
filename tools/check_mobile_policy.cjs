'use strict';
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const xml=fs.readFileSync(path.join(root,'sitemap.xml'),'utf8');
const urls=[...xml.matchAll(/<loc>(https:\/\/japulse\.com\/[^<]*)<\/loc>/g)].map(m=>m[1]);
const errors=[];
const core=['/','/live/','/now/','/run-eat/','/local-food/','/season/','/onsen/','/move/'];
const policies=['/about/','/privacy/','/contact/'];
for(const target of [...core,...policies])if(!urls.includes('https://japulse.com'+target))errors.push('Missing sitemap page '+target);
for(const url of urls){
 const pathname=new URL(url).pathname;
 const file=path.join(root,pathname.endsWith('/')?pathname.slice(1)+'index.html':pathname.slice(1));
 if(!fs.existsSync(file))continue;
 const html=fs.readFileSync(file,'utf8');
 if(!/name="viewport"[^>]*width=device-width/i.test(html))errors.push(pathname+' viewport missing');
 if(/width\s*:\s*(?:1[2-9]\d\d|[2-9]\d{3,})px/.test(html))errors.push(pathname+' very wide fixed CSS width; review responsive layout');
 if(core.includes(pathname)){
  for(const p of policies){if(!html.includes('href="'+p+'"')&&!html.includes('href="https://japulse.com'+p+'"'))errors.push(pathname+' missing policy navigation '+p);}
 }
}
if(errors.length){console.error(errors.slice(0,60).join('\n'));process.exitCode=1;}else console.log('PASS responsive baseline and site policy links across '+urls.length+' sitemap pages');