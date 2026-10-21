/* Real, opt-in JAPULSE Firebase Realtime Database presence.
   Imports SDK only AFTER public Firebase web config is supplied.
   Never synthesizes a visitor count; always hidden when connection fails. */
import { firebaseConfig } from "./presence-config.js";
const valid = !!firebaseConfig &&
  ["apiKey","authDomain","projectId","appId","databaseURL"].every(k =>
    typeof firebaseConfig[k] === "string" && firebaseConfig[k].length > 2);
if (valid && window.isSecureContext) {
  const locale = (document.documentElement.lang||"ko").toLowerCase();
  const lang = locale.startsWith("en")?"en":locale.startsWith("ja")?"ja":locale.startsWith("zh")?"zh":"ko";
  const strings = {
    ko:{one:"현재 JAPULSE 접속 중",many:"지금 함께 JAPULSE 보는 중",unit:"명"},
    en:{one:"On JAPULSE right now",many:"Exploring Japan together",unit:" online"},
    ja:{one:"現在JAPULSEにアクセス中",many:"今、一緒に日本を見ています",unit:"人"},
    zh:{one:"当前访问JAPULSE",many:"正在一起看日本",unit:"人"}
  }[lang];
  const badge = document.createElement("div");
  badge.className="jp-presence jp-presence-verified";
  badge.setAttribute("role","status");
  badge.setAttribute("aria-live","off");
  badge.hidden=true;
  const dot=document.createElement("span");dot.className="jp-presence-dot";dot.setAttribute("aria-hidden","true");
  const label=document.createElement("span");label.className="jp-presence-label";
  const number=document.createElement("strong");number.className="jp-presence-number";
  badge.append(dot,label,number);
  (document.querySelector("main")||document.body).prepend(badge);
  const hide=()=>{badge.hidden=true;};
  const version="12.0.0";
  const url="https://www.gstatic.com/firebasejs/"+version+"/";
  async function init(){
    const [appMod,authMod,database]=await Promise.all([
      import(url+"firebase-app.js"),import(url+"firebase-auth.js"),import(url+"firebase-database.js")
    ]);
    const app=appMod.initializeApp(firebaseConfig,"japulse-live-presence");
    const auth=authMod.getAuth(app);
    await authMod.setPersistence(auth,authMod.browserLocalPersistence);
    await auth.authStateReady();
    const user=auth.currentUser||(await authMod.signInAnonymously(auth)).user;
    if(!user||!user.uid)return;
    const db=database.getDatabase(app);
    const all=database.ref(db,"presence/v1");
    const mine=database.ref(db,"presence/v1/"+user.uid);
    let online=false,registered=false;
    database.onValue(database.ref(db,".info/connected"),async snap=>{
      online=snap.val()===true;
      if(!online){registered=false;hide();return;}
      try{
        const conn=database.push(mine);
        await database.onDisconnect(conn).remove();
        await database.set(conn,true);
        registered=true;
      }catch(_){registered=false;hide();}
    },hide);
    database.onValue(all,snap=>{
      if(!online||!registered){hide();return;}
      const count=snap.exists()?snap.numChildren():0;
      if(!Number.isSafeInteger(count)||count<1){hide();return;}
      label.textContent=count===1?strings.one:strings.many;
      number.textContent=count.toLocaleString(lang==="ja"?"ja-JP":lang==="zh"?"zh-CN":lang==="en"?"en-US":"ko-KR")+strings.unit;
      badge.setAttribute("aria-label",label.textContent+" "+number.textContent);
      badge.hidden=false;
    },hide);
    window.addEventListener("offline",hide);
  }
  init().catch(hide);
}
