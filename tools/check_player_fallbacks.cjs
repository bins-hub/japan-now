/* Exercise the shared player without depending on a live third-party broadcast. */
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');

class Element {
  constructor(tag) { this.tagName = tag; this.children = []; this.style = {}; this.hidden = false; }
  append(...nodes) { for (const node of nodes) { node.parent = this; this.children.push(node); } }
  remove() { if (this.parent) this.parent.children = this.parent.children.filter(node => node !== this); }
  querySelectorAll(selector) {
    const out = [];
    for (const node of this.children) {
      if (node.className === selector.slice(1)) out.push(node);
      out.push(...node.querySelectorAll(selector));
    }
    return out;
  }
}

async function check(lang, expectedSource, expectedFailure) {
  const timers = new Map(); let nextTimer = 1; const players = [];
  const YT = { Player: function (host, options) {
    this.options = options; this.destroy = () => {}; players.push(this);
  } };
  const context = {document: {head: new Element('head'), documentElement: {lang}, createElement: tag => new Element(tag)},
    window: {YT}, YT, location: {origin: 'https://japulse.com'},
    setTimeout(fn, delay) { const id = nextTimer++; timers.set(id, {fn, delay}); return id; },
    clearTimeout(id) { timers.delete(id); }};
  vm.createContext(context);
  vm.runInContext(fs.readFileSync(path.join(__dirname, '../assets/live-player.js'), 'utf8'), context);
  const host = new Element('div');
  const instance = context.window.JapanLivePlayer.mount(host, {title: 'Camera', videos: [{id: 'HjRZNBm1kms', name: 'Camera'}]});
  const panel = host.children[0], bar = panel.children[1], original = bar.children.at(-1);
  assert.equal(original.textContent, expectedSource);
  assert.equal(original.href, 'https://www.youtube.com/watch?v=HjRZNBm1kms');
  instance.play(0); await Promise.resolve();
  assert.equal(timers.size, 1);
  const oldTimer = [...timers.values()][0];
  players.at(-1).options.events.onStateChange({data: 1});
  assert.equal(timers.size, 0, 'successful playback cancels the startup timeout');
  instance.play(0); await Promise.resolve();
  assert.equal(timers.size, 1);
  oldTimer.fn(); // A stale callback must not interrupt the new play request.
  assert.equal(timers.size, 1);
  [...timers.values()][0].fn();
  assert.equal(timers.size, 0, 'timeout cleans up its timer');
  assert.equal(panel.children[0].children[0].children[0].textContent, expectedFailure);
  assert.equal(original.href, 'https://www.youtube.com/watch?v=HjRZNBm1kms');
  instance.destroy(); assert.equal(host.children.length, 0);
}

(async () => {
  await check('ko', 'YouTube 원본 ↗', '현재 재생 가능한 방송을 확인하지 못했습니다');
  await check('en', 'YouTube source ↗', 'No playable broadcast was found');
  await check('ja', 'YouTubeで見る ↗', '再生できる配信が見つかりませんでした');
  await check('zh-CN', 'YouTube原视频 ↗', '未找到可播放的直播');
  console.log('PASS: 4 languages; playback success, stalled startup, stale callbacks, source link and cleanup.');
})().catch(error => { console.error(error); process.exitCode = 1; });
