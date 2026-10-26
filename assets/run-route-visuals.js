/* JAPULSE animated RUN route diagrams. Illustrative sequences, never GPS tracks. */
(() => {
  "use strict";
  const NS = "http://www.w3.org/2000/svg";
  const shapes = {
    tokyo: {kind:"loop", d:"M 175 273 C 134 235 149 159 219 118 C 299 72 432 82 563 129 C 669 169 653 262 564 290 C 452 332 263 333 175 273", distance:"~5 km", label:"Imperial Palace"},
    osaka: {kind:"loop", d:"M 196 280 C 151 267 110 204 151 141 C 205 82 346 105 428 112 C 552 89 650 139 654 203 C 667 296 518 331 363 302 C 260 282 213 295 196 280", distance:"~3.5 km", label:"Osaka Castle Park"},
    kyoto: {kind:"return", d:"M 169 292 C 199 242 261 227 319 197 C 394 159 446 120 543 92 C 592 80 628 92 650 112 C 617 132 598 137 545 143 C 443 168 397 211 329 243 C 245 286 209 305 169 292", distance:"4.3km one-way", label:"Kamogawa River"},
    kyushu: {kind:"loop", d:"M 269 282 C 192 261 176 191 225 140 C 280 87 380 74 481 100 C 575 127 633 183 612 249 C 592 307 487 334 382 326 C 334 324 292 301 269 282", distance:"~2 km", label:"Ohori Park"},
    hokkaido: {kind:"loop", d:"M 223 284 C 143 260 145 179 207 132 C 270 91 309 111 371 107 C 448 91 534 86 591 150 C 657 229 577 308 474 312 C 344 339 275 315 223 284", distance:"short loop", label:"Nakajima Park"},
    okinawa: {kind:"return", d:"M 175 268 C 248 232 321 208 393 180 C 487 145 558 125 653 102 C 681 113 681 133 659 144 C 568 174 497 196 401 224 C 316 248 243 290 175 268", distance:"length varies", label:"Araha Beach"}
  };
  const locales = {
    ko:{title:"출발점에서 출발해 다시 돌아오는 동선",route:"코스 동선 애니메이션",start:"출발 · 도착",turn:"반환점",preview:"경로 도식",explain:"동선 이해용 도식입니다. 실제 축척·GPS 지도는 아니며 현장 표지와 지도 링크로 경로를 확인하세요.",loop:"순환형 · 출발지 복귀",back:"왕복형 · 같은 길 복귀",play:"▶ 재생",pause:"❚❚ 일시정지",replay:"↻ 처음부터",complete:"출발점 복귀!",ready:"출발 준비",running:"이동 중",maps:"아래 지도·길찾기에서 실제 경로 확인"},
    en:{title:"Follow the route and return to the starting point",route:"Animated route overview",start:"Start / finish",turn:"Turnaround",preview:"Route diagram",explain:"Illustrative sequence only, not a GPS track or scaled map. Confirm actual paths with the linked map and local signs.",loop:"Loop · return to start",back:"Out & back · return to start",play:"▶ Play",pause:"❚❚ Pause",replay:"↻ Replay",complete:"Back at the start!",ready:"Ready to start",running:"Moving along route",maps:"Use Maps & directions below to check the real path"},
    ja:{title:"出発地点から走り、同じ場所へ戻る動線",route:"動くコース案内",start:"スタート・ゴール",turn:"折り返し",preview:"コース概念図",explain:"動線を理解するための概念図です。GPS軌跡や実際の縮尺ではありません。現地案内と地図を確認してください。",loop:"周回型・出発点に戻る",back:"往復型・出発点に戻る",play:"▶ 再生",pause:"❚❚ 一時停止",replay:"↻ 最初から",complete:"出発地点に到着！",ready:"出発準備",running:"ルートを移動中",maps:"実際の道順は下の地図で確認"},
    "zh-cn":{title:"从起点出发，沿路线返回同一位置",route:"动态路线示意",start:"起点／终点",turn:"折返点",preview:"路线示意图",explain:"仅供理解行进方向，并非GPS轨迹或按比例绘制的地图。请参考实际地图与现场标志。",loop:"环线 · 返回起点",back:"往返 · 返回起点",play:"▶ 播放",pause:"❚❚ 暂停",replay:"↻ 重新播放",complete:"已回到起点！",ready:"准备出发",running:"沿路线前进中",maps:"实际路线请查看下方地图链接"}
  };
  const routeIds = Object.keys(shapes);
  const lang = location.pathname.startsWith("/ja/")?"ja":location.pathname.startsWith("/zh-cn/")?"zh-cn":location.pathname.startsWith("/en/")?"en":"ko";
  const t = locales[lang];
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const svgEl = (name,attrs={}) => {
    const el=document.createElementNS(NS,name);
    for(const [k,v] of Object.entries(attrs))el.setAttribute(k,v);
    return el;
  };
  const setSvgText=(parent,name,attrs,text)=>{const node=svgEl(name,attrs);node.textContent=text;parent.append(node);return node;};
  const controllers=[];
  for(const id of routeIds){
    const article=document.getElementById(id);
    if(!article)continue;
    const cfg=shapes[id];
    const panel=document.createElement("section");
    panel.className="jp-route-animated";
    panel.setAttribute("aria-label",t.route);
    const kicker=document.createElement("p");kicker.className="jp-route-kicker";kicker.textContent="JAPULSE · RUN ROUTE";
    const heading=document.createElement("h3");heading.textContent=t.title;
    const note=document.createElement("p");note.className="jp-route-disclaimer";note.textContent=t.explain;
    const graphic=document.createElement("div");graphic.className="jp-route-graphic";
    const svg=svgEl("svg",{viewBox:"0 0 820 395",role:"img","aria-label":t.route+" — "+cfg.label,"preserveAspectRatio":"xMidYMid meet"});
    setSvgText(svg,"title",{},cfg.label+": "+t.route);
    setSvgText(svg,"desc",{},t.explain);
    svg.append(svgEl("rect",{x:"0",y:"0",width:"820",height:"395",rx:"16",fill:"#edf6f3"}));
    svg.append(svgEl("path",{d:"M 44 64 H 775 M 44 337 H 775",stroke:"#cddfda","stroke-width":"2"}));
    setSvgText(svg,"text",{x:"42",y:"42",fill:"#126a58","font-size":"16","font-weight":"800","letter-spacing":"1"},"JAPULSE RUN");
    setSvgText(svg,"text",{x:"777",y:"42","text-anchor":"end",fill:"#4d6f67","font-size":"15","font-weight":"650"},cfg.distance);
    if(cfg.kind==="loop"){
      svg.append(svgEl("ellipse",{cx:"411",cy:"210",rx:"165",ry:"79",fill:"#cfe9df",opacity:".55"}));
    }else{
      svg.append(svgEl("path",{d:"M 90 212 Q 390 120 739 76",stroke:"#bedfd8","stroke-width":"3","stroke-dasharray":"8 12",fill:"none",opacity:".7"}));
    }
    const track=svgEl("path",{d:cfg.d,fill:"none",stroke:"#bad3cc","stroke-width":"19","stroke-linecap":"round","stroke-linejoin":"round"});
    const progress=svgEl("path",{d:cfg.d,fill:"none",stroke:"#087a69","stroke-width":"16","stroke-linecap":"round","stroke-linejoin":"round"});
    svg.append(track,progress);
    const total=progress.getTotalLength();
    progress.setAttribute("stroke-dasharray",String(total));
    progress.setAttribute("stroke-dashoffset",String(total));
    const start=progress.getPointAtLength(0);
    svg.append(svgEl("circle",{cx:start.x,cy:start.y,r:"22",fill:"#fff",stroke:"#127762","stroke-width":"3"}));
    const marker=svgEl("circle",{cx:start.x,cy:start.y,r:"23",fill:"#f3654d",stroke:"#fff","stroke-width":"4"});
    const halo=svgEl("circle",{cx:start.x,cy:start.y,r:"35",fill:"#f3654d",opacity:".18"});
    svg.append(halo,marker);
    setSvgText(svg,"text",{x:"40",y:"365",fill:"#244e49","font-size":"16","font-weight":"700"},"●  "+t.start);
    setSvgText(svg,"text",{x:"780",y:"365","text-anchor":"end",fill:"#4e756b","font-size":"15"},cfg.kind==="loop"?t.loop:t.back);
    graphic.append(svg);
    const ctrls=document.createElement("div");ctrls.className="jp-route-controls";
    const play=document.createElement("button");play.type="button";play.textContent=t.play;play.setAttribute("aria-label",t.play);
    const replay=document.createElement("button");replay.type="button";replay.textContent=t.replay;replay.setAttribute("aria-label",t.replay);
    const status=document.createElement("span");status.className="jp-route-status";status.setAttribute("role","status");status.setAttribute("aria-live","off");status.textContent=t.ready;
    const indicator=document.createElement("progress");indicator.className="jp-route-progress";indicator.max=100;indicator.value=0;indicator.setAttribute("aria-label","Route completion");
    ctrls.append(play,replay,status,indicator);
    const helper=document.createElement("p");helper.className="jp-route-bottom-note";helper.textContent=t.maps;
    panel.append(kicker,heading,ctrls,graphic,note,helper);
    const shower=article.querySelector(".jn-shower-jump");
    if(shower)shower.insertAdjacentElement("afterend",panel);else article.querySelector("h2")?.insertAdjacentElement("afterend",panel);
    let frame=0,playing=false,done=0,started=0,visible=false,autoLoop=!reduced,replayTimer=0;
    const duration=10800;
    const setProgress=(fraction)=>{
      const f=Math.min(1,Math.max(0,fraction));
      const pt=progress.getPointAtLength(total*f);
      marker.setAttribute("cx",pt.x);marker.setAttribute("cy",pt.y);
      halo.setAttribute("cx",pt.x);halo.setAttribute("cy",pt.y);
      progress.setAttribute("stroke-dashoffset",String(total*(1-f)));
      indicator.value=Math.round(f*100);
      if(playing)status.textContent=t.running+" · "+Math.round(f*100)+"%";
    };
    const stop=()=>{playing=false;cancelAnimationFrame(frame);clearTimeout(replayTimer);replayTimer=0;frame=0;play.textContent=t.play;play.setAttribute("aria-label",t.play);};
    const tick=time=>{
      if(!playing)return;
      if(!started)started=time;
      done=Math.min(1,(time-started)/duration);
      setProgress(done);
      if(done===1){stop();status.textContent=t.complete;if(visible&&autoLoop&&!reduced)replayTimer=setTimeout(()=>startAnimation(true),1600);return;}
      frame=requestAnimationFrame(tick);
    };
    const startAnimation=(restart=false)=>{
      if(restart){done=0;setProgress(0);}
      if(playing)return;
      if(done>=1){done=0;setProgress(0);}
      playing=true;started=0;status.textContent=t.running;
      play.textContent=t.pause;play.setAttribute("aria-label",t.pause);
      const initialDone=done;
      const begin=time=>{
        started=time-initialDone*duration;
        frame=requestAnimationFrame(tick);
      };
      frame=requestAnimationFrame(begin);
    };
    play.addEventListener("click",()=>{if(playing){autoLoop=false;stop();status.textContent=t.ready;}else{autoLoop=true;startAnimation();}});
    replay.addEventListener("click",()=>{autoLoop=true;stop();startAnimation(true);});
    controllers.push({panel,start:startAnimation,stop,visible:()=>visible,setVisible:v=>visible=v,allowAuto:()=>autoLoop,resetAuto:()=>{autoLoop=true;},isPlaying:()=>playing});
    if(reduced){setProgress(1);done=1;status.textContent=t.complete;}
  }
  if(!reduced&&"IntersectionObserver" in window){
    const watch=new IntersectionObserver(entries=>{
      for(const entry of entries){const c=controllers.find(x=>x.panel===entry.target);if(!c)continue;c.setVisible(entry.isIntersecting);if(entry.isIntersecting&&!c.isPlaying()&&c.allowAuto())c.start(true);else if(!entry.isIntersecting)c.stop();}
    },{threshold:.22});
    controllers.forEach(x=>watch.observe(x.panel));
  }else if(!reduced){
    controllers.forEach(x=>x.start());
  }
  document.addEventListener("visibilitychange",()=>{if(document.hidden)controllers.forEach(x=>x.stop());});
})();
