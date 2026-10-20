/*
 * JAPULSE live-region weather badges (short-range forecast, NOT observed temperature).
 * Source: Norwegian Meteorological Institute (MET Norway) Locationforecast 2.0.
 * Free for commercial use with CC BY 4.0 attribution; low-volume browser calls only.
 * Prefecture coordinates approximate prefectural capital; camera keys use venue coordinates.
 * Cache API responses locally for 15 minutes; load only badges that enter the viewport.
 * For high traffic, replace direct calls with a shared caching proxy per MET Norway ToS.
 */
(()=>{"use strict";
const coords={"hokkaido":[43.0618,141.3545],"aomori":[40.8244,140.74],"iwate":[39.702,141.1545],"miyagi":[38.2689,140.8721],"akita":[39.719,140.1035],"yamagata":[38.2404,140.3633],"fukushima":[37.7608,140.4747],"ibaraki":[36.3659,140.4712],"tochigi":[36.5551,139.8826],"gunma":[36.3906,139.0606],"saitama":[35.8617,139.6455],"chiba":[35.6074,140.1065],"tokyo":[35.6762,139.6503],"kanagawa":[35.4437,139.638],"niigata":[37.9161,139.0364],"toyama":[36.6953,137.2113],"ishikawa":[36.5613,136.6562],"fukui":[36.0652,136.2217],"yamanashi":[35.6639,138.5683],"nagano":[36.6485,138.195],"gifu":[35.4233,136.7607],"shizuoka":[34.9756,138.3828],"aichi":[35.1815,136.9066],"mie":[34.7303,136.5086],"shiga":[35.0045,135.8686],"kyoto":[35.0116,135.7681],"osaka":[34.6937,135.5023],"hyogo":[34.6901,135.1955],"nara":[34.6851,135.8048],"wakayama":[34.2305,135.1708],"tottori":[35.5011,134.2351],"shimane":[35.4681,133.0484],"okayama":[34.6552,133.9195],"hiroshima":[34.3853,132.4553],"yamaguchi":[34.1785,131.4737],"tokushima":[34.0703,134.5549],"kagawa":[34.3428,134.0466],"ehime":[33.8392,132.7657],"kochi":[33.5597,133.5311],"fukuoka":[33.5902,130.4017],"saga":[33.2635,130.3009],"nagasaki":[32.7503,129.8777],"kumamoto":[32.8031,130.7079],"oita":[33.2396,131.6093],"miyazaki":[31.9077,131.4202],"kagoshima":[31.5966,130.5571],"okinawa":[26.2124,127.6809],"shibuya":[35.6595,139.7005],"sensoji":[35.7148,139.7967],"kabukicho":[35.6938,139.7034],"dotonbori":[34.6686,135.501],"osaka-sky":[34.7025,135.4959],"arashiyama":[35.0094,135.667],"fuji":[35.4992,138.7687],"sapporo":[43.0591,141.3487],"hakata":[33.5902,130.4207],"bise":[26.703,127.882],"iki":[33.747,129.704]};
const lang=(document.documentElement.lang||"ko").toLowerCase().slice(0,2);
const t=({ko:{loading:"날씨 확인 중",missing:"날씨 정보 없음",forecast:"현재 예상 날씨",jst:"일본 현지"},en:{loading:"Loading weather",missing:"Weather unavailable",forecast:"Current forecast",jst:"Japan time"},ja:{loading:"天気を確認中",missing:"天気情報なし",forecast:"現在の予報",jst:"日本時間"},zh:{loading:"正在获取天气",missing:"天气暂不可用",forecast:"当前预报",jst:"日本时间"}})[lang]||({loading:"Loading weather",missing:"Weather unavailable",forecast:"Current forecast",jst:"Japan time"});
const nodes=[...document.querySelectorAll("[data-jp-weather]")];
if(!nodes.length)return;
const TTL=15*60*1000,MAX_STALE=90*60*1000,MAX_CONCURRENT=3;
const loaded=new Set(),queue=[],pending=new Map();let active=0;
const groups=new Map();
for(const el of nodes){const key=el.getAttribute("data-jp-weather");if(!coords[key])continue;let list=groups.get(key);if(!list)groups.set(key,list=[]);list.push(el);el.textContent="⌛ --°";el.title=t.loading;}
function icon(symbol){
const x=String(symbol||"").toLowerCase();
if(x.includes("thunder"))return"⛈️";
if(x.includes("sleet"))return"🌨️";
if(x.includes("snow"))return"❄️";
if(x.includes("rain"))return"🌧️";
if(x.includes("fog"))return"🌫️";
if(x.includes("partlycloudy"))return"⛅";
if(x.includes("cloudy"))return"☁️";
if(x.includes("fair"))return x.includes("night")?"🌙":"🌤️";
if(x.includes("clearsky"))return x.includes("night")?"🌙":"☀️";
return"🌡️";
}
function storageKey(key){return"jp.metweather.2026."+key;}
function readCache(key){try{const s=JSON.parse(localStorage.getItem(storageKey(key))||"null");if(s&&Number.isFinite(s.at)&&Number.isFinite(s.temp)&&typeof s.symbol==="string"&&Date.now()-s.at<MAX_STALE&&s.at<=Date.now()+60000)return s;}catch(_){}return null;}
function show(key,d,stale=false){
const txt=icon(d.symbol)+" "+Math.round(d.temp)+"°C";
(groups.get(key)||[]).forEach(el=>{
el.textContent=txt;
const at=d.forecastTime?new Intl.DateTimeFormat("en-GB",{timeZone:"Asia/Tokyo",hour:"2-digit",minute:"2-digit",hour12:false}).format(new Date(d.forecastTime)):"--:--";
el.title=t.forecast+" · "+at+" JST · MET Norway"+(stale?" (cached)":"");
el.dataset.jpWeatherReady="1";
});
}
function missing(key){(groups.get(key)||[]).forEach(el=>{el.textContent="—°";el.title=t.missing;});}
function request(key){
if(pending.has(key))return pending.get(key);
const promise=new Promise(resolve=>{queue.push({key,resolve});work();});pending.set(key,promise);return promise;
}
function work(){
while(active<MAX_CONCURRENT&&queue.length){
const {key,resolve}=queue.shift();active++;const c=coords[key];
const url="https://api.met.no/weatherapi/locationforecast/2.0/compact?lat="+Number(c[0]).toFixed(4)+"&lon="+Number(c[1]).toFixed(4);
fetch(url,{method:"GET",mode:"cors",credentials:"omit",cache:"default"}).then(r=>{if(!r.ok)throw Error("MET weather "+r.status);return r.json();}).then(data=>{
const entries=data&&data.properties&&data.properties.timeseries;
if(!Array.isArray(entries)||!entries.length)throw Error("No weather timeseries");
const now=Date.now();
const entry=entries.find(x=>Date.parse(x.time)>=now-60*60*1000)||entries[0];
const d=entry.data||{};
const temp=d.instant&&d.instant.details&&d.instant.details.air_temperature;
const symbol=(d.next_1_hours||d.next_6_hours||d.next_12_hours||{}).summary?.symbol_code||"";
if(!Number.isFinite(temp))throw Error("Missing forecast temperature");
const result={at:Date.now(),temp,symbol,forecastTime:entry.time};
try{localStorage.setItem(storageKey(key),JSON.stringify(result));}catch(_){}
show(key,result);
}).catch(()=>{const old=readCache(key);if(old)show(key,old,true);else missing(key);}).finally(()=>{active--;pending.delete(key);resolve();work();});
}
}
function load(key){
if(!groups.has(key))return;
const cached=readCache(key);
if(cached){show(key,cached,Date.now()-cached.at>TTL);if(Date.now()-cached.at<TTL)return;}
request(key);
}
function activate(el){
const key=el.getAttribute("data-jp-weather");if(!groups.has(key))return;
if(!loaded.has(key)){loaded.add(key);load(key);}
}
if("IntersectionObserver" in window){
const io=new IntersectionObserver(events=>{events.forEach(e=>{if(e.isIntersecting){activate(e.target);io.unobserve(e.target);}})},{rootMargin:"220px 0px"});
for(const el of nodes)io.observe(el);
}else nodes.slice(0,12).forEach(activate);
function clock(){for(const el of document.querySelectorAll("[data-jp-jst]")){el.textContent=t.jst+" · "+new Intl.DateTimeFormat("en-GB",{timeZone:"Asia/Tokyo",hour:"2-digit",minute:"2-digit",hour12:false}).format(new Date())+" JST";}}
clock();setInterval(clock,60000);
// Refresh only weather keys that have been viewed. Honor browser cache + local TTL.
setInterval(()=>{if(document.visibilityState!=="visible")return;loaded.forEach(load);},TTL);
})();
