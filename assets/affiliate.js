(function(){
"use strict";
var c=window.JAPAN_NOW_AFFILIATES||{};
var lang=(document.documentElement.lang||"ko").toLowerCase(),l=lang.indexOf("zh")===0?"zh-cn":lang.indexOf("ja")===0?"ja":lang.indexOf("en")===0?"en":"ko";
var available=Array.isArray(c[l])?c[l]:[];
var targets=document.querySelectorAll("[data-jn-affiliate-list]");
var labels={ko:"제휴 링크를 통한 예약이 발생하면 사이트 운영자에게 수수료가 지급될 수 있습니다.",en:"We may earn a commission from bookings made through affiliate links.","zh-cn":"通过联盟链接预订后，本站可能获得佣金。",ja:"アフィリエイトリンク経由の予約により報酬を受け取る場合があります。"};
targets.forEach(function(target){
 var city=target.getAttribute("data-jn-affiliate-list")||"all", count=0;
 available.forEach(function(entry){
   if(!entry||typeof entry!=="object"||entry.city!==city&&entry.city!=="all"||typeof entry.label!=="string"||typeof entry.url!=="string")return;
   try{var href=new URL(entry.url);if(href.protocol!=="https:")return;
    var a=document.createElement("a");a.href=href.href;a.rel="sponsored noopener noreferrer";a.target="_blank";a.textContent=entry.label;target.append(a);count++;
   }catch(e){}
 });
 if(count){
  var notice=document.createElement("div");notice.className="jn-affiliate-disclosure";notice.textContent=labels[l];target.after(notice);
  target.closest(".jn-booking")?.removeAttribute("hidden");
 }
});
})();