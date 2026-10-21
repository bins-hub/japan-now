/* JAPULSE PWA trial: opt-in install only; no intrusive interstitial or page caches. */
(function(){"use strict";
if(!window.isSecureContext)return;
const standalone=()=>window.matchMedia("(display-mode: standalone)").matches||window.navigator.standalone===true;
if("serviceWorker" in navigator)window.addEventListener("load",()=>{navigator.serviceWorker.register("/sw.js",{scope:"/",updateViaCache:"none"}).catch(()=>{});},{once:true});
const lang=(document.documentElement.lang||"ko").toLowerCase();
const code=lang.startsWith("ja")?"ja":lang.startsWith("en")?"en":lang.startsWith("zh")?"zh":"ko";
const labels={
ko:{button:"JAPULSE 앱 설치",title:"JAPULSE 홈 화면에 설치",tip:"Safari 공유 버튼(□↑) → '홈 화면에 추가'를 선택하세요. Chrome에서 열었다면 Safari로 접속해 주세요.",close:"닫기"},
en:{button:"Install JAPULSE",title:"Add JAPULSE to your home screen",tip:"In Safari, tap Share (□↑), then 'Add to Home Screen'. Open this site in Safari if needed.",close:"Close"},
ja:{button:"JAPULSEをインストール",title:"ホーム画面にJAPULSEを追加",tip:"Safariの共有ボタン（□↑）→「ホーム画面に追加」を選択してください。必要に応じてSafariで開いてください。",close:"閉じる"},
zh:{button:"安装JAPULSE",title:"添加JAPULSE到主屏幕",tip:"请在Safari中点击分享按钮（□↑），选择“添加到主屏幕”。如有需要，请先在Safari中打开网站。",close:"关闭"}
};
const t=labels[code],isIOS=/iPad|iPhone|iPod/.test(navigator.userAgent)||(/Macintosh/.test(navigator.userAgent)&&navigator.maxTouchPoints>1),isAndroid=/Android/i.test(navigator.userAgent);
const androidTips={ko:"Chrome 오른쪽 위 ⋮ 메뉴에서 '앱 설치' 또는 '홈 화면에 추가'를 선택하세요. 다른 앱에서 열었다면 Chrome에서 다시 열어 주세요.",en:"In Chrome, open the ⋮ menu and select 'Install app' or 'Add to Home screen'. Open in Chrome if you're using an in-app browser.",ja:"Chromeの⋮メニューから「アプリをインストール」または「ホーム画面に追加」を選択してください。アプリ内ブラウザの場合はChromeで開いてください。",zh:"请在Chrome的⋮菜单中选择“安装应用”或“添加到主屏幕”。若是在应用内浏览器中，请先用Chrome打开。"};
let deferred=null,button=null,dialog=null;
try{if(Number(localStorage.getItem("japulse.pwa.dismissUntil")||0)>Date.now())return;}catch(e){}
if(standalone())return;
function closeDialog(){if(dialog){dialog.remove();dialog=null;}}
function dismiss(){try{localStorage.setItem("japulse.pwa.dismissUntil",String(Date.now()+7*24*3600*1000));}catch(e){} closeDialog();if(button){button.remove();button=null;}}
function ensureButton(){if(button||standalone())return;
 const css=document.createElement("style");css.textContent=".jp-pwa-cta{position:fixed;z-index:65;right:14px;bottom:calc(14px + env(safe-area-inset-bottom,0px));padding:9px 13px;border:1px solid #eff8f9;border-radius:999px;background:#125f69;color:white;font:800 12px/1.3 system-ui,-apple-system,sans-serif;box-shadow:0 3px 12px #0b26323c;max-width:calc(100vw - 48px);cursor:pointer}.jp-pwa-close{position:fixed;z-index:66;right:7px;bottom:calc(37px + env(safe-area-inset-bottom,0px));background:#fff;color:#20525b;border:1px solid #b5d0d4;border-radius:99px;font:700 11px system-ui;padding:2px 6px;cursor:pointer}.jp-pwa-panel{position:fixed;z-index:70;bottom:calc(60px + env(safe-area-inset-bottom,0px));right:14px;left:auto;width:min(340px,calc(100vw - 28px));background:#fff;color:#163e47;border:1px solid #b8d5d9;border-radius:14px;box-shadow:0 9px 30px #091d3650;padding:18px;font-family:system-ui;line-height:1.6}.jp-pwa-panel h2{margin:0 0 7px;font-size:16px}.jp-pwa-panel p{font-size:13px;margin:0 0 12px}.jp-pwa-panel button{padding:7px 14px;border-radius:9px;border:1px solid #bdced4;background:white;color:#154b55;font-weight:800}";
 document.head.append(css);
 button=document.createElement("button");button.type="button";button.className="jp-pwa-cta";button.textContent="↧  "+t.button;button.setAttribute("aria-label",t.button);button.addEventListener("click",installNow);document.body.append(button);
 const x=document.createElement("button");x.type="button";x.className="jp-pwa-close";x.textContent="×";x.setAttribute("aria-label",t.close);x.addEventListener("click",()=>{x.remove();dismiss();});document.body.append(x);
 button._dismissEl=x;
}
function showIOS(){closeDialog();dialog=document.createElement("section");dialog.className="jp-pwa-panel";dialog.setAttribute("role","dialog");dialog.setAttribute("aria-label",t.title);
 const h=document.createElement("h2");h.textContent=t.title;const p=document.createElement("p");p.textContent=isIOS?t.tip:androidTips[code];const close=document.createElement("button");close.type="button";close.textContent=t.close;close.addEventListener("click",closeDialog);dialog.append(h,p,close);document.body.append(dialog);}
async function installNow(){
 if(standalone()){if(button){button._dismissEl?.remove();button.remove();button=null;}return;}
 if(deferred){const evt=deferred;deferred=null;try{await evt.prompt();await evt.userChoice;}catch(e){}if(button){button._dismissEl?.remove();button.remove();button=null;}return;}
 if(isIOS||isAndroid)showIOS();
}
window.addEventListener("beforeinstallprompt",e=>{e.preventDefault();deferred=e;ensureButton();});
window.addEventListener("appinstalled",()=>{closeDialog();if(button){button._dismissEl?.remove();button.remove();button=null;}});
if(isIOS||isAndroid){if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",ensureButton,{once:true});else ensureButton();}
})();