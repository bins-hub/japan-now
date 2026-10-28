/* JAPULSE homepage hero camera: one muted YouTube preview, with accessible click fallback. */
(function () {
  "use strict";
  const root = document.querySelector("[data-jp-home-live]");
  if (!root) return;
  let activeId = root.getAttribute("data-video-id");
  if (!/^[A-Za-z0-9_-]{11}$/.test(activeId || "")) return;
  const frame = root.querySelector("[data-jp-live-frame]");
  const stage = root.querySelector("[data-jp-live-screen]");
  const status = root.querySelector("[data-jp-live-status]");
  const overlayMessage = root.querySelector("[data-jp-live-overlay-message]");
  const retry = root.querySelector("[data-jp-live-retry]");
  if (!frame || !stage || !status || !overlayMessage || !retry) return;
  const lang = (document.documentElement.lang || "ko").toLowerCase();
  const key = lang.startsWith("zh") ? "zh" : lang.startsWith("ja") ? "ja" : lang.startsWith("en") ? "en" : "ko";
  const copy = {
    ko: { loading:"음소거로 영상 연결 중", playing:"영상 재생 중 · 실제 LIVE 여부는 원본에서 확인", blocked:"자동재생이 차단되었습니다. 재생을 눌러 주세요.", error:"현재 이 영상을 재생할 수 없습니다. YouTube 원본에서 확인해 주세요.", ended:"영상이 종료되었습니다. 원본 방송을 확인해 주세요.", alternate:"다른 시부야 카메라로 자동 연결 중…", reduced:"데이터 절약/모션 설정에 따라 자동재생을 건너뛰었습니다.", retry:"▶ 재생하기" },
    en: { loading:"Connecting video (muted)", playing:"Playing · confirm LIVE status at source", blocked:"Autoplay was blocked. Tap play to continue.", error:"Video unavailable here. Check the original source.", alternate:"Trying another Shibuya camera…", ended:"This video has ended. Check the source.", reduced:"Autoplay skipped due to data saving/motion settings.", retry:"▶ Play video" },
    ja: { loading:"ミュートで動画に接続中", playing:"動画再生中 · LIVE配信かは配信元で確認", blocked:"自動再生が制限されています。再生を押してください。", error:"再生できません。配信元でご確認ください。", alternate:"別の渋谷カメラに接続しています…", ended:"動画が終了しました。配信元をご確認ください。", reduced:"データ節約・視覚効果の設定により自動再生を停止しています。", retry:"▶ 動画を再生" },
    zh: { loading:"静音连接视频中", playing:"视频播放中 · 请以来源网站为准确认直播状态", blocked:"浏览器阻止了自动播放，请点击播放。", error:"无法播放视频，请查看原始来源。", alternate:"正在尝试其他涩谷摄像头…", ended:"视频已结束，请查看来源。", reduced:"根据省流量/减少动态效果设置，已跳过自动播放。", retry:"▶ 播放视频" }
  }[key];

  // Only one video is ever embedded: the thumbnail buttons simply switch its source.
  // These are existing JAPULSE camera candidates, NOT verified currently-live streams.
  const cameras = [
    { id:"8H3nRCFVR6Y", names:{ko:"도쿄 시부야",en:"Tokyo Shibuya",ja:"東京・渋谷",zh:"东京涩谷"} },
    { id:"i2PpmC1IeKk", names:{ko:"오사카 도톤보리",en:"Osaka Dotonbori",ja:"大阪・道頓堀",zh:"大阪道顿堀"} },
    { id:"1cnReFAU04k", names:{ko:"후지산",en:"Mount Fuji",ja:"富士山",zh:"富士山"} },
    { id:"RBHsITnIoI0", names:{ko:"삿포로",en:"Sapporo",ja:"札幌",zh:"札幌"} },
    { id:"JLlY6Cg17cc", names:{ko:"교토 아라시야마",en:"Kyoto Arashiyama",ja:"京都・嵐山",zh:"京都岚山"} },
    { id:"yETDDgrE2E4", names:{ko:"후쿠오카 하카타",en:"Fukuoka Hakata",ja:"福岡・博多",zh:"福冈博多"} }
  ];
  // Broadcasts may end or restrict embedding. Try alternate PUBLIC original uploads
  // for the SAME Shibuya crossing before showing an error. Never claim LIVE status.
  const alternativeFeeds = {
    "8H3nRCFVR6Y": [
      "dfVK7ld38Ys", // FNN Prime Online, Shibuya camera
      "BBQpLKc1P04", // ANNnewsCH, another Shibuya live broadcast
      "f50R4vDlCmA"  // iTSCOM, Shibuya camera
    ]
  };
  let alternateIndex = 0;
  const labels = {
    ko:{title:"카메라 선택",hint:"작은 화면을 눌러 위의 영상 바꾸기",camera:" · 공개 카메라"},
    en:{title:"Choose a camera",hint:"Tap a thumbnail to switch the main video",camera:" · public camera"},
    ja:{title:"カメラを選択",hint:"小さな画面を押すと上の映像が切り替わります",camera:" · 公開カメラ"},
    zh:{title:"选择摄像头",hint:"点击缩略图可切换上方视频",camera:" · 公开视频"}
  }[key];
  const videoName = root.querySelector(".jp-home-live-info strong");
  const sourceLink = root.querySelector(".jp-home-live-info a[href*='youtube.com/watch']");
  const topLabel = root.querySelector(".jp-home-live-label");
  const originalNote = root.querySelector(".jp-home-live-note");
  const switcher = document.createElement("div");
  switcher.className = "jp-home-cam-switcher";
  switcher.setAttribute("role","group");
  switcher.setAttribute("aria-label", labels.title);
  const switcherHeading = document.createElement("div");
  switcherHeading.className = "jp-home-cam-heading";
  switcherHeading.textContent = labels.hint;
  const track = document.createElement("div");
  track.className = "jp-home-cam-track";
  const thumbnails = cameras.map(function(camera) {
    const button = document.createElement("button");
    button.type="button";
    button.className="jp-home-cam-choice";
    button.setAttribute("aria-label",camera.names[key]);
    button.setAttribute("aria-pressed",String(camera.id===activeId));
    const thumbnail=document.createElement("span");
    thumbnail.className="jp-home-cam-thumb";
    const img=document.createElement("img");
    img.addEventListener("error",function(){img.src="https://japulse.com/assets/camera-placeholder.svg";},{once:true});
    img.src="https://i.ytimg.com/vi/"+camera.id+"/hqdefault.jpg";
    img.alt="";
    img.loading="lazy";
    img.decoding="async";
    img.width=160;
    img.height=90;
    const icon=document.createElement("span");
    icon.className="jp-home-cam-play";
    icon.setAttribute("aria-hidden","true");
    icon.textContent="▶";
    thumbnail.append(img,icon);
    const name=document.createElement("span");
    name.className="jp-home-cam-name";
    name.textContent=camera.names[key];
    button.append(thumbnail,name);
    button.addEventListener("click",function(){ selectCamera(camera); });
    track.appendChild(button);
    return {button,camera};
  });
  switcher.append(switcherHeading,track);
  if(originalNote)root.insertBefore(switcher,originalNote);
  else root.appendChild(switcher);
  function selectCamera(camera) {
    if (camera.id === activeId) {
      // A failed, currently selected camera can be retried directly.
      if (!playing) { alternateIndex = 0; resetPlayer(); start(); }
      return;
    }
    alternateIndex = 0;
    activeId = camera.id;
    root.setAttribute("data-video-id",activeId);
    stage.style.backgroundImage='url("https://i.ytimg.com/vi/'+activeId+'/hqdefault.jpg")';
    if(videoName)videoName.textContent=camera.names[key]+labels.camera;
    if(sourceLink)sourceLink.href="https://www.youtube.com/watch?v="+encodeURIComponent(activeId);
    if(topLabel)topLabel.textContent="◉ JAPAN CAMERA · "+camera.names[key];
    thumbnails.forEach(function(item){
      item.button.setAttribute("aria-pressed",String(item.camera.id===activeId));
    });
    clearTimer();
    playing=false;
    waiting();
    if (player && ready) {
      try { player.mute(); player.loadVideoById(activeId); }
      catch (_) { fallback(copy.error); return; }
      watchTimer=setTimeout(function(){if(!playing)fallback(copy.blocked);},12000);
    } else if (!connecting) start();
  }
  let player = null, connecting = false, ready = false, playing = false, watchTimer = 0, apiPromise = null, playSeq = 0;
  function clearTimer() { if (watchTimer) { clearTimeout(watchTimer); watchTimer = 0; } }
  function waiting() {
    status.textContent = copy.loading;
    overlayMessage.textContent = copy.loading;
    retry.hidden = true;
    stage.classList.remove("is-playing");
  }
  function fallback(message, sourceOnly) {
    clearTimer();
    status.textContent = message;
    overlayMessage.textContent = message;
    retry.textContent = sourceOnly ? (key === "ko" ? "▶ YouTube 원본 보기" : key === "ja" ? "▶ YouTubeで見る" : key === "zh" ? "▶ 在 YouTube 观看" : "▶ Watch on YouTube") : copy.retry;
    retry.dataset.sourceOnly = sourceOnly ? "1" : "0";
    retry.hidden = false;
    stage.classList.remove("is-playing");
  }
  function resetPlayer() {
    ++playSeq;
    clearTimer();
    try { if (player) player.destroy(); } catch (_) {}
    player = null; connecting = false; ready = false; playing = false;
    frame.replaceChildren();
    stage.classList.remove("is-playing");
  }
  function tryAnotherTokyoFeed() {
    const feeds = alternativeFeeds[activeId] || [];
    if (alternateIndex >= feeds.length) return false;
    const nextId = feeds[alternateIndex++];
    resetPlayer();
    status.textContent = copy.alternate;
    overlayMessage.textContent = copy.alternate;
    retry.hidden = true;
    if (sourceLink) sourceLink.href = "https://www.youtube.com/watch?v=" + encodeURIComponent(nextId);
    stage.style.backgroundImage = 'url("https://i.ytimg.com/vi/' + nextId + '/hqdefault.jpg")';
    start(nextId);
    return true;
  }
  function loadApi() {
    if (window.YT && typeof window.YT.Player === "function") return Promise.resolve(window.YT);
    if (apiPromise) return apiPromise;
    apiPromise = new Promise(function (resolve, reject) {
      let finished = false;
      const previous = window.onYouTubeIframeAPIReady;
      const timeout = setTimeout(function () {
        if (!finished) { finished = true; reject(new Error("YouTube API timeout")); }
      }, 15000);
      window.onYouTubeIframeAPIReady = function () {
        if (typeof previous === "function") { try { previous(); } catch (_) {} }
        if (!finished) { finished = true; clearTimeout(timeout); resolve(window.YT); }
      };
      const script = document.createElement("script");
      script.src = "https://www.youtube.com/iframe_api";
      script.async = true;
      script.onerror = function () { if (!finished) { finished = true; clearTimeout(timeout); reject(new Error("YouTube API unavailable")); } };
      document.head.appendChild(script);
    }).catch(function (err) { apiPromise = null; throw err; });
    return apiPromise;
  }
  function start(sourceOverride) {
    if (connecting) return;
    if (player && ready) {
      waiting();
      try { player.mute(); player.playVideo(); } catch (_) { fallback(copy.error); return; }
      watchTimer = setTimeout(function () { if (!playing) fallback(copy.blocked); }, 12000);
      return;
    }
    connecting = true;
    waiting();
    const seq = ++playSeq;
    const cameraIdAtStart = activeId;
    const requestedId = sourceOverride || activeId;
    clearTimer();
    watchTimer=setTimeout(function(){if(seq===playSeq&&!playing){resetPlayer();fallback(copy.error);}},20000);
    loadApi().then(function (YT) {
      if (seq !== playSeq) return;
      frame.replaceChildren();
      const holder = document.createElement("div");
      frame.appendChild(holder);
      player = new YT.Player(holder, {
        width: "100%", height: "100%", videoId: requestedId,
        playerVars: { autoplay: 1, mute: 1, playsinline: 1, controls: 1, rel: 0, origin: location.origin },
        events: {
          onReady: function (event) {
            if (seq !== playSeq) return;
            connecting = false; ready = true;
            try { event.target.mute(); if (activeId !== cameraIdAtStart) event.target.loadVideoById(activeId); else event.target.playVideo(); } catch (_) { fallback(copy.blocked); }
            clearTimer();
            watchTimer = setTimeout(function () { if (!playing) fallback(copy.blocked); }, 12000);
          },
          onStateChange: function (event) {
            if (seq !== playSeq) return;
            if (event.data === 1) {
              playing = true; clearTimer(); stage.classList.add("is-playing");
              retry.hidden = true; status.textContent = copy.playing;
            } else if (event.data === 0) {
              playing = false;
              if (!tryAnotherTokyoFeed()) fallback(copy.ended);
            } else if (event.data === 2 || event.data === 3 || event.data === 5) {
              playing = false;
            }
          },
          onAutoplayBlocked: function () {
            if (seq !== playSeq) return;
            playing = false; connecting = false; fallback(copy.blocked);
          },
          onError: function (event) {
            if (seq !== playSeq) return;
            resetPlayer();
            if (!tryAnotherTokyoFeed()) fallback(copy.error, event && (event.data === 100 || event.data === 101 || event.data === 150));
          }
        }
      });
    }).catch(function () {
      if (seq !== playSeq) return;
      connecting = false; ready = false; fallback(copy.error);
    });
  }
  retry.addEventListener("click", function () {
    if (retry.dataset.sourceOnly === "1") {
      const href = sourceLink && sourceLink.href ? sourceLink.href : "https://www.youtube.com/watch?v=" + encodeURIComponent(activeId);
      window.open(href, "_blank", "noopener,noreferrer");
      return;
    }
    alternateIndex = 0;
    if (sourceLink) sourceLink.href = "https://www.youtube.com/watch?v=" + encodeURIComponent(activeId);
    stage.style.backgroundImage = 'url("https://i.ytimg.com/vi/' + activeId + '/hqdefault.jpg")';
    resetPlayer();
    start();
  });
  let pausedForHidden=false;
  document.addEventListener("visibilitychange", function () {
    if (!player || !ready) return;
    try {
      if (document.hidden && playing) { pausedForHidden=true; player.pauseVideo(); }
      else if (!document.hidden && pausedForHidden) { pausedForHidden=false; player.mute(); player.playVideo(); }
    } catch (_) {}
  });
  const reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const saveData = !!(navigator.connection && navigator.connection.saveData);
  if (reducedMotion || saveData) fallback(copy.reduced);
  else start();
})();
