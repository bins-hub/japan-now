'use strict';
// Korean is the single structure/data source for ONSEN and MOVE.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),langs=['en','ja','zh-cn'];
function walk(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(dir,e.name)):e.name==='index.html'?[path.join(dir,e.name)]:[])}
const selectors=['h2','h3','section','article','table','thead','tbody','tr','th','td','details','summary','select','option','input','button','img'];
const images=h=>[...h.matchAll(/<img\b[^>]*\bsrc="([^"]+)"/g)].map(m=>m[1]);
const data=h=>[...h.matchAll(/\bdata-(?:price|private|filter|airport|one-route|move-entry)="([^"]+)"/g)].map(m=>m[0]);
let compared=0;
for(const family of ['onsen','move'])for(const source of walk(path.join(root,family))){
 const relative=path.relative(root,source),ko=fs.readFileSync(source,'utf8');
 for(const lang of langs){
  const file=path.join(root,lang,relative),html=fs.readFileSync(file,'utf8');
  for(const tag of selectors){const regex=new RegExp('<'+tag+'\\b','g');assert.equal((html.match(regex)||[]).length,(ko.match(regex)||[]).length,lang+'/'+relative+' '+tag+' count differs from Korean');}
  assert.deepEqual(images(html),images(ko),lang+'/'+relative+' must use the same images in the same order');
  assert.deepEqual(data(html),data(ko),lang+'/'+relative+' numeric/control data differs');
  const visible=html.replace(/<script\b[^>]*>[\s\S]*?<\/script>|<style\b[^>]*>[\s\S]*?<\/style>/g,'').replace(/<[^>]+>/g,'');
  assert.ok(!/[가-힣]/.test(visible),lang+'/'+relative+' untranslated Korean visible text');
  for(const script of html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g))assert.ok(!/[가-힣]/.test(script[1]),lang+'/'+relative+' untranslated dynamic/structured text');
  compared++;
 }
}
console.log(`PASS Korean-source parity: ${compared} localized ONSEN/MOVE pages; section/table/card/control counts, image order, numeric control data and translated static/dynamic text.`);
console.log('This does not certify third-party stream/image availability or mobile rendering.');
