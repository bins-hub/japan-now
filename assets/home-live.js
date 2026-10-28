/* JAPULSE camera viewer: direct YouTube iframe, explicit user-play option and source fallback. */
(function () {
"use strict";
const root=document.querySelector("[data-jp-home-live]"); if(!root) return;
const frame=root.querySelector("[data-jp-live-frame]");
const stage=root.querySelector("[data-jp-live-screen]");
const status=root.querySelector("[data-jp-live-status]");
const overlay=root.querySelector("[data-jp-live-overlay-message]");
const retry=root.querySelector("[data-jp-live-retry]");
const sourceLink=root.querySelector(".jp-home-live-info a[href*='youtube.com/watch']");
const title=root.querySelector(".jp-home-live-info strong");
const topLabel=root.querySelector(".jp-home-live-label");
const note=root.querySelector(".jp-home-live-note");
if(!frame||!stage||!status||!overlay||!retry) return;
const lang=(document.documentElement.lang||"ko").toLowerCase();
const key=lang.startsWith("en")?"en":lang.startsWith("ja")?"ja":lang.startsWith("zh")?"zh":"ko";
const tr={
ko:{select:"작은 화면을 눌러 위의 영상 바꾸기",play:"▶ 영상 재생하기",open:"YouTube 원본 보기 ↗",hint:"재생되지 않으면 YouTube 원본을 여세요. 실제 LIVE 여부는 원본에서 확인하세요.",name:" · 공개 카메라"},
en:{select:"Select a thumbnail to switch video",play:"▶ Play video",open:"View on YouTube ↗",hint:"If playback fails, use YouTube. Confirm LIVE status at source.",name:" · public camera"},
ja:{select:"サムネイルで動画を切り替え",play:"▶ 動画を再生",open:"YouTubeで見る ↗",hint:"再生できない場合はYouTubeへ。LIVE状態は配信元で確認してください。",name:" · 公開カメラ"},
zh:{select:"点击缩略图切换视频",play:"▶ 播放视频",open:"在 YouTube 观看 ↗",hint:"播放失败请前往YouTube。直播状态以来源为准。",name:" · 公开视频"}
}[key];
const cams=[
{id:"8H3nRCFVR6Y",names:{ko:"도쿄 시부야",en:"Tokyo Shibuya",ja:"東京・渋谷",zh:"东京涩谷"}},
{id:"6OgYfTMOmhY",names:{ko:"오사카 도톤보리",en:"Osaka Dotonbori",ja:"大阪・道頓堀",zh:"大阪道顿堀"}},
{id:"1cnReFAU04k",names:{ko:"후지산",en:"Mount Fuji",ja:"富士山",zh:"富士山"}},
{id:"RBHsITnIoI0",names:{ko:"삿포로",en:"Sapporo",ja:"札幌",zh:"札幌"}},
{id:"JLlY6Cg17cc",names:{ko:"교토 아라시야마",en:"Kyoto Arashiyama",ja:"京都・嵐山",zh:"京都岚山"}},
{id:"yETDDgrE2E4",names:{ko:"후쿠오카 하카타",en:"Fukuoka Hakata",ja:"福岡・博多",zh:"福冈博多"}}
];
let active=cams.find(c=>c.id===root.getAttribute("data-video-id"))||cams[0];
const toolbar=document.createElement("div"); toolbar.className="jp-home-cam-sourcebar";
toolbar.style.cssText="padding:9px 12px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;background:#123441";
const open=document.createElement("a");open.target="_blank";open.rel="noopener noreferrer";open.textContent=tr.open;
open.style.cssText="display:inline-block;background:#ff6653;color:#102832;padding:9px 12px;border-radius:8px;font-weight:700;text-decoration:none";
const hint=document.createElement("span");hint.textContent=tr.hint;hint.style.cssText="font-size:12px;line-height:1.5;color:#dce7ec";
toolbar.append(open,hint);
const switcher=document.createElement("div");switcher.className="jp-home-cam-switcher";
const heading=document.createElement("div");heading.className="jp-home-cam-heading";heading.textContent=tr.select;
const track=document.createElement("div");track.className="jp-home-cam-track";switcher.append(heading,track);
const buttons=[];
for(const cam of cams){
const btn=document.createElement("button");btn.type="button";btn.className="jp-home-cam-choice";
btn.setAttribute("aria-label",cam.names[key]);
const thumb=document.createElement("span");thumb.className="jp-home-cam-thumb";
const img=document.createElement("img");img.src="https://i.ytimg.com/vi/"+cam.id+"/hqdefault.jpg";
img.alt="";img.loading="lazy";img.width=160;img.height=90;
img.addEventListener("error",()=>{img.src="/assets/camera-placeholder.svg"},{once:true});
const icon=document.createElement("span");icon.className="jp-home-cam-play";icon.textContent="▶";thumb.append(img,icon);
const name=document.createElement("span");name.className="jp-home-cam-name";name.textContent=cam.names[key];
btn.append(thumb,name);btn.addEventListener("click",()=>choose(cam,true));track.append(btn);buttons.push({cam,btn});
}
if(note)root.insertBefore(switcher,note);else root.append(switcher);
if(note)root.insertBefore(toolbar,note);else root.append(toolbar);
function mount(auto){
frame.replaceChildren();
const iframe=document.createElement("iframe");
iframe.title=active.names[key]+" YouTube";
iframe.src="https://www.youtube.com/embed/"+encodeURIComponent(active.id)+"?playsinline=1&rel=0&autoplay="+(auto?"1":"0")+"&mute="+(auto?"1":"0");
iframe.allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
iframe.referrerPolicy="strict-origin-when-cross-origin";
iframe.setAttribute("allowfullscreen","");
iframe.style.cssText="width:100%;height:100%;border:0;display:block";
frame.appendChild(iframe);
stage.classList.add("is-playing");retry.hidden=true;
status.textContent=tr.hint;
overlay.textContent=tr.hint;
}
function choose(cam,play){
active=cam;root.setAttribute("data-video-id",cam.id);
if(title)title.textContent=cam.names[key]+tr.name;
if(topLabel)topLabel.textContent="◉ JAPAN CAMERA · "+cam.names[key];
if(sourceLink)sourceLink.href="https://www.youtube.com/watch?v="+cam.id;
open.href="https://www.youtube.com/watch?v="+cam.id;
stage.style.backgroundImage='url("https://i.ytimg.com/vi/'+cam.id+'/hqdefault.jpg")';
buttons.forEach(item=>item.btn.setAttribute("aria-pressed",String(item.cam.id===cam.id)));
frame.replaceChildren();stage.classList.remove("is-playing");
status.textContent=tr.hint;overlay.textContent=tr.hint;
retry.textContent=tr.play;retry.hidden=false;
if(play)mount(true);
}
retry.addEventListener("click",()=>mount(false));
choose(active,true);
// Native YouTube iframe avoids depending on the iframe API; user click starts playback.
// Cross-origin playback restrictions are controlled by the video publisher.
})();