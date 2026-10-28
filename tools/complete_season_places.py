"""Publish translated destination cards from the Korean seasonal guides; keep existing localized sections."""
from pathlib import Path
import re
from html import escape,unescape
ROOT=Path(__file__).resolve().parent.parent
RAW='''아라시야마|Arashiyama|嵐山|岚山
도후쿠지|Tofukuji|東福寺|东福寺
기요미즈데라|Kiyomizudera|清水寺|清水寺
오사카성 공원|Osaka Castle Park|大阪城公園|大阪城公园
만박기념공원|Expo ’70 Commemorative Park|万博記念公園|万博纪念公园
미노오 폭포|Minoh Falls|箕面大滝|箕面瀑布
마루야마 공원|Maruyama Park|円山公園|圆山公园
나카지마 공원|Nakajima Park|中島公園|中岛公园
모이와산|Mount Moiwa|藻岩山|藻岩山
고이시카와 고라쿠엔|Koishikawa Korakuen|小石川後楽園|小石川后乐园
메이지진구 가이엔|Meiji Jingu Gaien|明治神宮外苑|明治神宫外苑
다카오산|Mount Takao|高尾山|高尾山
철학의 길|Philosopher’s Path|哲学の道|哲学之道
게마 사쿠라노미야 공원|Kema Sakuranomiya Park|毛馬桜之宮公園|毛马樱之宫公园
홋카이도 신궁|Hokkaido Jingu|北海道神宮|北海道神宫
모에레누마 공원|Moerenuma Park|モエレ沼公園|莫埃来沼公园
우에노 공원|Ueno Park|上野公園|上野公园
치도리가후치|Chidorigafuchi|千鳥ヶ淵|千鸟渊
나카메구로|Nakameguro|中目黒|中目黑
후시미 이나리|Fushimi Inari|伏見稲荷|伏见稻荷
교토 철도박물관|Kyoto Railway Museum|京都鉄道博物館|京都铁道博物馆
나카노시마|Nakanoshima|中之島|中之岛
가이유칸|Osaka Aquarium Kaiyukan|海遊館|海游馆
오도리 공원|Odori Park|大通公園|大通公园
신주쿠 교엔|Shinjuku Gyoen|新宿御苑|新宿御苑
마루노우치·도쿄역 주변|Marunouchi and Tokyo Station|丸の内・東京駅周辺|丸之内与东京站周边
사가아라시야마역|Saga-Arashiyama Station|嵯峨嵐山駅|嵯峨岚山站
도후쿠지역|Tofukuji Station|東福寺駅|东福寺站
기요미즈고조역|Kiyomizu-Gojo Station|清水五条駅|清水五条站
오사카조코엔역|Osakajokoen Station|大阪城公園駅|大阪城公园站
반파쿠키넨코엔역|Bampaku-kinen-koen Station|万博記念公園駅|万博纪念公园站
미노오역|Minoh Station|箕面駅|箕面站
마루야마코엔역|Maruyama Koen Station|円山公園駅|圆山公园站
나카지마코엔역|Nakajima Koen Station|中島公園駅|中岛公园站
로프웨이 교통 연계|Connect to the ropeway|ロープウェイへの接続交通|换乘前往缆车的交通
로프웨이 접근 교통 연계|Connect to the ropeway|ロープウェイへの接続交通|换乘前往缆车的交通
이다바시역|Iidabashi Station|飯田橋駅|饭田桥站
가이엔마에역|Gaienmae Station|外苑前駅|外苑前站
다카오산구치역|Takaosanguchi Station|高尾山口駅|高尾山口站
기온시조역|Gion-Shijo Station|祇園四条駅|祇园四条站
긴카쿠지 주변 정류장|Bus stops near Ginkakuji|銀閣寺周辺のバス停|银阁寺附近巴士站
사쿠라노미야역|Sakuranomiya Station|桜ノ宮駅|樱之宫站
버스·도보 연계|Bus and walking connection|バス・徒歩の接続|巴士与步行接驳
우에노역|Ueno Station|上野駅|上野站
구단시타역|Kudanshita Station|九段下駅|九段下站
나카메구로역|Nakameguro Station|中目黒駅|中目黑站
이나리역|Inari Station|稲荷駅|稻荷站
우메코지교토니시역|Umekoji-Kyotonishi Station|梅小路京都西駅|梅小路京都西站
요도야바시역|Yodoyabashi Station|淀屋橋駅|淀屋桥站
오사카코역|Osakako Station|大阪港駅|大阪港站
지하철 오도리역|Odori Subway Station|地下鉄大通駅|地铁大通站
지하철 마루야마코엔역|Maruyama Koen Subway Station|地下鉄円山公園駅|地铁圆山公园站
강과 산의 가을 풍경|Autumn river and mountain scenery|川と山の秋景色|河流与山间秋景
사찰·계곡 단풍|Temple and valley foliage|寺院・渓谷の紅葉|寺院与峡谷红叶
사찰과 단풍 숲|Temple and autumn woodland|寺院と紅葉の森|寺院与红叶树林
성곽과 단풍|Castle scenery and autumn foliage|城郭と紅葉|城郭与红叶
도심 외곽 넓은 숲|Extensive woodland outside the centre|郊外に広がる森|市区外围的广阔树林
계곡과 산지 단풍|Valley and mountain foliage|渓谷と山の紅葉|峡谷与山地红叶
가을 숲 산책|Autumn woodland walk|秋の森の散策|秋季森林散步
연못과 단풍|Ponds and autumn foliage|池と紅葉|池塘与红叶
산지 단풍과 전망|Mountain foliage and views|山の紅葉と眺望|山地红叶与眺望
은행나무 가로수|Ginkgo-lined avenue|イチョウ並木|银杏林荫道
산길 단풍|Autumn mountain trails|山道の紅葉|山路红叶
기온 인근 벚꽃 명소|Cherry blossoms near Gion|祇園近くの桜の名所|祇园附近赏樱地
수로 옆 벚꽃 산책|Cherry-blossom walk by a canal|水路沿いの桜散策|水渠旁赏樱散步
도게쓰교와 강변 벚꽃|Togetsukyo Bridge and riverside blossoms|渡月橋と川沿いの桜|渡月桥与河畔樱花
성곽 주변 벚꽃|Blossoms around the castle|城郭周辺の桜|城郭周边樱花
강변 벚꽃길|Riverside cherry-blossom paths|川沿いの桜並木|河畔樱花步道
넓은 벚꽃 공원|Spacious cherry-blossom park|広々とした桜の公園|宽阔的樱花公园
봄철 꽃놀이|Spring blossom viewing|春の花見|春季赏花
신궁 경내 벚꽃|Cherry blossoms in shrine grounds|神宮境内の桜|神宫院内樱花
넓은 조경 공원|Extensive landscaped park|広大な景観公園|广阔的景观公园
넓은 벚꽃 산책로|Broad cherry-blossom walking paths|広い桜の散策路|宽阔的赏樱步道
해자 주변 벚꽃길|Cherry-blossom paths by the moat|堀沿いの桜道|护城河旁樱花步道
메구로강 벚꽃 산책|Meguro River blossom walk|目黒川の桜散策|目黑川赏樱散步
겨울 사찰 풍경|Winter temple scenery|冬の寺院風景|冬季寺院景色
도리이길 야외 산책|Outdoor walk through torii gates|鳥居の道を屋外散策|鸟居步道户外散步
실내 전시|Indoor exhibitions|屋内展示|室内展览
겨울 도심 산책|Winter city walk|冬の街歩き|冬季市内散步
강변 건축물과 야경|Riverside architecture and night views|川沿いの建築と夜景|河畔建筑与夜景
추운 날 실내 관광|Indoor sightseeing on cold days|寒い日の屋内観光|寒冷天气的室内观光
삿포로 중심부 겨울 산책·설경|Winter walk and snow scenery in central Sapporo|札幌中心部の冬の散策・雪景色|札幌市中心冬季散步与雪景
도심 숲 산책과 눈길 풍경|Urban woodland and snowy paths|市街地の森と雪道の景色|城市森林散步与雪路景观
시내 전망과 겨울 산지 풍경|City views and winter mountain scenery|市街地の眺望と冬山の景色|城市眺望与冬季山景'''
WORDS={r.split('|')[0]:r.split('|')[1:] for r in RAW.splitlines()}
COPY=[dict(places='Three places to explore',access='Nearby transport',map='Map and directions',route='Compare the route between places',itinerary='Plan a day or half-day visit',plan='Start with the first place below, take a lunch break, then choose the next stop after checking the actual travel time. Split widely separated locations across different days. This is a suggested sequence, not a transport timetable.',budget='Transport, budget and preparation',cost='Add the fares and admission fees of the actual facilities you select. Public walking areas and paid attractions have different conditions. Check opening hours and ticket rules with each operator.',faq='Seasonal travel questions',question='Is the best viewing date guaranteed?',answer='No. Bloom, foliage and snow conditions vary with temperature, altitude and location. A forecast is different from an on-site observation. Check current conditions before leaving.',short='What if I have only half a day?',shortanswer='Choose one area around the first destination, leave time for food and rest, and check your return transport.',photo='Reference photo, not a live view',credit='Original photo and license',prepare=['Bring a warm layer and comfortable walking shoes.','Bring comfortable shoes and allow for blossom-season crowds.','Bring warm clothing; in snowy areas choose shoes with good grip.']),
dict(places='おすすめの3か所',access='近くの交通拠点',map='地図・経路',route='場所間の移動経路を比較',itinerary='1日・半日のモデルプラン',plan='下記の最初の場所から始め、昼食・休憩を挟んで実際の移動時間を確認して次の場所を選びます。離れた場所は日を分けましょう。訪問順の提案であり交通時刻表ではありません。',budget='交通・予算・準備',cost='利用する交通機関と施設の料金を合計してください。無料の散策エリアと有料施設では条件が異なります。営業時間とチケット条件は各運営者の案内をご確認ください。',faq='季節旅行のよくある質問',question='見頃の日付は確定していますか？',answer='いいえ。開花・紅葉・積雪は気温、標高、場所によって異なります。予測と現地の観測結果は別です。出発前に現在の状況を確認してください。',short='半日しかない場合は？',shortanswer='最初の目的地周辺で1つのエリアを選び、食事・休憩の時間と帰りの交通を確保しましょう。',photo='参考写真・ライブ映像ではありません',credit='写真原本・ライセンス',prepare=['上着と歩きやすい靴を用意してください。','歩きやすい靴を用意し、花見の混雑に余裕を持ちましょう。','防寒着を用意し、積雪地では滑りにくい靴を選んでください。']),
dict(places='推荐游览的三个地点',access='附近交通节点',map='地图与路线',route='比较地点之间的交通路线',itinerary='规划一日或半日行程',plan='可从下方第一个地点开始，安排午餐休息，再确认实际交通时间后选择下一站。相距较远的地点建议分日游览。这是参观顺序建议，并非交通时刻表。',budget='交通、预算与准备',cost='按实际选择的交通和设施合计车费与门票。公共散步区域与收费景点的条件不同，请向各运营方确认开放时间和购票条件。',faq='季节旅行常见问题',question='最佳观赏日期已确定吗？',answer='没有。开花、红叶和积雪会随气温、海拔及地点变化。预测与现场观测并不相同，请在出发前确认当前情况。',short='只有半天时间怎么办？',shortanswer='选择第一个目的地周边的一个区域，并预留用餐、休息和返程交通时间。',photo='参考照片，并非实时画面',credit='照片原图与许可',prepare=['准备外套和舒适的步行鞋。','准备舒适的鞋，并为赏樱人流预留时间。','准备保暖衣物，积雪地区选择防滑鞋。'])]

def run():
 for source in sorted((ROOT/'season').glob('*/*/index.html')):
  rel=source.relative_to(ROOT);raw=source.read_text()
  # Tokyo's winter guide has a distinct, data-rich layout and is handled separately.
  if str(rel)=='season/winter/tokyo/index.html':continue
  details=re.findall(r'<details class="jp-season-place">(.*?)</details>',raw,re.S)
  for i,lang in enumerate(['en','ja','zh-cn']):
   p=ROOT/lang/rel;h=p.read_text();c=COPY[i]
   if 'id="jp-season-places"' in h:continue
   places=[];block='<div id="jp-season-places"><section class="panel"><h2>'+c['places']+'</h2>'
   for detail in details:
    ko=re.sub('<[^>]+>','',re.search(r'<summary[^>]*>(.*?)</summary>',detail,re.S)[1]).split(' ·')[0]
    name=WORDS[ko][i];places.append(name)
    values=re.findall(r'<p><strong>(?:주요 볼거리|볼거리|가까운 교통 거점|교통 거점):</strong>\s*(.*?)</p>',detail,re.S)
    urls=re.findall(r'href="(https://www.google.com/maps/[^\"]+)"',detail)
    block+='<details><summary>'+escape(name)+'</summary><div><p>'+WORDS[values[0]][i]+'</p><p><strong>'+c['access']+': </strong>'+WORDS[values[1]][i]+'</p>'
    if urls:block+='<a class="btn" href="'+urls[0]+'" target="_blank" rel="noopener noreferrer">'+c['map']+' ↗</a>'
    block+='</div></details>'
   block+='</section>'
   routeurls=list(dict.fromkeys(re.findall(r'href="(https://www.google.com/maps/dir/[^\"]+)"',raw)))
   if routeurls:block+='<section class="panel"><h2>'+c['route']+'</h2>'+''.join('<a class="btn" href="'+u+'" target="_blank" rel="noopener noreferrer">'+c['map']+' '+str(n+1)+' ↗</a>' for n,u in enumerate(routeurls))+'</section>'
   block+='<section class="panel"><h2>'+c['itinerary']+'</h2><p>'+c['plan']+'</p><ol>'+''.join('<li>'+escape(name)+'</li>' for name in places)+'</ol></section>'
   season=rel.parts[1];idx={'autumn':0,'cherry-blossoms':1,'winter':2}[season]
   block+='<section class="panel"><h2>'+c['budget']+'</h2><p>'+c['cost']+'</p><p>'+c['prepare'][idx]+'</p></section>'
   block+='<section class="panel"><h2>'+c['faq']+'</h2><h3>'+c['question']+'</h3><p>'+c['answer']+'</p><h3>'+c['short']+'</h3><p>'+c['shortanswer']+'</p></section></div>'
   h=h.replace('</main>',block+'</main>')
   h=h.replace('</head>','<style>#jp-season-places details{padding:16px 0;border-bottom:1px solid #64818a}#jp-season-places summary{cursor:pointer;font-weight:700;min-height:44px}#jp-season-places a{overflow-wrap:anywhere}</style></head>')
   p.write_text(h)
 print('Added Korean-guide place cards, transport nodes, map routes, planning and FAQs to 33 localized seasonal pages. Distinct winter Tokyo guide is separate.')
if __name__=='__main__':run()
