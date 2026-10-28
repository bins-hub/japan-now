"""Translate the distinct Tokyo winter guide's practical information from its Korean source."""
from pathlib import Path
import re
import html
ROOT=Path(__file__).resolve().parent.parent
DATA={
'en':[
('Tokyo winter weather','December 7.7°C · January 5.4°C · February 6.1°C. These are Japan Meteorological Agency 1991–2020 monthly climate normals for Tokyo, not the forecast for your travel date. Bring a coat and scarf; it feels colder after sunset.'),
('Ueno Park','Metropolitan park area: 05:00–23:00, free to walk around. Approximately 2 minutes on foot from JR / Tokyo Metro Ueno Station, or 1 minute from Keisei Ueno Station. Nearby museums have separate opening hours and admission fees.'),
('Shinjuku Gyoen','1 October–14 March: 09:00–16:30; last entry 16:00. Normally closed Mondays (the next weekday if Monday is a holiday), and 29 December–3 January. Adult admission ¥500; children aged 15 and under are free. Student and senior discounts have eligibility requirements.'),
('Marunouchi and Tokyo Station','Street walking is free. Combine the garden during daylight with Tokyo Station / Marunouchi after sunset. Individual 2026–2027 illumination events have separate confirmed dates; a suggested evening walk does not confirm an event is running.'),
('Rail transport','JR Yamanote Line is one option between Ueno and Tokyo stations. Compare the actual route from Shinjuku Gyoen to Ueno based on your departure point and the travel date.'),
('Suggested one-day itinerary','10:00–11:30 Shinjuku Gyoen → 11:30–13:00 lunch around Shinjuku → 13:00–15:30 Ueno Park → after 16:00 Tokyo Station / Marunouchi for food and night views. Add transport time between places. This is a suggested schedule, not train times or measured journey durations. Museum admission and opening times are separate.'),
('Admission budget','Ueno Park walking: free. Shinjuku Gyoen: adult ¥500. Marunouchi street walking: free. Minimum ordinary admission for these three walks is therefore ¥500 per adult; transport, meals, museums and paid events are additional.'),
('Can I plan on seeing snow?','Central Tokyo does not have persistent winter snow. Parks, night views and indoor museums are more dependable activities than planning a trip solely for snow.'),
('What is the simplest route?','Morning Shinjuku Gyoen → afternoon Ueno Park → evening Tokyo Station. Check the garden’s 16:00 winter last entry and the separate opening times of any museums you add.')],
'ja':[
('東京の冬の気候','12月7.7°C・1月5.4°C・2月6.1°C。気象庁の東京観測所における1991〜2020年の月平均平年値で、旅行当日の予報ではありません。コートやマフラーを用意し、日没後の冷え込みに備えましょう。'),
('上野公園','都立公園区域は05:00〜23:00、散策無料。JR・東京メトロ上野駅から徒歩約2分、京成上野駅から約1分。周辺の博物館はそれぞれ営業時間・入館料が異なります。'),
('新宿御苑','10月1日〜3月14日は09:00〜16:30、最終入園16:00。原則月曜休園（月曜が休日の場合は翌平日）、12月29日〜1月3日休園。一般¥500、15歳以下無料。学生・65歳以上の割引には条件があります。'),
('丸の内・東京駅周辺','街歩き自体は無料。昼間に庭園を見て、日没後に東京駅・丸の内の夜景を楽しむ流れが適しています。2026〜2027年のイルミネーションは各主催者が確定した開催日を別途確認してください。散策の提案はイベント開催を保証するものではありません。'),
('鉄道での移動','上野駅と東京駅の間はJR山手線などを利用できます。新宿御苑から上野へは出発地点によって乗り換えが異なるため、旅行当日の実際の経路を比較しましょう。'),
('1日のモデルコース','10:00〜11:30新宿御苑 → 11:30〜13:00新宿周辺で昼食 → 13:00〜15:30上野公園 → 16:00以降東京駅・丸の内で食事と夜景。場所間の移動時間を追加してください。時刻は旅程案で、鉄道時刻表や実測移動時間ではありません。博物館を加える場合は個別の料金・営業時間を確認しましょう。'),
('入場料の予算','上野公園散策は無料、新宿御苑は大人¥500、丸の内の街歩きは無料。3か所の通常の散策に必要な最低入場料は大人1人¥500です。交通、食事、博物館、有料イベントは別料金です。'),
('雪景色を前提にできますか？','東京中心部は冬に常時積雪がある地域ではありません。雪だけを目的にするより、公園、夜景、屋内の美術館・博物館を組み合わせると計画を立てやすくなります。'),
('最も簡単な回り方は？','午前は新宿御苑、午後は上野公園、夕方は東京駅周辺。新宿御苑の冬季最終入園16:00と、追加する博物館の営業時間を別々に確認してください。')],
'zh-cn':[
('东京冬季气候','12月7.7°C、1月5.4°C、2月6.1°C。这是日本气象厅东京观测站1991—2020年月平均气温常年值，并非旅行当天预报。建议准备外套和围巾，并注意日落后降温。'),
('上野公园','都立公园区域05:00—23:00，散步免费。从JR／东京地铁上野站步行约2分钟，从京成上野站约1分钟。附近各博物馆的开放时间与门票另计。'),
('新宿御苑','10月1日至3月14日09:00—16:30，最后入园16:00。原则上周一休园（如遇节假日则顺延至下一个工作日），12月29日至1月3日休园。成人¥500，15岁及以下免费；学生和65岁以上优惠有相应条件。'),
('丸之内与东京站周边','街道散步免费。适合白天游览庭园，日落后到东京站与丸之内观赏夜景。2026—2027年灯光活动的日期应分别查看各主办方的确定公告；推荐夜间散步不代表活动正在举办。'),
('铁路交通','上野站与东京站之间可选择JR山手线等线路。从新宿御苑到上野的换乘方式因出发位置而异，请比较旅行当天的实际路线。'),
('一日推荐行程','10:00—11:30新宿御苑 → 11:30—13:00新宿附近午餐 → 13:00—15:30上野公园 → 16:00以后东京站／丸之内用餐与看夜景。请另行加入地点间交通时间。这是行程建议，并非列车时刻或实测交通时长。若加入博物馆，需确认其单独门票与开放时间。'),
('门票预算','上野公园散步免费，新宿御苑成人¥500，丸之内街道散步免费。因此这三处普通散步的最低门票费用为每位成人¥500。交通、餐饮、博物馆和收费活动另计。'),
('能以看雪为主要安排吗？','东京市中心冬季并非常年积雪地区。与仅为雪景安排行程相比，公园、夜景与室内美术馆、博物馆的组合更稳妥。'),
('最简单的路线是什么？','上午新宿御苑，下午上野公园，傍晚东京站周边。请确认新宿御苑冬季最后入园16:00，并分别查看所加博物馆的开放时间。')]}
def align_place_details(lang, h, source):
 # The source repeats its gallery photos inside three expandable place cards.
 # Reuse translated venue facts rather than adding a second copy of them.
 photos=re.findall(r'<details class="jp-season-place">.*?<img[^>]+src="([^"]+)".*?</details>',source,re.S)
 credits=[('Nesnad, CC BY 4.0', 'Ueno%20Park%20-%202026%20Feb%2016%20various%2017.jpg'),('Mycomp, CC BY-SA 4.0','Shinjuku%20Gyoen%20(Park).jpg'),('Procrastinator acc, CC0 1.0','Tokyo%20station%20night.jpg')]
 labels={'en':('Show place details','Reference photo, not a live view'), 'ja':('場所の詳細を開く','参考写真・ライブ映像ではありません'), 'zh-cn':('展开地点详情','参考照片，并非实时画面')}
 assert len(photos)==3
 for i,(title,text) in enumerate(DATA[lang][1:4]):
  old='<section class="panel"><h2>'+title+'</h2><p>'+text+'</p></section>'
  if old not in h:
   assert f'data-jp-winter-place="{i}"' in h
   continue
  credit,file=credits[i]
  picture='<img loading="lazy" decoding="async" src="'+photos[i]+'" alt="'+html.escape(title+' · '+labels[lang][1],quote=True)+'" style="width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:12px;margin:10px 0" referrerpolicy="no-referrer">'
  attribution='<small>'+labels[lang][1]+' · <a href="https://commons.wikimedia.org/wiki/File:'+file+'" target="_blank" rel="noopener noreferrer">'+credit+' / Wikimedia Commons</a></small>'
  new='<section class="panel" data-jp-winter-place="'+str(i)+'"><details class="jp-season-place"><summary aria-label="'+html.escape(title+' · '+labels[lang][0],quote=True)+'"><h2 style="display:inline;font-size:1.2em">'+title+'</h2></summary><div class="jp-season-place-detail">'+picture+attribution+'<p>'+text+'</p></div></details></section>'
  assert h.count(old)==1
  h=h.replace(old,new)
 return h

def run():
 source=(ROOT/'season/winter/tokyo/index.html').read_text()
 urls=list(dict.fromkeys(re.findall(r'href="(https://[^\"]+)"',source)))
 external=[u for u in urls if not any(x in u for x in ['japulse.com','wikimedia.org','creativecommons.org'])]
 for lang,sections in DATA.items():
  p=ROOT/lang/'season/winter/tokyo/index.html';h=p.read_text()
  if 'id="jp-tokyo-winter-details"' in h:
   p.write_text(align_place_details(lang,h,source))
   continue
  label={'en':'Official information and maps','ja':'公式情報・地図','zh-cn':'官方信息与地图'}[lang]
  block='<div id="jp-tokyo-winter-details">'+''.join('<section class="panel"><h2>'+title+'</h2><p>'+text+'</p></section>' for title,text in sections)
  block+='<section class="panel"><h2>'+label+'</h2><ul>'+''.join('<li><a href="'+u+'" target="_blank" rel="noopener noreferrer">'+u.split('/')[2]+' ↗</a></li>' for u in external)+'</ul></section></div>'
  p.write_text(align_place_details(lang,h.replace('</main>',block+'</main>'),source))
 print('Translated Tokyo winter climate, venue hours, prices, transport, itinerary, budget, FAQs and source/map links into all three languages.')
if __name__=='__main__':run()
