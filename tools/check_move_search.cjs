'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
function field(value=''){return {value,hidden:false,handlers:{},addEventListener(event,fn){this.handlers[event]=fn},focus(){}}}
for(const [prefix,query,cityName] of [['','하코네','도쿄'],['en/','Hakone','Tokyo'],['ja/','箱根','東京'],['zh-cn/','箱根','东京']]){
 const html=fs.readFileSync(path.join(__dirname,'..',prefix,'move/index.html'),'utf8');
 const cards=[...html.matchAll(/<[^>]*class="[^"]*\bmove-finder-card\b[^>]*>/g)].map(m=>{const a=Object.fromEntries([...m[0].matchAll(/data-([\w-]+)="([^"]*)"/g)].map(x=>[x[1],x[2]]));return {dataset:{from:a.from,search:a.search},hidden:false}});
 assert.equal(cards.length,9);
 const fields={'move-finder-origin':field('all'),'move-finder-query':field(),'move-finder-status':field(),'move-finder-empty':field(),'move-finder-reset':field()};
 const script=html.match(/<script id="move-finder-script">([\s\S]*?)<\/script>/)[1];
 vm.runInNewContext(script,{document:{getElementById:id=>fields[id],querySelectorAll:()=>cards}});
 const visible=()=>cards.filter(c=>!c.hidden).length;assert.equal(visible(),9);
 for(const value of [query,query.toUpperCase(),'  '+query.toLowerCase()+'  ']){fields['move-finder-query'].value=value;fields['move-finder-query'].handlers.input();assert.equal(visible(),1,prefix+' case-insensitive native destination search');}
 fields['move-finder-query'].value='zzq-no-result';fields['move-finder-query'].handlers.input();assert.equal(visible(),0);
 fields['move-finder-reset'].handlers.click();assert.equal(visible(),9);
 fields['move-finder-origin'].value=cityName;fields['move-finder-origin'].handlers.change();assert.equal(visible(),3,prefix+' city filter');
}
console.log('PASS MOVE search: 4 languages, uppercase/lowercase/whitespace, no results, reset and city filtering.');
