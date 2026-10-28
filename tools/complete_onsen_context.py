"""Localize the Korean guides' access, images and bathing conditions without removing existing content."""
from pathlib import Path
import re
from html import escape, unescape

ROOT=Path(__file__).resolve().parent.parent
# Each row is the Korean guide's access information in en, ja and zh-CN.
ACCESS={
'arima':['From Kobe, use connecting trains or a bus.','神戸から鉄道を乗り継ぐか、バスでアクセス。','从神户换乘铁路或乘坐巴士前往。'],
'atami':['Use JR Atami Station.','JR熱海駅を利用。','利用JR热海站。'],
'beppu':['From Beppu Station, take a city bus to the chosen hot-spring district.','別府駅から市内バスで各温泉地区へ。','从别府站乘市内巴士前往各温泉区。'],
'dogo':['Take a Matsuyama city tram to Dogo Onsen Station.','松山市内の路面電車で道後温泉駅へ。','乘松山市内有轨电车前往道后温泉站。'],
'gero':['Use JR Gero Station.','JR下呂駅を利用。','利用JR下吕站。'],
'ginzan':['Take a bus from Oishida Station.','大石田駅からバスを利用。','从大石田站乘巴士前往。'],
'hakone':['From Odawara Station, continue by Hakone mountain railway or bus.','小田原駅から箱根の登山電車・バスで各地区へ。','从小田原站换乘箱根登山电车或巴士进入各区域。'],
'jozankei':['Take a Jozankei-bound bus from Sapporo.','札幌から定山渓行きのバスを利用。','从札幌乘开往定山溪的巴士。'],
'kaga':['From Kagaonsen Station, take a bus to the chosen hot-spring town.','加賀温泉駅から各温泉街へバスで移動。','从加贺温泉站乘巴士前往所选温泉小镇。'],
'kinosaki':['Walk into the town from JR Kinosaki Onsen Station.','JR城崎温泉駅から温泉街へ徒歩で移動。','从JR城崎温泉站步行进入温泉街。'],
'kinugawa':['Use Tobu Kinugawa Onsen Station.','東武鬼怒川温泉駅を利用。','利用东武鬼怒川温泉站。'],
'kusatsu':['Take a bus from Naganohara-Kusatsuguchi Station.','長野原草津口駅からバスでアクセス。','从长野原草津口站乘巴士前往。'],
'noboribetsu':['From JR Noboribetsu Station, take a bus to the hot-spring district.','JR登別駅から温泉街行きのバスを利用。','从JR登别站乘巴士前往温泉区。'],
'shibu':['From Yudanaka Station, continue by bus or taxi.','湯田中駅からバスまたはタクシーでアクセス。','从汤田中站换乘巴士或出租车。'],
'yufuin':['Use JR Yufuin Station or an express bus to Yufuin.','JR由布院駅、または由布院行き高速バスを利用。','利用JR由布院站或开往由布院的高速巴士。']}
CONTEXT={
'arima':['A historic hot-spring town that fits a Kobe or Osaka trip.','神戸・大阪旅行と組み合わせやすい歴史ある温泉街。','历史悠久的温泉小镇，适合与神户或大阪行程结合。'],
'atami':['Seaside views and shopping streets near the station make this an accessible break from Tokyo.','海の景色と駅周辺の商店街を楽しめる東京近郊の温泉地。','可欣赏海景和车站附近商店街的东京近郊温泉地。'],
'beppu':['Explore distinct hot-spring districts and streets filled with rising steam.','多様な温泉地区と湯けむりの風景が特徴の温泉都市。','以多个温泉区和袅袅蒸汽景观为特色的温泉城市。'],
'dogo':['Combine the historic bathhouse buildings with a stroll through Matsuyama’s shopping arcade.','歴史ある浴場建築と松山の商店街散策を組み合わせられます。','可结合历史浴场建筑与松山商店街散步。'],
'gero':['Hot-spring inns line the Hida River in this mountain town.','飛騨川沿いに温泉宿が集まる山間の温泉地。','温泉旅馆沿飞驒川分布的山间温泉地。'],
'ginzan':['A mountain village known for wooden inns and winter scenery.','木造旅館の街並みと冬景色で知られる山間の温泉街。','以木造旅馆街景和冬季雪景闻名的山间温泉小镇。'],
'hakone':['Combine mountain scenery, museums and an overnight hot-spring stay near Tokyo.','東京近郊で山の景色、美術館、温泉宿泊を組み合わせやすい地域。','适合将山景、美术馆与温泉住宿相结合的东京近郊地区。'],
'jozankei':['A valley retreat that combines nature with a hot-spring break on a Sapporo trip.','札幌旅行で渓谷の自然と温泉休憩を組み合わせやすい地域。','可在札幌行程中结合峡谷自然景观与温泉休息。'],
'kaga':['This Hokuriku destination includes several separate hot-spring towns, including Yamashiro and Yamanaka.','山代・山中など複数の温泉街を含む北陸の温泉地域。','包括山代、山中等多个温泉小镇的北陆温泉地区。'],
'kinosaki':['A traditional town known for walking between public baths in a yukata.','浴衣姿で外湯を巡りながら歩く伝統的な温泉街。','以穿浴衣步行巡游公共浴场为特色的传统温泉小镇。'],
'kinugawa':['Riverside hot-spring accommodation can be combined with a Nikko trip.','日光旅行と組み合わせられる川沿いの温泉宿泊エリア。','可与日光旅行结合的河畔温泉住宿地区。'],
'kusatsu':['Explore the Yubatake-centred town and traditional bathing culture.','湯畑を中心とした街歩きと伝統的な入浴文化を楽しめます。','可游览以汤畑为中心的温泉街并体验传统入浴文化。'],
'noboribetsu':['Volcanic scenery at Jigokudani sits alongside hot-spring hotels.','地獄谷の火山地形と温泉ホテルが集まる地域。','地狱谷火山地形与温泉酒店相结合的地区。'],
'shibu':['A mountain hot-spring town with traditional lanes and public baths.','伝統的な路地と外湯が残る山あいの温泉街。','保留传统巷道和公共浴场的山间温泉小镇。'],
'yufuin':['Enjoy Mount Yufu scenery, Lake Kinrin and a hot-spring stay together.','由布岳の景色、金鱗湖、温泉宿泊を楽しめる町。','可结合由布岳山景、金鳞湖与温泉住宿的小镇。']}
COPY={
'en':dict(access='Getting there',area='Plan a half-day or overnight stay',conditions='Bathing conditions',choose='Choose an actual facility',faq='Questions before visiting',photo='Reference photo · not a live view',credit='Photo credit / original license',map='Map and directions',sources='Original facility and tourism sources',shuttle='Some accommodation offers a shuttle. Confirm the selected property’s own access instructions.',stay='Combine a walk around the area with a half-day visit or an overnight stay. Public baths, private baths and accommodation availability differ by facility.',rows=[('Day visits','Admission for non-staying guests varies by facility.'),('Private / family baths','Only some properties offer these; confirm reservations and conditions.'),('Tattoos','Admission and covering rules differ by facility.'),('Prices and opening hours','There is no single area-wide price or opening schedule.')],steps=['Choose the district and decide between a day visit and an overnight stay.','Choose a facility on the map, then compare fees, opening hours and booking conditions on its official website.','If a private bath or tattoo acceptance is essential, use the individual facility’s policy.'],questions=[('Can I visit without staying overnight?','Not every inn accepts outside visitors. Check the day-bathing information of the specific facility.'),('Can I enter with tattoos?','Rules vary. Small covered tattoos and private-bath use may have different conditions; ask the chosen facility.')]),
'ja':dict(access='アクセス',area='半日散策・温泉宿泊の計画',conditions='入浴条件',choose='利用施設を選ぶ手順',faq='訪問前のよくある質問',photo='参考写真・現在のライブ映像ではありません',credit='写真提供・原本とライセンス',map='地図と経路',sources='施設・観光案内の原典',shuttle='宿によっては送迎があります。選んだ宿の実際のアクセス案内をご確認ください。',stay='周辺散策と半日の訪問、または1泊の温泉旅行を組み合わせましょう。共同浴場、貸切風呂、宿泊の条件は施設ごとに異なります。',rows=[('日帰り','外来入浴の受け入れは施設ごとに異なります。'),('貸切・家族風呂','一部の宿で提供。予約や利用条件の確認が必要です。'),('タトゥー','入浴・カバーの規定は施設ごとに異なります。'),('料金・営業時間','地域全体に共通する料金や営業時間はありません。')],steps=['滞在エリアを選び、日帰りか宿泊かを決めます。','地図で施設を選び、公式サイトで入浴料、営業時間、予約条件を比較します。','貸切風呂やタトゥー対応が必須なら、地域の一般情報ではなく個別施設の規定を基準にします。'],questions=[('宿泊せずに入浴できますか？','すべての宿が外来客を受け入れるわけではありません。利用する施設の日帰り入浴案内をご確認ください。'),('タトゥーがあっても利用できますか？','施設ごとに異なります。小さなタトゥーのカバーや貸切風呂の条件も、個別に確認してください。')]),
'zh-cn':dict(access='交通方式',area='规划半日游或温泉住宿',conditions='入浴条件',choose='选择实际设施的步骤',faq='出发前常见问题',photo='参考照片，并非当前实时画面',credit='照片作者、原图与许可',map='地图与路线',sources='设施与旅游信息原始来源',shuttle='部分住宿提供接送服务，请确认所选住宿的实际交通说明。',stay='可将周边散步与半日游或一晚温泉住宿结合。公共浴场、包场浴池和住宿条件因设施而异。',rows=[('当天入浴','是否接待非住客因设施而异。'),('私人浴池／家庭浴池','仅部分住宿提供，需确认预约和使用条件。'),('文身','能否入浴及遮盖规定因设施而异。'),('价格与营业时间','整个温泉地区没有统一价格或营业时间。')],steps=['先选择区域，并决定当天往返或住宿。','在地图上选择设施，再到官网比较入浴费、营业时间及预约条件。','如必须使用私人浴池或需要接纳文身，请以具体设施政策为准。'],questions=[('不住宿可以泡温泉吗？','并非所有旅馆都接待非住客，请查看所选设施的当天入浴说明。'),('有文身可以使用吗？','规定因设施而异。小文身遮盖和私人浴池的条件也需分别确认。')])}

def run():
    for slug, access in ACCESS.items():
        source=(ROOT/'onsen'/slug/'index.html').read_text()
        figure=re.search(r'<figure\b[^>]*>.*?</figure>',source,re.S)
        maps=re.findall(r'href="(https://www.google.com/maps/[^\"]+)"',source)
        official=list(dict.fromkeys(u for u in re.findall(r'href="(https://[^\"]+)"',source) if not any(s in u for s in ['japulse.com','google.com','wikimedia.org','creativecommons.org'])))
        for i,lang in enumerate(COPY):
            c=COPY[lang];file=ROOT/lang/'onsen'/slug/'index.html';html=file.read_text()
            if 'id="jp-onsen-context"' in html:continue
            title=unescape(re.sub('<[^>]+>','',re.search(r'<h1[^>]*>(.*?)</h1>',html,re.S)[1]))
            photo=''
            if figure:
                photo=figure[0]
                photo=re.sub(r'alt="[^"]*"',lambda m:'alt="'+escape(title,quote=True)+'"',photo)
                caption=re.search(r'<figcaption[^>]*>(.*?)</figcaption>',photo,re.S)
                if caption:
                    original=caption[1]
                    # Keep attribution names, licenses and source links verbatim.
                    credit=original.split('·',1)[-1].replace('촬영/제공:','').replace('사진 원본·라이선스 확인',c['credit']).replace('라이선스',c['credit'])
                    photo=photo.replace(caption[0],'<figcaption>'+c['photo']+' · '+credit+'</figcaption>')
            block='<div id="jp-onsen-context">'+photo
            block+=f'<section class="panel"><h2>{c["area"]}</h2><p>{CONTEXT[slug][i]}</p><p>{c["stay"]}</p></section>'
            block+=f'<section class="panel"><h2>{c["access"]}</h2><p>{access[i]}</p><p>{c["shuttle"]}</p>'
            if maps:block+=f'<a class="btn" href="{maps[0]}" target="_blank" rel="noopener noreferrer">{c["map"]} ↗</a>'
            block+='</section>'
            block+=f'<section class="panel"><h2>{c["conditions"]}</h2><dl>'+''.join(f'<dt><strong>{k}</strong></dt><dd>{v}</dd>' for k,v in c['rows'])+'</dl></section>'
            block+=f'<section class="panel"><h2>{c["choose"]}</h2><ol>'+''.join('<li>'+s+'</li>' for s in c['steps'])+'</ol></section>'
            block+=f'<section class="panel"><h2>{c["faq"]}</h2>'+''.join(f'<h3>{q}</h3><p>{a}</p>' for q,a in c['questions'])+'</section>'
            block+=f'<section class="panel"><h2>{c["sources"]}</h2><ul>'+''.join(f'<li><a href="{u}" target="_blank" rel="noopener noreferrer">{escape(unescape(u).split("/")[2])} ↗</a></li>' for u in official)+'</ul></section></div>'
            html=html.replace('</main>',block+'</main>')
            html=html.replace('</head>','<style>#jp-onsen-context figure{margin:20px 0}#jp-onsen-context img{width:100%;height:auto;border-radius:12px}#jp-onsen-context figcaption{font-size:13px;overflow-wrap:anywhere}#jp-onsen-context dd{margin:0 0 14px}#jp-onsen-context a{overflow-wrap:anywhere}</style></head>')
            file.write_text(html)
    print('Added translated Korean access, reference images, attribution, planning, bathing conditions and FAQs to 45 onsen guides. Facility-specific fare tables remain separately auditable.')

if __name__=='__main__':run()
