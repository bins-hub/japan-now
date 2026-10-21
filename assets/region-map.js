/* JAPULSE clickable map: all 47 shapes rendered inline for offline/fetch-safe display. */
(()=>{"use strict";
const slot=document.querySelector("[data-jp-map]");
if(!slot)return;
const root=slot.closest("[data-jp-directory]");
const svg=slot.querySelector("svg.jp-interactive-map");
if(!root||!svg)return;
const regions=[...svg.querySelectorAll("[data-jp-map-region]")];
if(regions.length!==8)return;
function setActive(current){
 regions.forEach(g=>g.setAttribute("aria-pressed",String(g.getAttribute("data-jp-map-region")===current)));
}
regions.forEach(g=>{
 const select=()=>{
   const region=g.getAttribute("data-jp-map-region");
   root.dispatchEvent(new CustomEvent("jp-map-select",{detail:{region}}));
 };
 g.addEventListener("click",select);
 g.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();select();}});
});
root.addEventListener("jp-region-changed",e=>setActive(e.detail?.region||"all"));
const current=root.querySelector('[data-jp-region][aria-pressed="true"]')?.getAttribute("data-jp-region")||"all";
setActive(current);
const credit=root.querySelector("[data-jp-map-caption]");
if(credit)credit.dataset.jpMapReady="true";
})();