/* JAPULSE homepage hero camera: one muted YouTube preview, with accessible click fallback. */
(function () {
  "use strict";
  const root = document.querySelector("[data-jp-home-live]");
  if (!root) return;
  const id = root.getAttribute("data-video-id");
  if (!/^[A-Za-z0-9_-]{11}$/.test(id || "")) return;
  const frame = root.querySelector("[data-jp-live-frame]");
  const stage = root.querySelector("[data-jp-live-screen]");
  const status = root.querySelector("[data-jp-live-status]");
  const overlayMessage = root.querySelector("[data-jp-live-overlay-message]");
  const retry = root.querySelector("[data-jp-live-retry]");
  if (!frame || !stage || !status || !overlayMessage || !retry) return;
  const lang = (document.documentElement.lang || "ko").toLowerCase();
  const key = lang.startsWith("zh") ? "zh" : lang.startsWith("ja") ? "ja" : lang.startsWith("en") ? "en" : "ko";
  const copy = {
    ko: { loading:"음소거로 영상 연결 중", playing:"영상 재생 중 · 실제 LIVE 여부는 원본에서 확인", blocked:"자동재생이 차단되었습니다. 재생을 눌러 주세요.", error:"영상을 재생할 수 없습니다. 원본 링크를 확인해 주세요.", ended:"영상이 종료되었습니다. 원본 방송을 확인해 주세요.", reduced:"데이터 절약/모션 설정에 따라 자동재생을 건너뛰었습니다.", retry:"▶ 재생하기" },
    en: { loading:"Connecting video (muted)", playing:"Playing · confirm LIVE status at source", blocked:"Autoplay was blocked. Tap play to continue.", error:"Video unavailable here. Check the original source.", ended:"This video has ended. Check the source.", reduced:"Autoplay skipped due to data saving/motion settings.", retry:"▶ Play video" },
    ja: { loading:"ミュートで動画に接続中", playing:"動画再生中 · LIVE配信かは配信元で確認", blocked:"自動再生が制限されています。再生を押してください。", error:"再生できません。配信元でご確認ください。", ended:"動画が終了しました。配信元をご確認ください。", reduced:"データ節約・視覚効果の設定により自動再生を停止しています。", retry:"▶ 動画を再生" },
    zh: { loading:"静音连接视频中", playing:"视频播放中 · 请以来源网站为准确认直播状态", blocked:"浏览器阻止了自动播放，请点击播放。", error:"无法播放视频，请查看原始来源。", ended:"视频已结束，请查看来源。", reduced:"根据省流量/减少动态效果设置，已跳过自动播放。", retry:"▶ 播放视频" }
  }[key];
  let player = null, connecting = false, ready = false, playing = false, watchTimer = 0, apiPromise = null;
  function clearTimer() { if (watchTimer) { clearTimeout(watchTimer); watchTimer = 0; } }
  function waiting() {
    status.textContent = copy.loading;
    overlayMessage.textContent = copy.loading;
    retry.hidden = true;
    stage.classList.remove("is-playing");
  }
  function fallback(message) {
    clearTimer();
    status.textContent = message;
    overlayMessage.textContent = message;
    retry.textContent = copy.retry;
    retry.hidden = false;
    stage.classList.remove("is-playing");
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
  function start() {
    if (connecting) return;
    if (player && ready) {
      waiting();
      try { player.mute(); player.playVideo(); } catch (_) { fallback(copy.error); return; }
      watchTimer = setTimeout(function () { if (!playing) fallback(copy.blocked); }, 12000);
      return;
    }
    connecting = true;
    waiting();
    loadApi().then(function (YT) {
      frame.replaceChildren();
      const holder = document.createElement("div");
      frame.appendChild(holder);
      player = new YT.Player(holder, {
        width: "100%", height: "100%", videoId: id,
        playerVars: { autoplay: 1, mute: 1, playsinline: 1, controls: 1, rel: 0, origin: location.origin },
        events: {
          onReady: function (event) {
            connecting = false; ready = true;
            try { event.target.mute(); event.target.playVideo(); } catch (_) { fallback(copy.blocked); }
            clearTimer();
            watchTimer = setTimeout(function () { if (!playing) fallback(copy.blocked); }, 12000);
          },
          onStateChange: function (event) {
            if (event.data === 1) {
              playing = true; clearTimer(); stage.classList.add("is-playing");
              retry.hidden = true; status.textContent = copy.playing;
            } else if (event.data === 0) {
              playing = false; fallback(copy.ended);
            } else if (event.data === 2 || event.data === 3 || event.data === 5) {
              playing = false;
            }
          },
          onAutoplayBlocked: function () { playing = false; connecting = false; fallback(copy.blocked); },
          onError: function () {
            playing = false; ready = false; connecting = false;
            try { player.destroy(); } catch (_) {}
            player = null; frame.replaceChildren(); fallback(copy.error);
          }
        }
      });
    }).catch(function () { connecting = false; ready = false; fallback(copy.error); });
  }
  retry.addEventListener("click", function () { start(); });
  document.addEventListener("visibilitychange", function () {
    if (!player || !ready) return;
    try {
      if (document.hidden && playing) player.pauseVideo();
      else if (!document.hidden && playing) { player.mute(); player.playVideo(); }
    } catch (_) {}
  });
  const reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const saveData = !!(navigator.connection && navigator.connection.saveData);
  if (reducedMotion || saveData) fallback(copy.reduced);
  else start();
})();
