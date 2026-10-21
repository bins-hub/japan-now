/* JAPULSE presence: real verified counts, or clearly labeled opt-in demo via ?presence_demo=1. */
(()=>{"use strict";
const locale=(document.documentElement.lang||"ko").toLowerCase();
const lang=locale.startsWith("en")?"en":locale.startsWith("ja")?"ja":locale.startsWith("zh")?"zh":"ko";
const translations={
 ko:{label:"LIVE · 지금 함께 보는 중",demo:"데모 · 가상 인원",unit:"명",desc:"테스트 화면입니다. 실제 접속자 수가 아닙니다."},
 en:{label:"LIVE · Watching together",demo:"DEMO · sample count",unit:"",desc:"Preview only. Not actual visitor data."},
 ja:{label:"LIVE · 一緒に視聴中",demo:"デモ · 仮の人数",unit:"人",desc:"テスト表示です。実際の接続人数ではありません。"},
 zh:{label:"LIVE · 正在一起观看",demo:"演示 · 模拟人数",unit:"人",desc:"仅供测试，不代表实际在线人数。"}
};
const t=translations[lang];
const params=new URLSearchParams(location.search);
const demo=params.get("presence_demo")==="1";
const raw=Number(params.get("presence_count"));
const defaultCount=Number.isSafeInteger(raw)&&raw>=1&&raw<=999?raw:28;
const endpoint=window.JAPULSE_PRESENCE_ENDPOINT;
if(!demo&&(typeof endpoint!=="string"||!/^https:\/\//.test(endpoint))){
 import("/assets/presence-firebase.js?v=20261021-f1").catch(()=>{});
 return;
}
let target=null;
if(!demo){try{const u=new URL(endpoint);if(u.protocol!=="https:")return;target=u.toString();}catch(_){return;}}
const slot=document.createElement("div");slot.className="jp-presence"+(demo?" jp-presence-demo":"");
slot.hidden=true;slot.setAttribute("role","status");slot.setAttribute("aria-live","off");
const dot=document.createElement("span");dot.className="jp-presence-dot";dot.setAttribute("aria-hidden","true");
const label=document.createElement("span");label.className="jp-presence-label";label.textContent=t.label;
const number=document.createElement("strong");number.className="jp-presence-number";
slot.append(dot,label,number);
function format(n){return new Intl.NumberFormat(locale).format(n)+t.unit;}
function show(n){number.textContent=format(n);slot.hidden=false;}
function mount(){const anchor=document.querySelector("main")||document.querySelector(".jp-wrap")||document.body;anchor.prepend(slot);}
if(demo){
 const badge=document.createElement("span");badge.className="jp-presence-demo-badge";badge.textContent=t.demo;slot.append(badge);slot.title=t.desc;
 let count=defaultCount, tick=0;
 function changeDemo(){if(document.visibilityState!=="visible")return;tick+=1;
  const delta=[0,2,1,-1,3,-2,0,1,-1,-2][(tick-1)%10];
  count=Math.max(1,Math.min(999,count+delta));show(count);
 }
 if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",()=>{mount();show(count);},{once:true});
 else{mount();show(count);}
 setInterval(changeDemo,16000);
 return;
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",mount,{once:true});else mount();
async function refresh(){if(document.visibilityState!=="visible")return;try{
 const ctrl=new AbortController();const timeout=setTimeout(()=>ctrl.abort(),4000);
 let response;try{response=await fetch(target,{mode:"cors",cache:"no-store",credentials:"omit",signal:ctrl.signal,headers:{Accept:"application/json"}});}finally{clearTimeout(timeout);}
 if(!response.ok)throw Error("Unavailable");
 const data=await response.json();
 if(!data||!Number.isSafeInteger(data.active)||data.active<0||data.active>10000000||data.verified!==true)throw Error("Invalid count");
 show(data.active);
}catch(_){slot.hidden=true;}}
refresh();setInterval(refresh,30000);document.addEventListener("visibilitychange",refresh);
})();