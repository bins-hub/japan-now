'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const flush=()=>new Promise(resolve=>setImmediate(resolve));
async function check(lang,missing){
 const node=key=>({key,nodeType:1,isConnected:true,dataset:{},getAttribute(){return key},matches(){return true},querySelectorAll(){return []}});
 const first=node('shibuya'),timers=new Map(),cache=new Map(),observed=[];let next=0,intersection,mutation,requests=0;
 const context={AbortController,Intl,Date,Number,Map,Set,WeakSet,Promise,
 document:{documentElement:{lang},body:{},visibilityState:'visible',querySelectorAll(s){return s==='[data-jp-weather]'?[first]:[]}},
 localStorage:{getItem:k=>cache.get(k)||null,setItem:(k,v)=>cache.set(k,v)},
 setTimeout(fn){timers.set(++next,fn);return next},clearTimeout:id=>timers.delete(id),setInterval(){},
 IntersectionObserver:class{constructor(fn){intersection=fn}observe(el){observed.push(el)}unobserve(){}},
 MutationObserver:class{constructor(fn){mutation=fn}observe(){}},
 fetch(url,options){requests++;if(url.includes('35.6595'))return Promise.resolve({ok:true,json:()=>Promise.resolve({properties:{timeseries:[{time:new Date().toISOString(),data:{instant:{details:{air_temperature:11}},next_1_hours:{summary:{symbol_code:'cloudy'}}}}]}})});
 return new Promise((resolve,reject)=>options.signal.addEventListener('abort',()=>reject(new Error('aborted'))));}
 };
 context.window={IntersectionObserver:context.IntersectionObserver};vm.createContext(context);
 vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/weather.js'),'utf8'),context);
 assert.ok(observed.includes(first));intersection([{isIntersecting:true,target:first}]);await flush();
 assert.equal(first.textContent,'☁️ 11°C');assert.equal(timers.size,0);
 const replacement=node('shibuya');mutation([{addedNodes:[replacement]}]);
 assert.ok(observed.includes(replacement),'dynamically inserted search result is observed');
 intersection([{isIntersecting:true,target:replacement}]);await flush();
 assert.equal(replacement.textContent,'☁️ 11°C');assert.equal(requests,1,'same place reuses cached forecast');
 const keys=['fuji','sapporo','hakata','arashiyama'];const pending=keys.map(node);
 for(const target of pending){mutation([{addedNodes:[target]}]);intersection([{isIntersecting:true,target}]);}
 assert.equal(requests,4,'only three provider requests run concurrently');
 [...timers.values()][0]();await flush();
 assert.equal(pending[0].textContent,'—°');assert.equal(pending[0].title,missing);
 assert.equal(requests,5,'timeout releases queue slot for the fourth weather request');
}
(async()=>{for(const [lang,missing] of [['ko','날씨 정보 없음'],['en','Weather unavailable'],['ja','天気情報なし'],['zh-CN','天气暂不可用']])await check(lang,missing);console.log('PASS weather: four languages, dynamic search cards, shared cache, request timeout and queue recovery.');})().catch(e=>{console.error(e);process.exitCode=1});
