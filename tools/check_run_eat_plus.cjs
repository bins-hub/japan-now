"use strict";
const fs=require("node:fs");
const path=require("node:path");
const root=path.resolve(__dirname,"..");
const ids=["tokyo","osaka","kyoto","kyushu","hokkaido","okinawa"];
const prefixes=["","en/","ja/","zh-cn/"];
const errors=[];
const check=(v,message)=>{if(!v)errors.push(message)};
const urls=[];
for(const prefix of prefixes){
  const file=prefix+"run-eat/index.html";
  const html=fs.readFileSync(path.join(root,file),"utf8");
  const href="https://japulse.com/"+prefix+"run-eat/";
  urls.push(href);
  check(html.includes('<link rel="canonical" href="'+href+'">'),"canonical "+file);
  check((html.match(/<link rel="alternate" hreflang=/g)||[]).length===5,"hreflang "+file);
  check(html.includes('id="jp-run-plan-mount"'),"planner placeholder "+file);
  check(html.includes('src="/assets/run-eat-plus.js?v=20261027-b1"'),"planner script "+file);
  check(html.includes('href="/assets/run-eat-plus.css?v=20261027-b1"'),"planner CSS "+file);
  check((html.match(/JAPULSE VERIFIED RUN START/g)||[]).length===6,"six static verified guides "+file);
  check((html.match(/JAPULSE VERIFIED RUN END/g)||[]).length===6,"six static verified guide ends "+file);
  for(const id of ids){
    check(html.includes('id="jp-proof-'+id+'"'),"route proof "+file+" "+id);
    check(html.includes('id="'+id+'"'),"route anchor "+file+" "+id);
  }
  check(!/<meta\b[^>]*content="[^"]*noindex/i.test(html),"unwanted noindex "+file);
}
const sitemap=fs.readFileSync(path.join(root,"sitemap.xml"),"utf8");
for(const url of urls)check(sitemap.includes("<loc>"+url+"</loc>"),"sitemap run-eat URL "+url);
for(const p of ["assets/run-eat-plus.css","assets/run-eat-plus.js","assets/run-route-visuals.js","assets/run-route-visuals.css"]){
 check(fs.existsSync(path.join(root,p)),"missing asset "+p);
}
for(const token of ["indicator.value=Math.round(f*100)","progress.setAttribute(\"stroke-dashoffset\"","r:\"23\",fill:\"#f3654d\""]){
 check(fs.readFileSync(path.join(root,"assets/run-route-visuals.js"),"utf8").includes(token),"animation progress: "+token);
}
check(fs.readFileSync(path.join(root,"assets/run-eat-plus.js"),"utf8").includes('weatherValue==="snow"'),"scenario-based weather selection");
if(errors.length){errors.forEach(e=>console.error("FAIL",e));process.exit(1);}
console.log("PASS 4 locales × 6 official source-backed course cards, itinerary controls, animation percent and index-safe URLs");
