/* JAPULSE presence widget. Never show fabricated counts. Activation requires a trusted backend endpoint. */
(()=>{"use strict";
const endpoint=window.JAPULSE_PRESENCE_ENDPOINT;
if(typeof endpoint!=="string"||!/^https:\/\//.test(endpoint))return;
let target;try{const u=new URL(endpoint);if(!["https:"].includes(u.protocol))return;target=u.toString();}catch(_){return}
const locale=(document.documentElement.lang||"ko").toLowerCase();
const lang=locale.startsWith("en")?"en":locale.startsWith("ja")?"ja":locale.startsWith("zh")?"zh":"ko";
const copy={ko:"지금 함께 보는 중",en:"Watching together now",ja:"いま一緒に視聴中",zh:"正在一起观看"};
const slot=document.createElement("div");slot.className="jp-presence";slot.hidden=true;slot.setAttribute("role","status");slot.setAttribute("aria-live","off");slot.innerHTML='<span class="jp-presence-dot" aria-hidden="true"></span><span class="jp-presence-label"></span><strong class="jp-presence-number"></strong>';
slot.querySelector(".jp-presence-label").textContent=copy[lang];
const countEl=slot.querySelector(".jp-presence-number");
const mount=()=>{const anchor=document.querySelector("main")||document.querySelector(".jp-wrap")||document.body;anchor.prepend(slot);};
let timer=null;
async function refresh(){if(document.visibilityState!=="visible")return;try{const ctrl=new AbortController();const timeout=setTimeout(()=>ctrl.abort(),4000);let response;try{response=await fetch(target,{mode:"cors",cache:"no-store",credentials:"omit",signal:ctrl.signal,headers:{"Accept":"application/json"}});}finally{clearTimeout(timeout)}
if(!response.ok)throw Error("Unavailable");
const data=await response.json();if(!data||!Number.isSafeInteger(data.active)||data.active<0||data.active>10000000||data.verified!==true)throw Error("Invalid count");
countEl.textContent=new Intl.NumberFormat(locale).format(data.active)+(lang==="ko"?"명":lang==="ja"?"人":lang==="zh"?"人":"");slot.hidden=false;
}catch(_){slot.hidden=true;}}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",mount,{once:true});else mount();
refresh();timer=setInterval(refresh,30000);document.addEventListener("visibilitychange",refresh);
})();
