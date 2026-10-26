
/* JAPULSE optional itinerary helper. Weather is user-supplied, never inferred from cameras. */
(()=>{
"use strict";
const node=document.getElementById("jp-run-plan-mount");
if(!node)return;
const pathname=location.pathname;
const lang=pathname.startsWith("/en/")?"en":pathname.startsWith("/ja/")?"ja":pathname.startsWith("/zh-cn/")?"zh":"ko";
const prefix=lang==="ko"?"":lang==="zh"?"zh-cn/":lang+"/";
const tr={
 ko:{eyebrow:"JAPULSE · WATCH → RUN → EAT",title:"지금 상황에 맞춰 코스 고르기",intro:"장소와 상황을 직접 선택하면 여행 동선을 제안합니다. 날씨·영업정보를 실시간으로 측정하거나 자동 확인한 결과는 아닙니다.",route:"지역 / 코스",weather:"현지 날씨 (직접 선택)",purpose:"하고 싶은 활동",time:"이용 가능한 시간",sun:"맑거나 흐림",rain:"비",heat:"폭염 / 강풍",snow:"눈 / 결빙",run:"러닝 중심",walk:"걷기 중심",eat:"식사 중심",short:"1시간 안팎",medium:"2시간 안팎",long:"반나절",button:"추천 동선 만들기",result:"추천 이동 순서",camera:"카메라 분위기 확인",course:"실제 코스 자료 확인",food:"식당 목록 확인",disclaimer:"제안된 동선은 예시이며 예상 소요 시간·운영시간·이동거리를 보장하지 않습니다. 방문 전 공식 출처와 교통·기상을 확인하세요.",warningRain:"비가 오면 강변·해안가를 피하고 실내 또는 가까운 산책으로 변경하세요.",warningHeat:"폭염·강풍이면 야외 러닝을 권하지 않습니다. 실내 관광과 수분 보충을 우선하세요.",warningSnow:"눈·결빙 시 뛰지 말고 출입 통제와 제설 상태를 확인하세요.",warningClear:"공식 안내의 코스 방향, 보행자 우선 규칙과 현장 공지를 지키세요.",shortTime:"시간이 짧습니다. 전 구간 완주 대신 출발점 주변만 둘러보는 것을 고려하세요.",step1:"1. 영상으로 주변 분위기를 살피되 LIVE 여부는 원본에서 확인",step2:"2. 공식 지도·동선 설명 확인 후 이동",step3:"3. 러닝/산책 종료 뒤 식당의 실제 영업시간 확인"},
 en:{eyebrow:"JAPULSE · WATCH → RUN → EAT",title:"Build a route around your conditions",intro:"Choose the place and conditions yourself. This is a planning guide, not a live forecast or verification of open businesses.",route:"Destination / course",weather:"Local conditions (you select)",purpose:"Your focus",time:"Time available",sun:"Dry / cloudy",rain:"Rain",heat:"Heat / strong wind",snow:"Snow / ice",run:"Run",walk:"Walk",eat:"Food first",short:"About 1 hour",medium:"About 2 hours",long:"Half a day",button:"Build example itinerary",result:"Suggested sequence",camera:"View nearby camera",course:"Open official course info",food:"Find local places to eat",disclaimer:"Suggested stages are examples, not measured journey times, venue schedules or verified route navigation. Recheck transport and local conditions.",warningRain:"Rain: avoid riversides, slippery trails and beaches; prefer indoor alternatives.",warningHeat:"Extreme heat or wind: avoid outdoor runs and prioritize shade, water and indoor activities.",warningSnow:"Snow or ice: do not run until paths and closures have been checked.",warningClear:"Follow official running direction, pedestrian priority and posted local notices.",shortTime:"Short visit: consider a partial walk instead of completing the full run.",step1:"1. Check the camera atmosphere; confirm LIVE status at its publisher",step2:"2. Review the official course map before going",step3:"3. Check restaurant opening information after the run or walk"},
 ja:{eyebrow:"JAPULSE · 見る → 走る → 食べる",title:"現地の状況に合わせてコースを選ぶ",intro:"地域や天候はご自身で選択してください。リアルタイムの天気・店舗営業情報ではありません。",route:"地域・コース",weather:"現地の状況（ご自身で選択）",purpose:"目的",time:"利用できる時間",sun:"晴れ・曇り",rain:"雨",heat:"猛暑・強風",snow:"雪・凍結",run:"ランニング",walk:"散策",eat:"食事を優先",short:"約1時間",medium:"約2時間",long:"半日",button:"訪問の目安を表示",result:"おすすめの流れ",camera:"近隣のカメラ",course:"公式コース資料",food:"周辺の食事先",disclaimer:"所要時間や営業状況を実測・保証するものではありません。交通や気象・施設案内を再確認してください。",warningRain:"雨の時は川辺や海岸、滑りやすい場所を避け、屋内などの代案を検討してください。",warningHeat:"猛暑・強風時の屋外ランニングは避け、休憩と水分補給を優先してください。",warningSnow:"雪や凍結がある時は走らず、除雪状況と規制を確認してください。",warningClear:"指定された走行方向、歩行者優先、現地の掲示を守ってください。",shortTime:"短時間の場合は全コースより一部の散策も検討してください。",step1:"1. 映像の雰囲気を確認し、LIVEは配信元で確認",step2:"2. 公式地図とアクセスを見てから移動",step3:"3. 散策後に飲食店の営業情報を再確認"},
 zh:{eyebrow:"JAPULSE · 看 → 跑 → 吃",title:"根据实际情况选择游览路线",intro:"请自行选择当地状况；这不是实时天气、商户营业或路线可用性的自动检测。",route:"地区／路线",weather:"当地状况（自行选择）",purpose:"主要活动",time:"可用时间",sun:"晴朗／多云",rain:"下雨",heat:"高温／强风",snow:"雪／结冰",run:"跑步",walk:"散步",eat:"优先用餐",short:"约1小时",medium:"约2小时",long:"半天",button:"生成参考行程",result:"建议顺序",camera:"查看周边摄像头",course:"查看官方路线资料",food:"查找当地餐厅",disclaimer:"这只是参考行程，不代表已测量行程耗时、交通或营业情况。请核实天气和官方公告。",warningRain:"下雨时应避开河边和湿滑的海滨道路，考虑室内活动。",warningHeat:"高温或强风时避免户外跑步，优先补水与室内活动。",warningSnow:"雪天或结冰时不要跑步，先确认积雪及通行限制。",warningClear:"遵守官方跑步方向、行人优先和现场提示。",shortTime:"时间较短，可以只在起点附近散步，不必完成整条路线。",step1:"1. 先看周边摄像头，并在原发布方确认直播状态",step2:"2. 查看官方路线地图，再决定前往方式",step3:"3. 跑步或散步后核实餐厅营业情况"}
};
const names={
  ko:["도쿄 황궁","오사카성 공원","교토 가모가와","후쿠오카 오호리공원","삿포로 나카지마공원","오키나와 아라하 해변"],
  en:["Tokyo Imperial Palace","Osaka Castle Park","Kyoto Kamo River","Fukuoka Ohori Park","Sapporo Nakajima Park","Okinawa Araha Beach"],
  ja:["東京・皇居","大阪城公園","京都・鴨川","福岡・大濠公園","札幌・中島公園","沖縄・アラハビーチ"],
  zh:["东京皇居","大阪城公园","京都鸭川","福冈大濠公园","札幌中岛公园","冲绳安良波海滩"]
};
const ids=["tokyo","osaka","kyoto","kyushu","hokkaido","okinawa"];
const sources=[
"https://www.gotokyo.org/en/story/guide/running-course-guide-for-runners/index.html",
"https://www.osakacastlepark.jp/sports/runningmap.html?lang=en",
"https://kyoto.travel/en/destinations/running-coursekamogawa-river/",
"https://www.ohorikouen.jp/map/",
"https://www.sapporosport.org/sapporomachirun/",
"https://chatantourism.com/en/spot/araha-beach/"
];
const cams=["shibuya","dotonbori","arashiyama","hakata","sapporo","okinawa"];
const food=["tokyo","osaka","kyoto","kyushu","", ""];
const text=tr[lang];
const el=(tag,classname,label)=>{let n=document.createElement(tag);if(classname)n.className=classname;if(label)n.textContent=label;return n};
const addOpts=(select,opts)=>opts.forEach(([value,label])=>{const option=el("option","",label);option.value=value;select.append(option)});
node.className="jp-run-planner";
const eyebrow=el("span","jp-plan-kicker",text.eyebrow);
const title=el("h2","",text.title);
const intro=el("p","",text.intro);
const form=el("form","jp-plan-form");form.noValidate=true;
const grid=el("div","jp-plan-grid");
const makeSelect=(label,options)=>{const wrap=el("label","",label);const select=el("select");addOpts(select,options);wrap.append(select);grid.append(wrap);return select};
const route=makeSelect(text.route,ids.map((id,i)=>[id,names[lang][i]]));
const weather=makeSelect(text.weather,[["sun",text.sun],["rain",text.rain],["heat",text.heat],["snow",text.snow]]);
const focus=makeSelect(text.purpose,[["run",text.run],["walk",text.walk],["eat",text.eat]]);
const duration=makeSelect(text.time,[["short",text.short],["medium",text.medium],["long",text.long]]);
const submit=el("button","",text.button);submit.type="submit";
const result=el("div","jp-plan-result");result.hidden=true;result.setAttribute("role","region");result.setAttribute("aria-live","polite");
form.append(grid,submit);node.append(eyebrow,title,intro,form,result);
const link=(href,label)=>{const a=el("a","",label);a.href=href;return a};
form.addEventListener("submit",event=>{
  event.preventDefault();
  const i=ids.indexOf(route.value),id=ids[i],weatherValue=weather.value;
  const weatherNote=weatherValue==="rain"?text.warningRain:weatherValue==="heat"?text.warningHeat:weatherValue==="snow"?text.warningSnow:text.warningClear;
  result.replaceChildren();
  const h=el("h3","",text.result+": "+names[lang][i]);result.append(h);
  const ol=el("ol");
  let sequences=[text.step1,text.step2,text.step3];
  if(focus.value==="eat")sequences=[text.step1,text.step3,text.step2];
  if(focus.value==="walk")sequences=[text.step1,text.step2,text.step3];
  sequences.forEach(s=>ol.append(el("li","",s)));
  result.append(ol,el("p","jp-plan-warning",weatherNote));
  if(duration.value==="short")result.append(el("p","jp-plan-disclaimer",text.shortTime));
  const links=el("div","jp-plan-links");
  const camHref="https://japulse.com/"+prefix+"cameras/"+cams[i]+"/";
  links.append(link(camHref,text.camera),link(sources[i],text.course));
  links.children[1].target="_blank";links.children[1].rel="noopener noreferrer";
  if(food[i])links.append(link("https://japulse.com/"+prefix+"local-food/#"+food[i],text.food));
  else links.append(link("https://www.google.com/maps/search/?api=1&query="+encodeURIComponent(names.en[i]+" restaurant"),text.food));
  result.append(links,el("p","jp-plan-disclaimer",text.disclaimer));
  result.hidden=false;
});
})();
