/* JAPULSE sticky preview: independent layer; original YouTube player remains in place. */
(function () {
  "use strict";
  var root = document.querySelector("[data-jp-home-live]");
  if (!root) return;
  var stage = root.querySelector("[data-jp-live-screen]");
  if (!stage || !stage.parentNode) return;
  var header = document.querySelector(".jp-bar");
  var media = window.matchMedia("(max-width: 839px)");
  var placeholder = document.createElement("div");
  placeholder.className = "jp-home-sticky-placeholder";
  placeholder.hidden = true;
  placeholder.setAttribute("aria-hidden", "true");
  stage.parentNode.insertBefore(placeholder, stage);

  var lang = (document.documentElement.lang || "ko").toLowerCase();
  var key = lang.indexOf("zh") === 0 ? "zh" : lang.indexOf("ja") === 0 ? "ja" : lang.indexOf("en") === 0 ? "en" : "ko";
  var labels = {
    ko: ["이전 카메라", "다음 카메라", "작은 영상 닫기"],
    en: ["Previous camera", "Next camera", "Close floating video"],
    ja: ["前のカメラ", "次のカメラ", "小さい動画を閉じる"],
    zh: ["上一个摄像头", "下一个摄像头", "关闭悬浮视频"]
  }[key];
  var controls = document.createElement("div");
  controls.className = "jp-home-sticky-controls";
  controls.setAttribute("role", "group");
  controls.setAttribute("aria-label", labels[2]);
  function addButton(glyph, label, callback) {
    var button = document.createElement("button");
    button.type = "button";
    button.textContent = glyph;
    button.setAttribute("aria-label", label);
    button.title = label;
    button.addEventListener("click", callback);
    controls.appendChild(button);
  }
  function switchCamera(direction) {
    var choices = Array.prototype.slice.call(root.querySelectorAll(".jp-home-cam-choice"));
    if (!choices.length) return;
    var index = choices.findIndex(function (choice) { return choice.getAttribute("aria-pressed") === "true"; });
    var next = (index + direction + choices.length) % choices.length;
    choices[next].click(); // Reuse the existing one-iframe camera-switch function.
  }
  var floating = false;
  var dismissed = false;
  var pending = false;
  function headerBottom() {
    return header ? Math.max(0, header.getBoundingClientRect().bottom) : 0;
  }
  function setFloating(value) {
    if (floating === value) return;
    floating = value;
    if (value) {
      placeholder.style.height = stage.getBoundingClientRect().height + "px";
      placeholder.hidden = false;
      stage.classList.add("jp-is-floating");
    } else {
      stage.classList.remove("jp-is-floating");
      placeholder.hidden = true;
    }
  }
  function update() {
    pending = false;
    if (!media.matches) {
      dismissed = false;
      setFloating(false);
      return;
    }
    var bottom = headerBottom();
    stage.style.setProperty("--jp-floating-top", Math.ceil(bottom + 8) + "px");
    var origin = floating ? placeholder : stage;
    var originBottom = origin.getBoundingClientRect().bottom;
    if (dismissed && originBottom >= bottom + 20) dismissed = false;
    var wantsFloating = !dismissed && originBottom < bottom - 4;
    // Keep the small video from obscuring content on short landscape screens.
    if (window.innerHeight < 390) wantsFloating = false;
    setFloating(wantsFloating);
  }
  function schedule() {
    if (pending) return;
    pending = true;
    window.requestAnimationFrame(update);
  }
  addButton("‹", labels[0], function () { switchCamera(-1); });
  addButton("›", labels[1], function () { switchCamera(1); });
  addButton("×", labels[2], function () {
    dismissed = true;
    setFloating(false);
    schedule();
  });
  stage.appendChild(controls);
  window.addEventListener("scroll", schedule, {passive:true});
  window.addEventListener("resize", schedule, {passive:true});
  if (media.addEventListener) media.addEventListener("change", schedule);
  else if (media.addListener) media.addListener(schedule);
  schedule();
})();
