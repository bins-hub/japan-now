/* JAPULSE nationwide prefecture explorer: local client-side search, no paid API. */
(function(){
"use strict";
const root=document.querySelector("[data-jp-directory]");
if(!root)return;
const search=root.querySelector("[data-jp-query]");
const statusButtons=[...root.querySelectorAll("[data-jp-status]")];
const regionButtons=[...root.querySelectorAll("[data-jp-region]")];
const prefectures=[...root.querySelectorAll(".jp-pref[data-pref]")];
const sections=[...root.querySelectorAll(".jp-pref-section")];
const count=root.querySelector("[data-jp-count]");
const empty=root.querySelector("[data-jp-empty]");
let status="all", region="all";
function normalize(s){return(s||"").toLocaleLowerCase().normalize("NFKC").replace(/\s+/g,"");}
function render(){
const q=normalize(search.value);let matched=0;
prefectures.forEach(el=>{
const searchable=el.getAttribute("data-search")||"";
const okText=!q||normalize(searchable).includes(q);
const okRegion=region==="all"||el.dataset.region===region;
const okStatus=status==="all"||(status==="stream"&&el.dataset.stream==="yes")||(status==="official"&&el.dataset.official==="yes");
const show=okText&&okRegion&&okStatus;
el.hidden=!show;if(show)matched++;
});
sections.forEach(el=>{el.hidden=![...el.querySelectorAll(".jp-pref")].some(p=>!p.hidden);});
if(count)count.textContent=String(matched);
if(empty)empty.hidden=matched!==0;
}
function change(buttons,field,value){buttons.forEach(b=>b.setAttribute("aria-pressed",String(b.getAttribute(field)===value)));}
statusButtons.forEach(b=>b.addEventListener("click",()=>{status=b.dataset.jpStatus;change(statusButtons,"data-jp-status",status);render();}));
regionButtons.forEach(b=>b.addEventListener("click",()=>{region=b.dataset.jpRegion;change(regionButtons,"data-jp-region",region);render();}));
search.addEventListener("input",render);
if(location.hash.startsWith("#pref-")){
const el=root.querySelector(location.hash);if(el){region="all";render();setTimeout(()=>el.scrollIntoView({block:"center"}),80);}
}
render();
})();