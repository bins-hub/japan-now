(function () {
"use strict";
// The banners are MOCKUPS only: official homepage links, never affiliate tracking.
if (window.JAPAN_NOW_SHOW_DEMO_BANNERS !== true) return;
var locale=(document.documentElement.lang||"ko").toLowerCase();
locale=locale.startsWith("zh")?"zh-cn":locale.startsWith("ja")?"ja":locale.startsWith("en")?"en":"ko";
var dictionaries={
ko:{eyebrow:"ADVERTISEMENT PREVIEW · TEST ONLY",title:"일본 여행 준비, 여기서 이어가세요",intro:"실시간 영상과 러닝·맛집을 본 다음 필요한 서비스만 선택하세요.",notice:"디자인 테스트용 배너입니다. 광고 계약·제휴 승인을 받았다는 뜻이 아니며, 링크는 추적 코드가 없는 공식 홈페이지로 이동합니다.",close:"테스트 배너 닫기",cta:"공식 사이트 보기",featured:"여행·관광",hotel:"숙소·호텔",connection:"인터넷",tickets:"일본 관광·체험 찾아보기",ticketsDesc:"관광패스·전망대·현지 액티비티를 살펴보세요.",stay:"일본 숙소 찾아보기",stayDesc:"방문할 지역에 맞춰 호텔과 료칸을 검색하세요.",esim:"일본 여행 eSIM",esimDesc:"출국 전 사용할 모바일 데이터 상품을 비교하세요."},
en:{eyebrow:"AD PREVIEW · DEMO ONLY",title:"Keep planning your Japan trip",intro:"After live cameras, running and local food, explore useful travel services.",notice:"These are visual demo banners, not paid ads or approved affiliate partnerships. Links open official homepages with no referral tracking.",close:"Close demo banners",cta:"Official website",featured:"Attractions",hotel:"Hotels",connection:"Connectivity",tickets:"Japan tours & tickets",ticketsDesc:"Explore sightseeing passes, observation decks and experiences.",stay:"Find a hotel in Japan",stayDesc:"Look for hotels and ryokan along your travel route.",esim:"Japan travel eSIM",esimDesc:"Compare mobile data options before you depart."},
"zh-cn":{eyebrow:"广告版式预览 · 仅供测试",title:"继续规划日本行程",intro:"看完实时画面、跑步路线与当地美食，再按需了解旅行服务。",notice:"这里是视觉测试用横幅，不代表已获得广告或联盟合作授权。点击后进入无推广追踪的官方网站。",close:"关闭测试横幅",cta:"查看官方网站",featured:"景点门票",hotel:"酒店住宿",connection:"移动网络",tickets:"日本景点与体验",ticketsDesc:"了解景点通票、观景台和当地体验项目。",stay:"寻找日本酒店",stayDesc:"根据旅程地点浏览酒店和日式旅馆。",esim:"日本旅行 eSIM",esimDesc:"出行前比较手机流量套餐。"},
ja:{eyebrow:"広告デザインの試用 · DEMO",title:"日本旅行の準備を続けよう",intro:"ライブカメラ・ランニング・地元グルメの後に便利な旅行サービスをチェック。",notice:"これは表示確認用のデモバナーです。広告契約やアフィリエイト承認を意味しません。リンクは紹介追跡のない各公式サイトに移動します。",close:"デモバナーを閉じる",cta:"公式サイトを見る",featured:"観光・体験",hotel:"ホテル",connection:"通信",tickets:"観光チケット・体験",ticketsDesc:"観光パス、展望台、現地アクティビティなどをチェック。",stay:"日本の宿泊施設",stayDesc:"旅程に合わせてホテルや旅館を探しましょう。",esim:"日本旅行のeSIM",esimDesc:"出発前にモバイルデータプランを比較しましょう。"}
};
var t=dictionaries[locale];
var cards=[
{brand:"Klook",url:"https://www.klook.com/",icon:"🎟️",tag:t.featured,title:t.tickets,desc:t.ticketsDesc},
{brand:"Agoda",url:"https://www.agoda.com/",icon:"🏨",tag:t.hotel,title:t.stay,desc:t.stayDesc},
{brand:"Airalo",url:"https://www.airalo.com/",icon:"📶",tag:t.connection,title:t.esim,desc:t.esimDesc}
];
function element(tag,klass,text){var node=document.createElement(tag);if(klass)node.className=klass;if(text)node.textContent=text;return node;}
document.querySelectorAll("[data-jn-demo-banners]").forEach(function(slot){
 var panel=element("div","jn-demo-panel");
 var head=element("div","jn-demo-header");
 var heading=element("div","jn-demo-heading");
 heading.append(element("span","jn-demo-eyebrow",t.eyebrow),element("h2","",t.title),element("p","",t.intro));
 var dismiss=element("button","jn-demo-close",t.close);dismiss.type="button";dismiss.addEventListener("click",function(){slot.replaceChildren();});
 head.append(heading,dismiss);panel.append(head);
 var grid=element("div","jn-demo-grid");
 cards.forEach(function(item,i){
 var card=element("article","jn-demo-card jn-demo-"+i);
 var above=element("div","jn-demo-card-head");
 var ico=element("div","jn-demo-icon",item.icon);ico.setAttribute("aria-hidden","true");
 var brand=element("div","jn-demo-brand");brand.append(element("strong","",item.brand),element("span","",item.tag));
 above.append(ico,brand);
 var body=element("div","jn-demo-card-body");
 body.append(element("h3","",item.title),element("p","",item.desc));
 var link=element("a","jn-demo-cta",t.cta+" ↗");
 link.href=item.url;link.target="_blank";link.rel="noopener noreferrer";link.setAttribute("aria-label",item.brand+" – "+t.cta);
 body.append(link);card.append(above,body);grid.append(card);
 });
 var note=element("p","jn-demo-notice",t.notice);
 panel.append(grid,note);slot.append(panel);
});
})();