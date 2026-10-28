"""Restore missing practical guidance using the Korean section markup.

Run only for these five sections; leave existing interactive features untouched.
Translations follow the source, including its review date (not a new fact check).
"""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent.parent
SECTIONS = {
    'live': 'jp-live-practical-guide', 'now': 'jp-now-practical-guide',
    'run-eat': 'jp-run-visit-guide', 'local-food': 'jp-eat-visit-guide',
    'season': 'jp-season-visit-guide',
}

# These two sections have no section id in the Korean source. Locate them by
# their existing heading id/text, without changing the source page.
EXTRA = {
 'run-eat': ('jp-run-source-guide', '일본 러닝 코스를 안전하게 이용하는 순서'),
 'local-food': ('jp-eat-method-guide', '러닝 뒤 동네 식당을 찾는 법'),
}
EXTRA_COPY = {
 'en': {
  'run-eat': [
   'How to use Japan’s running routes safely',
   'JAPULSE route lengths and itineraries are planning references, not GPS survey records or personal site inspections. Find the starting point on the map, check route rules, events, construction and weather, then decide when to run.',
   'Find the starting point and return location on the route map.',
   'If you need current video, check the original broadcast’s LIVE indicator and time.',
   'Search separately for restaurants in the area around your chosen course, checking travel time and opening hours.',
   'See actual restaurants by area ↗', 'Camera travel guide ↗',
   'The 360° button opens a separate Google Street View page. This site does not automatically call the paid Google Maps image API.'
  ],
  'local-food': [
   'How to find neighborhood food after a run',
   'Start with practical access from your location rather than tourist popularity rankings.',
   '① Choose the location first',
   'After an Imperial Palace run, check the journey to Jinbocho; after Osaka Castle Park, check the route to Morinomiya in Google Maps. Places in the same city are not necessarily a short walk apart.',
   'Check running routes by area ↗',
   '② Check hours and menus',
   'Choose a meal type such as a breakfast set, udon or ramen, while remembering that menus and prices can change. Check the restaurant’s official channels and current map listings for closures, operations and reservations.',
   'Check on Google Maps ↗',
   '③ Understand the evidence and filming locations',
   'This page is not based on personal visits or surveys of local residents. Candidates come from linked local articles and reviews in Japan; current popularity or operation is not guaranteed.',
   'About JAPULSE ↗',
   'City comparison at a glance',
   'Tokyo', ' — The Imperial Palace running course and Jinbocho’s curry and Western-style restaurants are different locations. Check the journey first. ', 'Tokyo restaurants →',
   'Osaka', ' — From Osaka Castle Park, head toward Morinomiya to compare set meals and udon options. ', 'Osaka restaurants →',
   'Kyoto', ' — Combine the Kamo River area with noodle dishes and traditional snacks around Demachiyanagi. ', 'Kyoto restaurants →',
   'Fukuoka', ' — Check the distance from Ohori Park to Ropponmatsu and confirm lunch hours. ', 'Fukuoka restaurants →',
   'Selection and sources reviewed: 20 October 2026. Prices, closing days and operations may have changed. Restaurant photos and reviews remain the property of their original providers.'
  ]
 },
 'ja': {
  'run-eat': [
   '日本のランニングコースを安全に利用する手順',
   'JAPULSEの距離と経路は訪問計画の参考情報であり、GPSによる実測記録や個人の現地調査ではありません。地図で出発位置を確認し、利用ルール・イベント・工事・気象情報を調べてから走る時間を決めてください。',
   'コース地図で出発点と戻る場所を確認します。',
   '現在の映像が必要な場合は、元の配信のLIVE表示と時刻を確認します。',
   '食事は選んだコース周辺の地域で別途検索し、移動時間と営業時間を確認します。',
   '地域別の実在する飲食店を見る ↗', '現地カメラの活用ガイド ↗',
   '360°ボタンは別のGoogleストリートビューへ移動します。このサイトは有料のGoogle Maps画像APIを自動呼び出ししません。'
  ],
  'local-food': [
   'ランニング後に近隣の飲食店を探す方法',
   '観光地の人気順ではなく、その場所から実際に移動できるかを先に確認してください。',
   '① まず場所を決める',
   '皇居で走った場合は神保町へ、大阪城公園の場合は森ノ宮へ移動する必要があるかGoogleマップで確認します。同じ都市でもすぐに歩いて行けるとは限りません。',
   '地域別のランニング経路を確認 ↗',
   '② 営業時間とメニューを確認',
   '朝定食・うどん・ラーメンなど食事の種類を選びますが、メニューや価格は変わる場合があります。店舗の公式案内と最新の地図登録情報で休業・営業・予約の有無を確認してください。',
   'Googleマップで確認 ↗',
   '③ 根拠と撮影場所を区別する',
   'このページは実際の訪問記や地元住民へのアンケートではありません。出典付きの地域記事や日本国内のレビューから候補をまとめており、現在の人気や営業を保証するものではありません。',
   'JAPULSEについて ↗',
   '都市別の比較',
   '東京', ' — 皇居のランニングコースと神保町のカレー・洋食店は同じ地点ではないため、まず移動経路を確認します。', '東京の飲食店を見る →',
   '大阪', ' — 大阪城公園から森ノ宮方面へ移動し、定食・うどんの候補を比較できます。', '大阪の飲食店を見る →',
   '京都', ' — 鴨川沿いと出町柳周辺の麺料理・伝統的なおやつの候補を組み合わせます。', '京都の飲食店を見る →',
   '福岡', ' — 大濠公園と六本松の距離を確認し、ランチの営業時間を調べます。', '福岡の飲食店を見る →',
   '選定・出典確認：2026年10月20日。その後、価格・定休日・営業情報が変わった可能性があります。写真・レビューの権利は各提供元に帰属します。'
  ]
 },
 'zh-cn': {
  'run-eat': [
   '安全使用日本跑步路线的步骤',
   'JAPULSE的路线长度与行程仅供规划参考，并非GPS实测记录或个人实地考察结果。请先在地图上确认起点，并查看路线规则、活动、施工和天气信息，再决定跑步时间。',
   '在路线地图上确认起点及返回位置。',
   '如果需要当前视频，请确认原始直播的LIVE标识和时间。',
   '在所选路线周边另行搜索餐厅，并检查交通时间和营业时间。',
   '查看各地区真实餐厅列表 ↗', '当地摄像头使用指南 ↗',
   '360°按钮会打开单独的Google街景页面；本站不会自动调用收费的Google Maps图片API。'
  ],
  'local-food': [
   '跑步后如何寻找附近餐厅',
   '请先确认从实际位置能否方便到达，而不是只看旅游热门排名。',
   '① 先确定地点',
   '在东京皇居跑步后，请用Google地图确认前往神保町的路线；在大阪城公园跑步后，确认前往森之宫的路线。同城地点并不一定都能直接步行到达。',
   '查看各地区跑步路线 ↗',
   '② 确认营业时间和菜单',
   '可以先选早餐套餐、乌冬面或拉面等餐食类型，但菜单和价格可能变化。请通过餐厅官方渠道与最新地图信息确认休息日、营业及预约情况。',
   '在Google地图确认 ↗',
   '③ 区分资料依据与拍摄地点',
   '本页并非亲自到访的食记或针对当地居民的调查结果。候选餐厅依据附有来源链接的地方文章和日本国内评论整理，不保证目前的人气或营业状态。',
   '关于JAPULSE ↗',
   '城市对比一览',
   '东京', ' — 皇居跑步路线与神保町的咖喱、西餐店不在同一地点，请先确认交通路线。', '查看东京餐厅 →',
   '大阪', ' — 从大阪城公园往森之宫方向移动，可以比较套餐和乌冬面餐厅。', '查看大阪餐厅 →',
   '京都', ' — 可将鸭川河畔与出町柳地区的面食、传统小吃结合安排。', '查看京都餐厅 →',
   '福冈', ' — 请确认大濠公园到六本松的距离，并检查午餐营业时间。', '查看福冈餐厅 →',
   '选定与来源核对：2026年10月20日。此后价格、休息日及营业信息可能变化。餐厅照片和评论的权利归原始提供方所有。'
  ]
 }
}

def extra_source(page):
    source = (ROOT / page / 'index.html').read_text()
    ident, title = EXTRA[page]
    at = source.index(title, source.index('<main'))
    start = source.rfind('<section', 0, at)
    return source[start:source.index('</section>', at) + len('</section>')]

def render_extra(page, lang):
    section = extra_source(page)
    originals = [x for x in re.findall(r'>([^<>]+)<', section) if re.search('[가-힣]', x)]
    translations = EXTRA_COPY[lang][page]
    assert len(originals) == len(translations), (page, len(originals), len(translations))
    mapping = dict(zip(originals, translations))
    section = re.sub(r'>([^<>]+)<', lambda m: '>' + html.escape(mapping.get(m[1], html.unescape(m[1])), quote=False) + '<', section)
    section = section.replace('<section ', '<section id="' + EXTRA[page][0] + '" ', 1)
    section = section.replace('href="https://japulse.com/', 'href="https://japulse.com/' + lang + '/')
    assert not re.search('[가-힣]', section)
    return section
COPY = {
 'en': {
  'live': [
   'How to use Japan’s live cameras',
   'Local cameras can help you assess visible crowds and weather conditions when planning a trip to Japan. Camera direction, refresh intervals and broadcast delays vary; do not use video alone to determine current temperatures or road closures.',
   'Before departure:', ' Check that the view is current and compare it with a separate weather forecast.',
   'Before traveling to the site:', ' Check that the place shown and your intended destination are in the same location.',
   'Seasonal trips:', ' Foliage and snow can look different depending on camera angle. Also check official local tourism information.',
   'Local weather and travel checks →', 'Seasonal travel information →', 'Airport and sightseeing transport →',
   'Guidance reviewed: 2026-10-28. Check the video provider’s actual update time and usage restrictions first.'
  ],
  'now': [
   'Japan travel weather: checks beyond temperature',
   'Conditions can feel very different across Japan depending on region and elevation. Check hourly forecasts, rain and wind rather than deciding what to wear or where to go from the current temperature alone.',
   'City trips such as Tokyo and Osaka:', ' Check morning and evening temperatures and rain forecasts separately.',
   'Hokkaido and mountain areas:', ' Check temperature differences between lowland and mountain destinations, plus snow, road and transport notices.',
   'Running and walking:', ' Check rain, wind, sunset time and the distance you expect to cover.',
   'Live video:', ' Use the view for local context; it does not replace official weather warnings.',
   'Local live cameras →', 'Foliage and seasonal trips →', 'Transport and transfer guides →',
   'Guidance reviewed: 2026-10-28. Check observation and forecast times with each weather source.'
  ],
  'run-eat': [
   'Before running in Japan',
   'A route’s mapped starting point may differ from the actual entrance. Check the start location and your return route before leaving.',
   'Check sunset, temperature, rain and wind. In summer consider heat illness and water stops; in winter consider icy surfaces.',
   'Official local notices take priority for park and path restrictions, facility opening hours and event closures.',
   'LIVE local view →', 'NOW weather →', 'MOVE transport →',
   'Guidance reviewed: 2026-10-28 · Recheck official operating information for your visit date.'
  ],
  'local-food': [
   'Before visiting restaurants in Japan',
   'Opening hours, closing days, last orders and queue arrangements can change. Check the restaurant’s official notices on the day of your visit.',
   'Acceptance of cash, cards and transit IC cards, child policies and reservation rules vary by restaurant.',
   'Check the station exit and walking distance to the restaurant, plus your group’s allergies and dietary restrictions in advance.',
   'MOVE directions →', 'NOW weather →', 'LIVE local atmosphere →',
   'Guidance reviewed: 2026-10-28 · Recheck official operating information for your visit date.'
  ],
  'season': [
   'Foliage, blossoms and snow: forecasts versus observations',
   'Peak foliage, full bloom and snow conditions change each year. Long-range predicted dates may differ from on-site observations.',
   'Seasonal timing can differ between city centers and mountain areas. Compare official local tourism notices with current photos just before departure.',
   'Check transport delays and attraction operating changes caused by rain, strong wind or snow, and prepare an alternative plan.',
   'LIVE local cameras →', 'NOW local weather →', 'MOVE transport options →',
   'Guidance reviewed: 2026-10-28 · Recheck official operating information for your visit date.'
  ],
 },
 'ja': {
  'live': [
   '日本のライブカメラの活用方法',
   '日本旅行の計画では、現地カメラに映る街の混雑や天気の様子を参考にできます。ただし、カメラの向き・更新間隔・配信の遅延はそれぞれ異なるため、映像だけで現在の気温や道路規制を判断しないでください。',
   '出発前：', ' 映像が最新かを確認し、別途天気予報と比較してください。',
   '現地へ移動する前：', ' 映像の場所と実際の訪問先が同じ位置か確認してください。',
   '季節の旅行：', ' 紅葉や雪景色は撮影角度によって見え方が異なるため、公式の地域観光情報も確認してください。',
   '現地の天気・旅行前の確認 →', '季節別の旅行情報 →', '空港・観光地への移動 →',
   '案内確認日：2026-10-28。映像提供者の実際の更新時刻と利用制限を優先して確認してください。'
  ],
  'now': [
   '日本旅行の天気、気温以外の確認ポイント',
   '日本では地域や標高によって体感する天気が大きく異なります。現在の気温だけで服装や当日の移動を決めず、時間帯別の予報と雨・風も確認してください。',
   '東京・大阪などの都市旅行：', ' 朝と夜の気温、雨の予報を分けて確認してください。',
   '北海道・山間部：', ' 平地と山の観光地の気温差、雪・道路・交通の案内を個別に確認してください。',
   'ランニング・徒歩旅行：', ' 雨、風、日没時刻、予定の移動距離も確認してください。',
   'ライブ映像：', ' 現地の様子を知る参考として利用し、気象警報の代わりにしないでください。',
   '日本の現地ライブカメラ →', '紅葉・季節の旅行 →', '交通・乗り換え案内 →',
   '案内確認日：2026-10-28。気象情報の観測・予報時刻は各情報源で確認してください。'
  ],
  'run-eat': [
   '日本で走る前の確認事項',
   '地図上のスタート地点と実際の入口が異なる場合があります。出発前にスタート地点と帰りの経路を確認してください。',
   '日没・気温・雨・風を確認し、夏は熱中症のリスクと給水場所、冬は路面の凍結を考慮してください。',
   '公園・遊歩道の通行制限、施設の開放時間、イベントによる規制は地域の公式案内を優先してください。',
   'LIVE 現地の映像 →', 'NOW 天気 →', 'MOVE 交通手段 →',
   '案内確認日：2026-10-28 · 訪問日の公式営業情報を再確認してください。'
  ],
  'local-food': [
   '日本の飲食店を訪れる前のチェックリスト',
   '営業時間・定休日・ラストオーダー・順番待ちの方法は変わる場合があります。訪問当日に店舗の公式案内を確認してください。',
   '現金・カード・交通系ICの利用可否、子どもの同伴や予約のルールは店舗ごとに異なります。',
   '駅の出口と店舗までの徒歩距離、同行者のアレルギーや食事制限を事前に確認してください。',
   'MOVE 道順 →', 'NOW 天気 →', 'LIVE 現地の様子 →',
   '案内確認日：2026-10-28 · 訪問日の公式営業情報を再確認してください。'
  ],
  'season': [
   '紅葉・桜・雪景色、予報と観測の違い',
   '紅葉の見頃・桜の満開・雪の状態は毎年変わり、長期予想の日付と現地の観測日は異なる場合があります。',
   '季節の名所では、市街地と山間部で時期が異なる場合があります。出発直前に公式の地域観光案内と最新の写真を比較してください。',
   '雨・強風・積雪による交通の遅延や観光施設の営業変更を確認し、代替プランも用意してください。',
   'LIVE 現地カメラ →', 'NOW 地域の天気 →', 'MOVE 移動方法 →',
   '案内確認日：2026-10-28 · 訪問日の公式営業情報を再確認してください。'
  ],
 },
 'zh-cn': {
  'live': [
   '如何使用日本实时摄像头',
   '规划日本旅行时，可以通过当地摄像头参考画面中可见的街道人流和天气情况。但不同摄像头的拍摄方向、更新间隔和直播延迟各不相同，请勿仅凭视频判断当前气温或道路管制情况。',
   '出发前：', ' 确认画面是否为最新，并与单独的天气预报进行比较。',
   '前往现场前：', ' 确认画面中的地点与实际目的地是否位于同一位置。',
   '季节旅行：', ' 红叶和雪景会因拍摄角度而呈现不同效果，请同时查看官方当地旅游信息。',
   '当地天气与出行检查 →', '季节旅行信息 →', '机场与景点交通 →',
   '指南核对日期：2026-10-28。请优先确认视频提供方的实际更新时间及使用限制。'
  ],
  'now': [
   '日本旅行天气：气温之外的检查要点',
   '日本不同地区和海拔的体感天气可能差异很大。不要仅凭当前气温决定穿着或当天行程，还应查看分时预报、降雨和风况。',
   '东京、大阪等城市旅行：', ' 分别查看早晚气温与降雨预报。',
   '北海道及山区：', ' 单独确认平地与山区景点的温差，以及积雪、道路和交通通知。',
   '跑步与徒步：', ' 查看降雨、风况、日落时间和预计行程距离。',
   '实时视频：', ' 将画面用作了解当地情况的参考，不要用来替代气象预警。',
   '日本当地实时摄像头 →', '红叶与季节旅行 →', '交通与换乘指南 →',
   '指南核对日期：2026-10-28。请在各气象来源确认观测和预报时间。'
  ],
  'run-eat': [
   '在日本跑步前的检查事项',
   '地图上标注的起点可能与实际入口不同。出发前请确认起点位置和返回路线。',
   '查看日落、气温、降雨和风况。夏季需考虑中暑风险及补水地点，冬季需注意路面结冰。',
   '公园与步道的通行限制、设施开放时间和活动管制，以当地官方通知为准。',
   'LIVE 当地画面 →', 'NOW 天气 →', 'MOVE 交通方式 →',
   '指南核对日期：2026-10-28 · 请按到访日期重新确认官方运营信息。'
  ],
  'local-food': [
   '到访日本餐厅前的检查清单',
   '营业时间、休息日、最后点单时间和现场排队方式可能发生变化。请在到访当天查看餐厅官方通知。',
   '是否接受现金、银行卡和交通IC卡，以及儿童同行与预约政策，因餐厅而异。',
   '请提前确认车站出口、到餐厅的步行距离，以及同行者的过敏和饮食限制。',
   'MOVE 路线导航 →', 'NOW 天气 →', 'LIVE 当地情况 →',
   '指南核对日期：2026-10-28 · 请按到访日期重新确认官方运营信息。'
  ],
  'season': [
   '红叶、樱花与雪景：预报与观测的区别',
   '红叶最佳观赏期、樱花盛开期和积雪情况每年都会变化，长期预测日期可能与现场观测日期不同。',
   '市中心与山区景点的季节进程可能不同。出发前请对照官方当地旅游通知与最新照片。',
   '请确认降雨、强风和积雪造成的交通延误及景点运营变更，并准备替代行程。',
   'LIVE 当地摄像头 →', 'NOW 当地天气 →', 'MOVE 出行方式 →',
   '指南核对日期：2026-10-28 · 请按到访日期重新确认官方运营信息。'
  ],
 },
}

def render(page, lang):
    ident = SECTIONS[page]
    source = (ROOT / page / 'index.html').read_text()
    section = re.search(r'<section\b[^>]*id="' + ident + r'".*?</section>', source, re.S).group()
    originals = [x for x in re.findall(r'>([^<>]+)<', section) if re.search('[가-힣]', x)]
    translations = COPY[lang][page]
    assert len(originals) == len(translations), (page, lang, len(originals), len(translations))
    mapping = dict(zip(originals, translations))
    section = re.sub(r'>([^<>]+)<', lambda m: '>' + html.escape(mapping.get(m[1], html.unescape(m[1])), quote=False) + '<', section)
    # Two Korean sections repeat the title as an accessible label.
    section = re.sub(r'aria-label="[^"]*[가-힣][^"]*"', 'aria-label="' + html.escape(translations[0], quote=True) + '"', section)
    section = re.sub(r'href="/(live|now|move|season)/"', lambda m: 'href="/' + lang + '/' + m[1] + '/"', section)
    assert not re.search('[가-힣]', section)
    return section

if __name__ == '__main__':
    for lang in COPY:
        for page, ident in SECTIONS.items():
            path = ROOT / lang / page / 'index.html'
            content = path.read_text()
            section = render(page, lang)
            if f'id="{ident}"' in content:
                content = re.sub(r'<section\b[^>]*id="' + ident + r'".*?</section>', lambda m: section, content, flags=re.S)
            else:
                assert content.count('</main>') == 1
                content = content.replace('</main>', section + '</main>')
            path.write_text(content)
    for lang in COPY:
        for page, (ident, title) in EXTRA.items():
            path = ROOT / lang / page / 'index.html'
            content = path.read_text()
            section = render_extra(page, lang)
            if f'id="{ident}"' in content:
                content = re.sub(r'<section\b[^>]*id="' + ident + r'".*?</section>', lambda m: section, content, flags=re.S)
            else:
                content = content.replace('</main>', section + '</main>')
            path.write_text(content)
    print('Restored 7 practical guidance sections in 3 languages (15 pages).')
