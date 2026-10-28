"""Restore the two visible Korean-source FAQs without changing camera players."""
from pathlib import Path
import re, html

ROOT=Path(__file__).resolve().parent.parent
COPY={
 'en': {
  'arashiyama': ('Can I see Kyoto’s Arashiyama bamboo grove live?', 'This page provides links to public Arashiyama cameras. Check playback availability on the original broadcast.'),
  'dotonbori': ('Can I see Dotonbori’s current street scene and crowds?', 'Public camera links on the Dotonbori guide show part of the streetscape. Each camera covers only one direction and does not measure overall crowd levels accurately.'),
  'fuji': ('Can a live camera show whether Mount Fuji is visible today?', 'You can refer to a public Mount Fuji camera near Lake Kawaguchi. Check live status and capture time first; visibility can differ from other viewpoints.'),
  'hakata': ('Is there live video around Hakata Station?', 'The Hakata Station camera controls on this page lead to public video and original sources. Check official transport information such as JR for station operations and train timetables.'),
  'iki': ('Where can I see the current sea view on Iki Island, Nagasaki?', 'The Iki Island Kojima Shrine guide provides the original camera link. Do not judge whether coastal access is safe from video alone.'),
  'kabukicho': ('Can I watch live street video from Shinjuku Kabukicho?', 'This page links to the original public Kabukicho camera information and YouTube video. Broadcasting depends on the provider’s circumstances.'),
  'okinawa': ('Where can I watch Okinawa’s sea live?', 'JAPAN NOW links to the original YouTube video for the Bise beach camera. Check official marine and weather information to assess swimming conditions or approaching typhoons.'),
  'osaka-sky': ('Can I watch Osaka’s night view live?', 'Follow the original YouTube link for the Osaka city camera to check playback. Confirm the original broadcast’s indicator to determine whether it is live.'),
  'sapporo': ('Can I watch snow falling in Sapporo through a live camera?', 'Public video links around Odori Park show the weather visible on screen. Refer to official weather and transport information for actual snow depth and road restrictions.'),
  'sensoji': ('Where can I see the current view of Senso-ji in Asakusa?', 'The original-broadcast control on this page opens the camera’s YouTube page. Check the broadcast’s current availability separately.'),
  'shibuya': ('Where can I see the current view of Shibuya Crossing?', 'JAPAN NOW’s Shibuya camera guide links to the provider’s YouTube video and original information. Check the broadcast’s LIVE indicator and time to confirm whether it is currently live.'),
 },
 'ja': {
  'arashiyama': ('京都・嵐山の竹林をライブで見られますか？','このページでは嵐山の公開カメラへのリンクを提供しています。再生できるかは元の配信で確認してください。'),
  'dotonbori': ('道頓堀の現在の様子や混雑を見られますか？','道頓堀の案内ページから公開映像で街の一部を見ることができます。カメラは特定の方向だけを映すため、地域全体の混雑を正確に測定する情報ではありません。'),
  'fuji': ('今日の富士山の見え方をライブカメラで確認できますか？','河口湖周辺の富士山公開カメラを参考にできます。ライブ配信か、撮影時刻はいつかを先に確認し、他の展望場所とは視界が異なることに注意してください。'),
  'hakata': ('博多駅周辺のライブ映像はありますか？','このページの博多駅カメラの操作から公開映像と元の情報源を確認できます。駅の営業や列車の時刻表はJRなどの公式交通案内で確認してください。'),
  'iki': ('長崎県・壱岐島の現在の海の様子はどこで見られますか？','壱岐島・小島神社の案内ページで元のカメラリンクを確認できます。映像だけで海岸への立ち入りが安全だと判断しないでください。'),
  'kabukicho': ('新宿・歌舞伎町の街のライブ映像を見られますか？','このページでは歌舞伎町の公開カメラの元情報とYouTube動画にリンクしています。配信状況は提供者の事情によって変わります。'),
  'okinawa': ('沖縄の海をライブで見られるサイトはありますか？','JAPAN NOWから備瀬の海岸カメラの元のYouTube動画を開けます。遊泳の可否や台風の接近は、必ず公式の海洋・気象情報で判断してください。'),
  'osaka-sky': ('大阪の夜景のライブ映像を見られますか？','大阪市街のカメラの元のYouTube動画リンクから再生状況を確認できます。ライブ配信かどうかは元の表示を確認してください。'),
  'sapporo': ('札幌で雪が降る様子をライブカメラで見られますか？','大通公園周辺の公開映像リンクで画面に映る天気の様子を確認できます。実際の積雪量や道路規制は公式の気象・交通情報を確認してください。'),
  'sensoji': ('浅草・浅草寺の現在の風景はどこで見られますか？','このページの元の配信を開く操作で、カメラのYouTubeページへ移動できます。現在の配信状況は別途確認してください。'),
  'shibuya': ('渋谷スクランブル交差点の現在の様子はどこで見られますか？','JAPAN NOWの渋谷カメラ案内から、提供者のYouTube動画と元の情報を開けます。現在ライブ配信中かどうかは、配信のLIVE表示と時刻を確認してください。'),
 },
 'zh-cn': {
  'arashiyama': ('可以实时观看京都岚山竹林吗？','本页提供岚山公开摄像头链接，请在原始直播页面确认是否可以播放。'),
  'dotonbori': ('可以查看道顿堀当前街景和人流吗？','道顿堀指南中的公开视频可以展示部分街景。摄像头只拍摄特定方向，不能准确衡量整个地区的拥挤程度。'),
  'fuji': ('可以用实时摄像头确认今天能否看清富士山吗？','可以参考河口湖附近的富士山公开摄像头。请先确认是否为直播及拍摄时间，并注意其他观景点的能见度可能不同。'),
  'hakata': ('有博多站周边的实时视频吗？','通过本页的博多站摄像头控件可以查看公开视频和原始来源。车站运营及列车时刻表请查阅JR等官方交通信息。'),
  'iki': ('在哪里可以看长崎壹岐岛当前的海景？','壹岐岛小岛神社指南提供原始摄像头链接。请勿仅凭视频判断海岸是否可以安全进入。'),
  'kabukicho': ('可以观看新宿歌舞伎町街道的直播吗？','本页提供歌舞伎町公开摄像头的原始信息和YouTube视频链接，播出情况可能因提供方而变化。'),
  'okinawa': ('哪里可以实时观看冲绳海景？','JAPAN NOW可打开备濑海滩摄像头的原始YouTube视频。游泳条件和台风接近情况必须查看官方海洋与气象信息。'),
  'osaka-sky': ('可以实时观看大阪夜景吗？','可以通过大阪市区摄像头的原始YouTube链接确认播放状态，是否为直播请查看原始视频的标识。'),
  'sapporo': ('可以通过实时摄像头看札幌下雪吗？','大通公园一带的公开视频链接可以展示画面中的天气情况。实际积雪深度和道路管制请查阅官方气象与交通信息。'),
  'sensoji': ('在哪里可以看浅草寺当前的风景？','本页的原始直播控件可以打开该摄像头的YouTube页面。请另行确认当前播出状态。'),
  'shibuya': ('在哪里可以看涩谷十字路口当前的景象？','JAPAN NOW涩谷摄像头指南提供播出方的YouTube视频与原始信息链接。请确认直播的LIVE标识与时间，判断是否正在实时播出。'),
 }
}
COMMON={
 'en':('Frequently asked questions','Is this view currently live?','Listing a camera page does not guarantee a live broadcast. Check the player or original channel for a LIVE indicator and the latest broadcast time.'),
 'ja':('よくある質問','この映像は現在ライブ配信ですか？','カメラページへの掲載だけではライブ配信を保証しません。プレイヤーまたは元のチャンネルのLIVE表示と最新の配信時刻を確認してください。'),
 'zh-cn':('常见问题','此画面目前是实时直播吗？','收录摄像头页面并不保证正在直播。请查看播放器或原始频道的LIVE标识与最新播出时间。')
}

def run():
 count=0
 for lang,entries in COPY.items():
  heading,q2,a2=COMMON[lang]
  for slug,(q1,a1) in entries.items():
   source=(ROOT/'cameras'/slug/'index.html').read_text()
   assert re.search(r'<article><h2>자주 하는 질문</h2>.*?</article>',source,re.S)
   p=ROOT/lang/'cameras'/slug/'index.html';s=p.read_text()
   # Existing source players may inject buttons dynamically. Never replace them.
   block='<article id="jp-camera-source-faq" class="article"><h2>'+heading+'</h2>'+''.join('<div class="qa"><strong>'+html.escape(q)+'</strong><p>'+html.escape(a)+'</p></div>' for q,a in [(q1,a1),(q2,a2)])+'</article>'
   if 'id="jp-camera-source-faq"' in s:
    s=re.sub(r'<article id="jp-camera-source-faq"[^>]*>.*?</article>',lambda m:block,s,flags=re.S)
   else:
    match=re.search(r'<div class="article"><h2>[^<]+</h2><div class="grid">',s)
    assert match,(p,'Cannot find existing related-camera section')
    s=s[:match.start()]+block+s[match.start():]
   p.write_text(s);count+=1
 print(f'Restored two Korean-source FAQs on {count} localized camera pages.')

if __name__=='__main__':run()
