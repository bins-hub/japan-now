/* JAPULSE Haneda on-site official YouTube players. Sources may rotate/stop; never claim verified live. */
(()=>{"use strict";
const box=document.getElementById("hanedaPlayer"),start=document.getElementById("hanedaPlay"),buttons=[...document.querySelectorAll("[data-jp-haneda-source]")];
if(!box||!start||!buttons.length)return;
const providers={
ntv:{id:"2PIdi3Xa7TY",name:"日テレNEWS",terminal:"T2"},
tbs:{id:"dYpspgeXSaQ",name:"TBS NEWS DIG",terminal:"T2"},
tbs1:{id:"2f9NOSw-FqM",name:"TBS NEWS DIG",terminal:"T1"}
};
let current="ntv";
const sourceLink=document.querySelector("[data-jp-haneda-original]");
const providerText=document.querySelector("[data-jp-haneda-provider]");
const availability=document.querySelector("[data-jp-haneda-availability]");
function setSource(key,autoplay){
 if(!providers[key])return;current=key;
 const source=providers[key];
 buttons.forEach(b=>{const selected=b.dataset.jpHanedaSource===key;b.setAttribute("aria-pressed",String(selected));b.classList.toggle("is-selected",selected);});
 if(sourceLink)sourceLink.href="https://www.youtube.com/watch?v="+encodeURIComponent(source.id);
 if(providerText)providerText.textContent=source.name+" · "+source.terminal;
 if(availability)availability.hidden=!autoplay;
 if(autoplay)play();
}
function play(){
 const source=providers[current];
 const iframe=document.createElement("iframe");
 iframe.src="https://www.youtube-nocookie.com/embed/"+encodeURIComponent(source.id)+"?autoplay=1&playsinline=1&rel=0";
 iframe.title="Haneda Airport "+source.terminal+" / "+source.name+" — official YouTube video";
 iframe.allow="autoplay;encrypted-media;picture-in-picture;web-share";
 iframe.referrerPolicy="strict-origin-when-cross-origin";
 iframe.allowFullscreen=true;
 box.replaceChildren(iframe);
 if(availability)availability.hidden=false;
}
start.addEventListener("click",play);
buttons.forEach(b=>b.addEventListener("click",()=>setSource(b.dataset.jpHanedaSource,true)));
setSource(current,false);
})();