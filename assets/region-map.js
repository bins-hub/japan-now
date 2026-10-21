/* JAPULSE map: SVG source lalamalink CC0; keyboard and touch accessible. */
(()=>{"use strict";
const slot=document.querySelector("[data-jp-map]");
if(!slot)return;
const root=slot.closest("[data-jp-directory]");
const source="https://japulse.com/assets/japan-regions-map.svg?v=20261021-m1";
const msg=root?.querySelector("[data-jp-map-caption]");
fetch(source,{credentials:"same-origin"}).then(r=>{if(!r.ok)throw Error("Map "+r.status);return r.text();}).then(xml=>{
 const doc=new DOMParser().parseFromString(xml,"image/svg+xml");
 const svg=doc.documentElement;
 if(svg.localName!=="svg"||doc.querySelector("parsererror"))throw Error("Invalid SVG");
 const regions=[...svg.querySelectorAll("[data-jp-map-region]")];
 if(regions.length!==8)throw Error("Invalid Japan regions");
 const own=document.importNode(svg,true);
 slot.replaceChildren(own);
 function activate(g){
  const region=g.getAttribute("data-jp-map-region");
  if(!root||!region)return;
  root.dispatchEvent(new CustomEvent("jp-map-select",{detail:{region}}));
 }
 own.querySelectorAll("[data-jp-map-region]").forEach(g=>{
   g.addEventListener("click",()=>activate(g));
   g.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();activate(g);}});
 });
 root?.addEventListener("jp-region-changed",e=>{
  const current=e.detail?.region||"all";
  own.querySelectorAll("[data-jp-map-region]").forEach(g=>g.setAttribute("aria-pressed",String(g.getAttribute("data-jp-map-region")===current)));
 });
 const initial=root?.querySelector('[data-jp-region][aria-pressed="true"]')?.getAttribute("data-jp-region")||"all";
 own.querySelectorAll("[data-jp-map-region]").forEach(g=>g.setAttribute("aria-pressed",String(g.getAttribute("data-jp-map-region")===initial)));
 if(msg)msg.dataset.jpMapReady="true";
}).catch(()=>{
 const fallback=root?.querySelector("[data-jp-map-fallback]");
 if(fallback)fallback.hidden=false;
 slot.hidden=true;
 if(msg)msg.dataset.jpMapReady="false";
});
})();