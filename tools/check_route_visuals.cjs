"use strict";
const fs=require("node:fs");
const path=require("node:path");
const root=path.resolve(__dirname,"..");
const ids=["tokyo","osaka","kyoto","kyushu","hokkaido","okinawa"];
const langs=["","en/","ja/","zh-cn/"];
const js=fs.readFileSync(path.join(root,"assets/run-route-visuals.js"),"utf8");
const css=fs.readFileSync(path.join(root,"assets/run-route-visuals.css"),"utf8");
const errs=[];
for(const id of ids){
  const pattern=new RegExp("\\b"+id+": \\{kind:\"(loop|return)\", d:\"([^\"]+)\"");
  const match=js.match(pattern);
  if(!match){errs.push("Missing animated path: "+id);continue;}
  const nums=[...match[2].matchAll(/-?\d+(?:\.\d+)?/g)].map(x=>Number(x[0]));
  if(nums.length<8||Math.abs(nums[0]-nums.at(-2))>0.001||Math.abs(nums[1]-nums.at(-1))>0.001)errs.push("Route does not return to its starting point: "+id);
}
for(const lang of langs){
  const file=lang+"run-eat/index.html";
  const html=fs.readFileSync(path.join(root,file),"utf8");
  if(!html.includes('href="/assets/run-route-visuals.css?v=20261027-c1"'))errs.push("Missing route CSS in "+file);
  if(!html.includes('src="/assets/run-route-visuals.js?v=20261027-c1"'))errs.push("Missing animated route JS in "+file);
  for(const id of ids)if(!html.includes('id="'+id+'"'))errs.push("Missing course "+id+" in "+file);
  const canonical=(html.match(/<link rel="canonical" href="([^"]+)"/)||[])[1];
  if(canonical!=="https://japulse.com/"+lang+"run-eat/")errs.push("Canonical changed: "+file);
  if((html.match(/<link rel="alternate" hreflang=/g)||[]).length!==5)errs.push("Hreflang count changed: "+file);
  if((html.match(/<h1(?:\s[^>]*)?>/g)||[]).length!==1)errs.push("H1 changed: "+file);
}
for(const token of ["requestAnimationFrame","getPointAtLength","prefers-reduced-motion","IntersectionObserver","aria-label","t.complete"])if(!js.includes(token))errs.push("Missing animation/accessibility feature: "+token);
if(!css.includes("jp-route-animated"))errs.push("Missing scoped route CSS");
if(errs.length){for(const e of errs)console.error("FAIL",e);process.exit(1);}
console.log("PASS: 6 closed animation paths and 4 language pages; accessibility, links, canonicals and hreflang present.");
console.log("Route drawings are conceptual sketches, not surveyed GPS navigation tracks.");
