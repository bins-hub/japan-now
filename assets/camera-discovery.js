
(function(){
"use strict";
const entries=[{"ko":"도쿄역 마루노우치","en":"Tokyo Station Marunouchi","region":"kanto","weather":"tokyo-marunouchi","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/kanto/tokyo/tokyo-station-marunouchi.html"},{"ko":"오사카 신사이바시","en":"Osaka Shinsaibashi","region":"kansai","weather":"shinsaibashi","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/kansai/osaka/shinsaibashi.html"},{"ko":"교토 히가시혼간지","en":"Kyoto Higashi Honganji Temple","region":"kansai","weather":"kyoto-honganji","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/kansai/kyoto/higashi-hongan-ji-temple.html"},{"ko":"고베항 전망","en":"Kobe Port Panorama","region":"kansai","weather":"kobe-port","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/hyogo/kobe/kobe.html"},{"ko":"가미코치 갓파바시","en":"Kamikochi Kappa Bridge","region":"chubu","weather":"kamikochi","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/nagano-prefecture/kamikochi/kamikochi-kappa-bridge.html"},{"ko":"미야지마 이쓰쿠시마 신사","en":"Miyajima Itsukushima Shrine","region":"chugoku","weather":"miyajima","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/prefecture-of-hiroshima/hiroshima/miyajima-itsukushima-shrine.html"},{"ko":"삿포로 모이와산","en":"Sapporo Mount Moiwa","region":"hokkaido","weather":"sapporo-moiwa","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/prefecture-of-hokkaido/sapporo/mount-moiwa.html"},{"ko":"하코다테 항구","en":"Hakodate Harbour","region":"hokkaido","weather":"hakodate","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/prefecture-of-hokkaido/hakodate/panorama.html"},{"ko":"리시리섬 페리터미널","en":"Rishiri Ferry Terminal","region":"hokkaido","weather":"rishiri","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/prefecture-of-hokkaido/rishirifuji/ferry-terminal.html"},{"ko":"도쿄 하네다공항","en":"Tokyo Haneda Airport","region":"kanto","weather":"haneda","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/kanto/tokyo/haneda-tokyo-international-airport.html"},{"ko":"도쿄타워 전망","en":"Tokyo Tower View","region":"kanto","weather":"tokyo-tower","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/kanto/tokyo/tokyo-tower.html"},{"ko":"도쿄 스카이라인","en":"Tokyo Skyline","region":"kanto","weather":"tokyo-skyline","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/kanto/tokyo/tokyo-skyline.html"},{"ko":"도쿄 신칸센 철도","en":"Tokyo Shinkansen Trains","region":"kanto","weather":"tokyo-shinkansen","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/kanto/tokyo/shinkansen.html"},{"ko":"도쿄 하마리큐 정원","en":"Tokyo Hamarikyu Garden","region":"kanto","weather":"tokyo-hamarikyu","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/kanto/tokyo/hamarikyu-garden.html"},{"ko":"도쿄 신바시역","en":"Tokyo Shimbashi Station","region":"kanto","weather":"tokyo-shimbashi","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/kanto/tokyo/shimbashi.html"},{"ko":"도쿄 신주쿠역","en":"Tokyo Shinjuku Station","region":"kanto","weather":"tokyo-shinjuku","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/kanto/tokyo/shinjuku-station.html"},{"ko":"가마쿠라 고마치 거리","en":"Kamakura Komachi Street","region":"kanto","weather":"kamakura","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/kanto/kamakura/kamakura.html"},{"ko":"닛코 신쿄 다리","en":"Nikko Shinkyo Bridge","region":"kanto","weather":"nikko","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/kanto/nikko/shinkyo-bridge.html"},{"ko":"가마쿠라 해변 전망","en":"Kamakura Bay","region":"kanto","weather":"kamakura","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/kanagawa-prefecture/kamakura/kamakura.html"},{"ko":"마쓰모토성 정면","en":"Matsumoto Castle","region":"chubu","weather":"matsumoto","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/nagano-prefecture/matsumoto/castle.html"},{"ko":"마쓰모토성 서쪽","en":"Matsumoto Castle West View","region":"chubu","weather":"matsumoto","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/nagano-prefecture/matsumoto/matsumoto.html"},{"ko":"가나자와 겐로쿠엔","en":"Kanazawa Kenrokuen Garden","region":"chubu","weather":"kanazawa","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/ishikawa-prefecture/kanazawa/park.html"},{"ko":"가나자와 시내","en":"Kanazawa City","region":"chubu","weather":"kanazawa","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/ishikawa-prefecture/kanazawa/kanazawa.html"},{"ko":"다테야마 무로도 설경","en":"Tateyama Murodo","region":"chubu","weather":"murodo","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/prefecture-of-toyama/tateyama/murodo-slopes.html"},{"ko":"야마나카호 후지산","en":"Lake Yamanakako and Mount Fuji","region":"chubu","weather":"yamanakako","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/yamanashi-prefecture/yamanakako/lake-yamanakako-mount-fuji.html"},{"ko":"오사카역","en":"Osaka Station","region":"kansai","weather":"osaka","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/kansai/osaka/train-station.html"},{"ko":"신오사카역","en":"Shin-Osaka Station","region":"kansai","weather":"shin-osaka","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/kansai/osaka/shin-osaka-station.html"},{"ko":"히로시마역 입구","en":"Hiroshima Station","region":"chugoku","weather":"hiroshima","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/prefecture-of-hiroshima/hiroshima/train-station.html"},{"ko":"다다노미 항구","en":"Tadanomi Port","region":"chugoku","weather":"tadanomi","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/prefecture-of-hiroshima/hiroshima/tadanomi-port.html"},{"ko":"돗토리 사구","en":"Tottori Sand Dunes","region":"chugoku","weather":"tottori-sand","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/prefecture-of-tottori/tottori/sand-dunes.html"},{"ko":"이와쿠니 긴타이교","en":"Iwakuni Kintai Bridge","region":"chugoku","weather":"iwakuni","source":"Iwakuni City","url":"https://kintaikyo.iwakuni-city.net/liveview.html"},{"ko":"이마바리 구루시마 해협대교","en":"Imabari Kurushima Kaikyo Bridge","region":"shikoku","weather":"imabari","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/ehime-prefecture/imabari/kurushima-kaikyo.html"},{"ko":"나가사키 항구","en":"Nagasaki Port","region":"kyushu","weather":"nagasaki-port","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/nagasaki-prefecture/nagasaki/port-of-nagasaki.html"},{"ko":"구마모토 가라시마 공원","en":"Kumamoto Karashima Park","region":"kyushu","weather":"kumamoto","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/kyushu/kumamoto/park-karashima.html"},{"ko":"구마모토 시내","en":"Kumamoto City","region":"kyushu","weather":"kumamoto","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/kyushu/kumamoto/kumamoto.html"},{"ko":"가고시마 사쿠라지마 화산","en":"Kagoshima Sakurajima Volcano","region":"kyushu","weather":"sakurajima","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/prefecture-of-kagoshima/tarumizu/sakurajima.html"},{"ko":"오키나와 미야코지마 해변","en":"Okinawa Miyakojima Beach","region":"okinawa","weather":"miyakojima","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/okinawa-prefecture/miyakojima/miyakojima.html"},{"ko":"오키나와 나하시 전망","en":"Okinawa Naha View","region":"okinawa","weather":"naha","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/okinawa-prefecture/naha/city.html"},{"ko":"오키나와 온나 가리유시 비치","en":"Okinawa Onna Kariyushi Beach","region":"okinawa","weather":"onna","source":"SkylineWebcams","url":"https://www.skylinewebcams.com/en/webcam/japan/okinawa-prefecture/onna/onna.html"},{"ko":"도쿄 시부야 스크램블","en":"Tokyo Shibuya Crossing","region":"kanto","weather":"shibuya","source":"JAPULSE","path":"cameras/shibuya/"},{"ko":"도쿄 아사쿠사 센소지","en":"Asakusa Sensoji","region":"kanto","weather":"sensoji","source":"JAPULSE","path":"cameras/sensoji/"},{"ko":"도쿄 신주쿠 가부키초","en":"Shinjuku Kabukicho","region":"kanto","weather":"kabukicho","source":"JAPULSE","path":"cameras/kabukicho/"},{"ko":"오사카 도톤보리","en":"Osaka Dotonbori","region":"kansai","weather":"dotonbori","source":"JAPULSE","path":"cameras/dotonbori/"},{"ko":"오사카 도심 전망","en":"Osaka Skyline","region":"kansai","weather":"osaka-sky","source":"JAPULSE","path":"cameras/osaka-sky/"},{"ko":"교토 아라시야마","en":"Kyoto Arashiyama","region":"kansai","weather":"arashiyama","source":"JAPULSE","path":"cameras/arashiyama/"},{"ko":"삿포로 오도리 공원","en":"Sapporo Odori Park","region":"hokkaido","weather":"sapporo","source":"JAPULSE","path":"cameras/sapporo/"},{"ko":"후지산 가와구치호","en":"Mount Fuji Kawaguchiko","region":"chubu","weather":"fuji","source":"JAPULSE","path":"cameras/fuji/"},{"ko":"후쿠오카 하카타역","en":"Fukuoka Hakata Station","region":"kyushu","weather":"hakata","source":"JAPULSE","path":"cameras/hakata/"},{"ko":"나가사키 이키섬","en":"Nagasaki Iki Island","region":"kyushu","weather":"iki","source":"JAPULSE","path":"cameras/iki/"},{"ko":"오키나와 비세","en":"Okinawa Bise","region":"okinawa","weather":"bise","source":"JAPULSE","path":"cameras/okinawa/"}];
const root=document.querySelector("[data-jp-extra-cameras]");
if(!root)return;
const directory=root.closest("[data-jp-directory]");
const lang=(document.documentElement.lang||"ko").toLowerCase().slice(0,2);
const dict={
ko:{title:"일본 전국 카메라 50곳 모아보기",subtitle:"기존 안내 11곳 · 외부 원본 39곳 · 페이지 주소 확인, 현재 방송 상태는 미확인",search:"지역·카메라 이름 검색",all:"전체",more:"카메라 더 보기",empty:"조건에 맞는 카메라가 없습니다.",internal:"JAPULSE 안내",external:"외부 원본",watch:"원본에서 보기 ↗",local:"카메라 보기 →",notice:"외부 영상은 재송출하지 않습니다. 연결된 제공 사이트에서 재생 가능 여부·촬영 시각을 확인하세요.",found:"곳의 카메라 페이지"},
en:{title:"Explore 50 camera sources across Japan",subtitle:"11 guides · 39 external source pages · source links reviewed, broadcasts unverified",search:"Search places and cameras",all:"All",more:"Show more cameras",empty:"No camera matches your filters.",internal:"JAPULSE guide",external:"Source website",watch:"Open source ↗",local:"View camera →",notice:"We do not rebroadcast third-party streams. Check availability and timestamp at the source.",found:"camera pages"},
ja:{title:"日本全国のカメラ50地点を探す",subtitle:"サイト内11件・外部39件。配信元ページを確認済み、現在の配信状況は未確認です。",search:"地域・カメラ名を検索",all:"すべて",more:"もっと見る",empty:"該当するカメラはありません。",internal:"JAPULSE案内",external:"外部配信元",watch:"配信元を見る ↗",local:"カメラを見る →",notice:"第三者の映像は再配信していません。実際の配信状況と撮影時刻は配信元でご確認ください。",found:"地点のカメラページ"},
zh:{title:"探索日本全国50处摄像头资源",subtitle:"站内11处·外部39处，来源页面已核对，实时播放状态仍须自行确认",search:"搜索地区与摄像头",all:"全部",more:"查看更多摄像头",empty:"未找到匹配结果。",internal:"JAPULSE介绍",external:"外部来源",watch:"查看来源 ↗",local:"查看摄像头 →",notice:"本站不擅自转播第三方视频。播放状态和拍摄时间请以原网站为准。",found:"处摄像头页面"}
};
const t=dict[lang]||dict.en;
const areaNames={
hokkaido:{ko:"홋카이도",en:"Hokkaido",ja:"北海道",zh:"北海道"},
kanto:{ko:"간토",en:"Kanto",ja:"関東",zh:"关东"},
chubu:{ko:"주부",en:"Chubu",ja:"中部",zh:"中部"},
kansai:{ko:"간사이",en:"Kansai",ja:"関西",zh:"关西"},
chugoku:{ko:"주고쿠",en:"Chugoku",ja:"中国地方",zh:"中国地方"},
shikoku:{ko:"시코쿠",en:"Shikoku",ja:"四国",zh:"四国"},
kyushu:{ko:"규슈",en:"Kyushu",ja:"九州",zh:"九州"},
okinawa:{ko:"오키나와",en:"Okinawa",ja:"沖縄",zh:"冲绳"}
};
const order=["all","hokkaido","kanto","chubu","kansai","chugoku","shikoku","kyushu","okinawa"];
const heading=document.createElement("div");
heading.className="jp-section-header";
const headingBox=document.createElement("div"),h=document.createElement("h2"),sub=document.createElement("p");
h.textContent=t.title;sub.textContent=t.subtitle;headingBox.append(h,sub);heading.append(headingBox);
const controls=document.createElement("div");controls.className="jp-live-discovery-controls";
const search=document.createElement("input");search.type="search";search.maxLength=120;search.placeholder=t.search;search.setAttribute("aria-label",t.search);
const buttons=document.createElement("div");buttons.className="jp-live-area-buttons";buttons.setAttribute("aria-label",t.all);
const grid=document.createElement("div");grid.className="jp-live-discovery-grid";
const results=document.createElement("p");results.className="jp-live-count";results.setAttribute("aria-live","polite");
const more=document.createElement("button");more.type="button";more.className="jp-live-more";more.textContent=t.more;
const note=document.createElement("p");note.className="jp-live-note";note.textContent=t.notice;
const list=entries.map((entry,i)=>{
 const url=entry.source==="JAPULSE"?"https://japulse.com/"+(lang==="ko"?"":(lang==="zh"?"zh-cn/":lang+"/"))+entry.path:entry.url;
 const a=document.createElement("a");a.className="jp-live-discovery-card";a.href=url;
 if(entry.source!=="JAPULSE"){a.target="_blank";a.rel="noopener noreferrer";}
 const top=document.createElement("div");top.className="jp-live-card-top";
 const region=document.createElement("span");region.className="jp-live-region";region.textContent=areaNames[entry.region]?.[lang]||entry.region;
 const weather=document.createElement("span");weather.className="jp-weather";weather.setAttribute("data-jp-weather",entry.weather);weather.textContent="⌛ --°";weather.title=t.subtitle;
 top.append(region,weather);
 const title=document.createElement("strong");title.textContent=lang==="ko"?entry.ko:entry.en;
 const foot=document.createElement("div");foot.className="jp-live-card-foot";
 const provider=document.createElement("small");provider.textContent=entry.source==="JAPULSE"?t.internal:entry.source+" · "+t.external;
 const action=document.createElement("span");action.textContent=entry.source==="JAPULSE"?t.local:t.watch;
 foot.append(provider,action);a.append(top,title,foot);a.dataset.region=entry.region;
 return {a,entry};
});
let selected="all",visible=6;
for(const area of order){
 const b=document.createElement("button");b.type="button";b.textContent=area==="all"?t.all:(areaNames[area][lang]||area);
 b.className="jp-live-area-button";b.dataset.selected=String(area===selected);b.setAttribute("aria-pressed",String(area===selected));
 b.addEventListener("click",()=>{selected=area;visible=6;[...buttons.children].forEach(el=>{const checked=el===b;el.dataset.selected=String(checked);el.setAttribute("aria-pressed",String(checked));});render();});
 buttons.append(b);
}
function normalize(s){return String(s||"").normalize("NFKC").toLocaleLowerCase().replace(/\s+/g,"");}
function render(){
 const term=normalize(search.value);
 const filtered=list.filter(({entry})=>(selected==="all"||entry.region===selected||(selected==="kyushu"&&entry.region==="okinawa"))&&(!term||normalize([entry.ko,entry.en,entry.region,entry.source,areaNames[entry.region]?.[lang]].join(" ")).includes(term)));
 if(selected!=="all")filtered.sort((a,b)=>Number(b.entry.source==="JAPULSE")-Number(a.entry.source==="JAPULSE"));
 const showing=new Set(filtered.slice(0,visible).map(({a})=>a));
 list.forEach(({a})=>{a.hidden=!showing.has(a);});
 const area=selected==="all"?"":(areaNames[selected]?.[lang]||selected)+" · ";
 results.textContent=area+String(filtered.length)+" "+t.found;
 more.hidden=filtered.length<=visible;
 empty.hidden=filtered.length!==0;
}
more.addEventListener("click",()=>{visible+=9;render();});
search.addEventListener("input",()=>{visible=6;render();});
const empty=document.createElement("p");empty.className="jp-live-empty";empty.textContent=t.empty;empty.hidden=true;
list.forEach(({a})=>grid.append(a));grid.append(empty);
controls.append(search);
if(!directory)controls.append(buttons);
root.append(heading,controls,results,grid,more,note);
if(directory){
 directory.addEventListener("jp-region-changed",event=>{
  const next=event.detail?.region;
  if(next!=="all"&&!order.includes(next))return;
  selected=next;visible=6;search.value="";
  [...buttons.children].forEach(b=>{
   const index=order.indexOf(next),active=order.indexOf(b.textContent===t.all?"all":order.find(code=>(areaNames[code]?.[lang]||code)===b.textContent))===index;
   b.setAttribute("aria-pressed",String(active));
  });
  render();
 });
}
render();
})();