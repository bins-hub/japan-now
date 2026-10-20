(function(){
"use strict";
var conf=window.JAPAN_NOW_ADSENSE||{};
if(conf.enabled!==true)return;
var lang=(document.documentElement.lang||"ko").toLowerCase();
lang=lang.startsWith("zh")?"zh-cn":lang.startsWith("ja")?"ja":lang.startsWith("en")?"en":"ko";
var trans={
ko:{label:"광고 · 데모",title:"Google AdSense 배너 영역",small:"광고가 게시되면 이 영역에 자동으로 표시됩니다.",note:"광고 위치 확인용 예시 · 실제 광고 아님",close:"데모 닫기",real:"광고"},
en:{label:"Advertisement · preview",title:"Google AdSense banner space",small:"An approved ad can appear in this position.",note:"Layout preview only · not a real advertisement",close:"Close preview",real:"Advertisement"},
"zh-cn":{label:"广告 · 演示",title:"Google AdSense 广告位置",small:"获批并配置后可在此区域显示广告。",note:"仅用于布局预览 · 非真实广告",close:"关闭演示",real:"广告"},
ja:{label:"広告 · デモ",title:"Google AdSense バナー枠",small:"承認・設定後はここに実際の広告を表示できます。",note:"レイアウト確認用 · 実際の広告ではありません",close:"デモを閉じる",real:"広告"}
};
var t=trans[lang];
var client=typeof conf.client==="string"?conf.client.trim():"";
var slot=typeof conf.slot==="string"?conf.slot.trim():"";
var live=conf.mode==="live"&&/^ca-pub-[0-9]{12,20}$/.test(client)&&/^[0-9]{5,20}$/.test(slot);
var targets=document.querySelectorAll("[data-jn-adsense-slot]");
if(!targets.length)return;
function tag(name,className,text){var e=document.createElement(name);if(className)e.className=className;if(text)e.textContent=text;return e;}
if(live){
  // Only in explicitly enabled live mode with supplied genuine publisher/slot IDs.
  var script=document.createElement("script");
  script.async=true;
  script.src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client="+encodeURIComponent(client);
  script.crossOrigin="anonymous";
  script.onload=function(){targets.forEach(function(target){
    var outer=tag("div","jn-adsense-live");
    outer.append(tag("span","jn-adsense-label",t.real));
    var ins=tag("ins","adsbygoogle");
    ins.style.display="block";
    ins.setAttribute("data-ad-client",client);
    ins.setAttribute("data-ad-slot",slot);
    ins.setAttribute("data-ad-format","auto");
    ins.setAttribute("data-full-width-responsive","true");
    outer.append(ins);target.append(outer);
    try{(window.adsbygoogle=window.adsbygoogle||[]).push({});}catch(err){console.warn("AdSense display unavailable");}
  });};
  document.head.append(script);
  return;
}
targets.forEach(function(target){
  var body=tag("div","jn-adsense-demo");
  var upper=tag("div","jn-adsense-upper");
  var label=tag("span","jn-adsense-label",t.label);
  var close=tag("button","jn-adsense-close",t.close);close.type="button";close.addEventListener("click",function(){target.replaceChildren();});
  upper.append(label,close);
  var preview=tag("div","jn-adsense-preview");
  var mark=tag("div","jn-adsense-mark","AD");
  var message=tag("div","jn-adsense-message");
  message.append(tag("strong","",t.title),tag("span","",t.small));
  preview.append(mark,message);
  body.append(upper,preview,tag("p","jn-adsense-note",t.note));
  target.append(body);
});
})();