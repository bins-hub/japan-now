/* JAPULSE · GA4 visitor statistics; enabled after optional consent. */
(function () {
  "use strict";
  var MEASUREMENT_ID = "G-G63KG5ES51";
  var KEY = "japulse.analytics.choice.v1";
  var choices = {
    ko: {title:"방문 통계 선택",description:"JAPULSE 개선을 위해 Google Analytics 4로 방문 수, 방문 페이지와 접속 경로를 측정합니다. 동의한 경우에만 통계 태그가 실행됩니다.",yes:"통계 허용",no:"허용 안 함",settings:"통계 쿠키 설정",privacy:"개인정보처리방침"},
    en: {title:"Visitor analytics choice",description:"Help improve JAPULSE with Google Analytics 4 data such as page views and traffic sources. Tracking starts only with your consent.",yes:"Allow analytics",no:"Decline",settings:"Analytics settings",privacy:"Privacy policy"},
    ja: {title:"アクセス解析の選択",description:"JAPULSEの改善のため、Google Analytics 4で閲覧数や流入元を確認します。同意した場合のみ解析タグを読み込みます。",yes:"解析を許可",no:"許可しない",settings:"解析Cookieの設定",privacy:"プライバシーポリシー"},
    "zh-cn": {title:"访问统计设置",description:"为改进JAPULSE，我们使用Google Analytics 4统计页面浏览量与访问来源。仅在您同意后启用统计代码。",yes:"允许统计",no:"拒绝",settings:"统计Cookie设置",privacy:"隐私政策"}
  };
  var htmlLang = (document.documentElement.lang || "ko").toLowerCase();
  var lang = htmlLang.indexOf("zh")===0 ? "zh-cn" : htmlLang.indexOf("ja")===0 ? "ja" : htmlLang.indexOf("en")===0 ? "en" : "ko";
  var t = choices[lang];
  var consent;
  function readConsent(){try{return localStorage.getItem(KEY);}catch(e){return null;}}
  function saveConsent(value){try{localStorage.setItem(KEY,value);}catch(e){}}
  function removeCookies(){
    var names=document.cookie.split(";").map(function(c){return c.split("=")[0].trim();}).filter(function(name){return /^_ga($|_)/.test(name);});
    names.forEach(function(name){var path="; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";document.cookie=name+"="+path;document.cookie=name+"="+path+"; domain="+location.hostname;document.cookie=name+"="+path+"; domain=.japulse.com";});
  }
  var started=false;
  function start(){
    if(started)return;
    started=true;
    window.dataLayer=window.dataLayer||[];
    window.gtag=function(){window.dataLayer.push(arguments);};
    window.gtag("js",new Date());
    window.gtag("config",MEASUREMENT_ID,{allow_google_signals:false,allow_ad_personalization_signals:false});
    var script=document.createElement("script");
    script.async=true;
    script.src="https://www.googletagmanager.com/gtag/js?id="+encodeURIComponent(MEASUREMENT_ID);
    document.head.appendChild(script);
  }
  function css(){
    if(document.getElementById("jn-ga-style"))return;
    var style=document.createElement("style");style.id="jn-ga-style";
    style.textContent=".jn-ga-choice{position:fixed;z-index:9999;bottom:14px;left:14px;right:14px;max-width:570px;margin:auto;background:#faffff;color:#163640;border:1px solid #c8dee0;border-radius:15px;padding:18px;box-shadow:0 12px 46px rgba(0,0,0,.24);font-family:system-ui,-apple-system,sans-serif}.jn-ga-choice strong{display:block;font-size:17px;margin-bottom:7px}.jn-ga-choice p{font-size:13px;line-height:1.65;margin:0 0 10px;color:#45626a}.jn-ga-buttons{display:flex;gap:8px;flex-wrap:wrap}.jn-ga-buttons button{flex:1;min-height:41px;padding:10px 13px;border:1px solid #186c77;border-radius:9px;background:#186c77;color:#fff;font:700 13px system-ui;cursor:pointer}.jn-ga-buttons button:last-child{background:#fff;color:#165967}.jn-ga-choice a{display:inline-block;color:#27646a;font-size:12px;margin-bottom:12px;text-decoration:underline}.jn-ga-footer{display:inline-block;border:0!important;background:transparent!important;color:inherit!important;font-size:12px!important;text-decoration:underline!important;cursor:pointer;padding:8px!important}.jn-ga-choice:focus-visible,.jn-ga-buttons button:focus-visible,.jn-ga-footer:focus-visible{outline:2px solid #f66;outline-offset:2px}@media(max-width:500px){.jn-ga-choice{bottom:8px;left:8px;right:8px;padding:14px}.jn-ga-buttons{flex-direction:column}.jn-ga-buttons button{width:100%}}";
    document.head.appendChild(style);
  }
  function hide(){var node=document.getElementById("jn-ga-choice");if(node)node.remove();}
  function privacyUrl(){return "/"+(lang==="ko"?"":lang+"/")+"privacy/";}
  function panel(){
    hide();css();
    var node=document.createElement("section");node.id="jn-ga-choice";node.className="jn-ga-choice";node.setAttribute("role","dialog");node.setAttribute("aria-modal","false");node.setAttribute("aria-label",t.title);
    var h=document.createElement("strong");h.textContent=t.title;node.appendChild(h);
    var p=document.createElement("p");p.textContent=t.description;node.appendChild(p);
    var a=document.createElement("a");a.href=privacyUrl();a.textContent=t.privacy;node.appendChild(a);
    var buttons=document.createElement("div");buttons.className="jn-ga-buttons";
    [["yes",t.yes],["no",t.no]].forEach(function(entry){
      var b=document.createElement("button");b.type="button";b.textContent=entry[1];
      b.addEventListener("click",function(){
        var previous=readConsent();saveConsent(entry[0]);hide();
        if(entry[0]==="yes")start();
        else if(previous==="yes"){removeCookies();location.reload();}
      });
      buttons.appendChild(b);
    });
    node.appendChild(buttons);document.body.appendChild(node);
  }
  function init(){
    css();consent=readConsent();
    if(consent==="yes")start();
    else if(consent!=="no")panel();
    var footer=document.querySelector("footer");
    if(footer&&!document.getElementById("jn-ga-footer")){
      var control=document.createElement("button");control.type="button";control.id="jn-ga-footer";control.className="jn-ga-footer";control.textContent=t.settings;
      control.addEventListener("click",panel);footer.appendChild(control);
    }
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init,{once:true});
  else init();
})();