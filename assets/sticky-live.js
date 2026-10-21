/* JAPULSE mobile sticky player: keep the SAME YouTube iframe alive while scrolling. */
(function(){
  "use strict";
  const root=document.querySelector(".jp-home-video[data-jp-home-live]");
  if(!root || !window.matchMedia || !window.requestAnimationFrame)return;
  const stage=root.querySelector(".jp-home-live-stage");
  if(!stage)return;
  const header=document.querySelector(".jp-bar");
  const mobile=window.matchMedia("(max-width: 640px)");
  const lang=(document.documentElement.lang||"ko").toLowerCase();
  const closeLabel=lang.startsWith("ja")?"小窓を閉じる":lang.startsWith("zh")?"关闭悬浮视频":lang.startsWith("en")?"Close floating video":"떠 있는 영상 닫기";
  const placeholder=document.createElement("div");
  placeholder.className="jp-live-sticky-placeholder";
  placeholder.setAttribute("aria-hidden","true");
  stage.before(placeholder);
  const close=document.createElement("button");
  close.type="button";
  close.className="jp-live-sticky-close";
  close.setAttribute("aria-label",closeLabel);
  close.textContent="×";
  stage.appendChild(close);
  let floating=false, dismissed=false, scheduled=false;
  function setFloating(next){
    if(floating===next)return;
    if(next){
      // Replace only the stage's layout space; never detach or rebuild the iframe.
      placeholder.style.height=Math.round(stage.getBoundingClientRect().height)+"px";
      stage.classList.add("jp-live-floating");
      root.classList.add("jp-live-sticky-active");
    }else{
      stage.classList.remove("jp-live-floating");
      root.classList.remove("jp-live-sticky-active");
      placeholder.style.height="0px";
    }
    floating=next;
  }
  function update(){
    scheduled=false;
    if(!mobile.matches){
      dismissed=false;
      setFloating(false);
      return;
    }
    const headerBottom=header?Math.max(0,header.getBoundingClientRect().bottom):0;
    const top=Math.round(headerBottom+8);
    stage.style.setProperty("--jp-live-floating-top",top+"px");
    // Placeholder always remains in the normal document flow as the scroll anchor.
    const originalTop=placeholder.getBoundingClientRect().top;
    const passed=window.scrollY>40 && originalTop<=headerBottom+8;
    if(!passed){
      dismissed=false;
      setFloating(false);
    }else if(!dismissed){
      setFloating(true);
      if(floating){
        // The original stage normally has a 16:9 aspect ratio and 200px minimum.
        placeholder.style.height=Math.round(Math.max(200,root.clientWidth*9/16))+"px";
      }
    }
  }
  function schedule(){
    if(scheduled)return;
    scheduled=true;
    window.requestAnimationFrame(update);
  }
  close.addEventListener("click",function(){
    dismissed=true;
    setFloating(false);
  });
  window.addEventListener("scroll",schedule,{passive:true});
  window.addEventListener("resize",schedule);
  if(mobile.addEventListener)mobile.addEventListener("change",schedule);
  else if(mobile.addListener)mobile.addListener(schedule);
  schedule();
})();
