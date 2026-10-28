'use strict';
const fs = require('node:fs');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const routes = ['tokyo-hakone','osaka-kyoto','shinjuku-kawaguchiko','kyoto-nara','osaka-kobe','sapporo-otaru','tokyo-kamakura','osaka-nara','kyoto-arashiyama'];
const airportRoutes = ['narita-shinjuku','haneda-shinagawa','kansai-namba','narita-ueno','haneda-hamamatsucho','kansai-kyoto','kansai-shin-osaka','new-chitose-sapporo'];
const read = path => fs.readFileSync(path,'utf8');
const home = read('move/index.html');
const sitemap = read('sitemap.xml');
function uniqueIds(html, path) {
  const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
  assert.equal(new Set(ids).size,ids.length,path+' has duplicate IDs');
}
function scriptsValid(html,path) {
  const all=[...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)];
  for(const [i,item] of all.entries()){
    if(/application\/ld\+json/.test(item[1])){JSON.parse(item[2]);continue;}
    if(/\bsrc=/.test(item[1]))continue;
    new vm.Script(item[2],{filename:path+':script'+i});
  }
  assert.equal((html.match(/<script\b/gi)||[]).length,all.length,path+' unbalanced script tags');
}
uniqueIds(home,'MOVE home');
scriptsValid(home,'MOVE home');
for (const id of ['move-route-finder','move-unified','move-step-guide','move-compare','move-planner']) {
  assert.ok(home.includes('id="'+id+'"'),'missing main feature: '+id);
}
assert.equal((home.match(/class="card move-finder-card"/g)||[]).length,9,'expected nine discovery cards');
assert.equal((home.match(/data-one-route="/g)||[]).length,9,'expected nine unified routes');
assert.equal((home.match(/data-move-compare-from="/g)||[]).length,9,'expected nine comparison rows');
assert.equal((home.match(/data-airport="/g)||[]).length,8,'expected eight airport routes');
assert.ok(home.includes('move-finder-script')&&home.includes('move-one-script'),'missing client search/selector logic');
for(const slug of routes){
  const path='move/'+slug+'/index.html',html=read(path),url='https://japulse.com/move/'+slug+'/';
  uniqueIds(html,path);scriptsValid(html,path);
  assert.ok(html.includes('rel="canonical" href="'+url+'"'),path+' canonical missing');
  assert.ok(sitemap.includes('<loc>'+url+'</loc>'),path+' sitemap entry missing');
  assert.ok(home.includes('href="/move/'+slug+'/"'),path+' home card link missing');
  assert.ok(html.includes('id="move-practical-tips"'),path+' practical tips missing');
  assert.ok(html.includes('id="move-station-audit"'),path+' station audit missing');
  assert.ok(html.includes('id="move-related-guides"'),path+' related links missing');
  assert.ok(html.includes('"@type":"FAQPage"'),path+' FAQ schema missing');
}
for(const slug of airportRoutes){
 const path='move/'+slug+'/index.html',html=read(path),url='https://japulse.com/move/'+slug+'/';
 uniqueIds(html,path);scriptsValid(html,path);
 assert.ok(html.includes('rel="canonical" href="'+url+'"'),path+' canonical missing');
 assert.ok(sitemap.includes('<loc>'+url+'</loc>'),path+' sitemap entry missing');
 assert.ok(home.includes('href="/move/'+slug+'/"'),path+' MOVE internal link missing');
 assert.ok(html.includes('<title>') && html.includes('</title>'),path+' title missing');
 assert.ok(html.includes('name="description"'),path+' description missing');
 assert.ok(html.includes('google.com/maps/dir/'),path+' navigation map missing');
 assert.ok(html.includes('target="_blank" rel="noopener noreferrer"'),path+' safe official link missing');
}
console.log('Airport SEO PASS: eight independent guides');
console.log('MOVE integrity PASS: 9 destination pages, 8 airport routes, scripts, SEO, internal navigation');
