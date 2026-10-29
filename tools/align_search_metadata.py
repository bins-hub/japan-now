"""Keep localized search intent and page metadata aligned after content generation.

Only metadata and page-describing JSON-LD are updated. No new URLs or body claims.
"""
from html import escape, unescape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LANGS = ['en', 'ja', 'zh-cn']
LANG_CODES = {'ko': 'ko', 'en': 'en', 'ja': 'ja', 'zh-cn': 'zh-CN'}
NAMES = json.loads((ROOT/'content/search-page-names.json').read_text())
ONSEN = {
 'hakone':['Day-use baths, fees & access','日帰り温泉・料金・アクセス','日归温泉、费用与交通'],
 'kusatsu':['Day-use baths, fees & Yubatake access','日帰り入浴・料金・湯畑へのアクセス','日归泡汤、费用与汤畑交通'],
 'beppu':['Day-use baths, fees, hours & access','日帰り温泉・料金・営業時間・アクセス','日归温泉、费用、营业时间与交通'],
 'yufuin':['Day-use baths, private-bath conditions & fees','日帰り温泉・貸切風呂の条件・料金','日归温泉、私人浴池条件与费用'],
 'noboribetsu':['Day-use fees & Jigokudani travel','日帰り入浴料・地獄谷への旅行','日归泡汤费用与地狱谷旅行'],
 'jozankei':['Day-use fees & access from Sapporo','日帰り入浴料・札幌からのアクセス','日归泡汤费用与札幌交通'],
 'kinosaki':['Public bath passes, fees & closing days','外湯めぐり・料金・休館日','外汤巡游、费用与休馆日'],
 'arima':['Kin no Yu & Gin no Yu fees and opening information','金の湯・銀の湯の料金と営業情報','金之汤、银之汤费用与营业信息'],
 'gero':['Day-use bathing fees & opening hours','日帰り入浴料・営業時間','日归泡汤费用与营业时间'],
 'ginzan':['Day-use fees, winter travel & access','日帰り入浴料・冬の旅行・アクセス','日归泡汤费用、冬季旅行与交通'],
 'dogo':['Admission, opening hours & reservations','入浴料・営業時間・予約方法','门票、营业时间与预约方式'],
 'atami':['Day-use baths, Fuua fees & access from Tokyo','日帰り温泉・Fuuaの料金・東京からのアクセス','日归温泉、Fuua费用与东京交通'],
 'kaga':['Yamashiro Soyu bathing fees & access','山代温泉総湯の入浴料・アクセス','山代温泉总汤费用与交通'],
 'shibu':['Oyu day-use fees & public bath rules','大湯の日帰り入浴料・外湯の利用条件','大汤日归泡汤费用与外汤规则'],
 'kinugawa':['Free footbaths, Nikko access & travel','無料足湯・日光へのアクセス・旅行','免费足汤、日光交通与旅行'],
}
REGIONS = {
 'tokyo':[['Tokyo live cameras: Shibuya, Shinjuku & Asakusa','Browse public camera guides for Shibuya Crossing, Kabukicho and Sensoji. Check original broadcasts and local travel tips; current live status depends on the provider.'],['東京ライブカメラ｜渋谷・新宿・浅草','渋谷スクランブル交差点、新宿歌舞伎町、浅草寺の公開カメラと旅行情報をまとめて確認。現在の配信状況は各配信元でご確認ください。'],['东京实时摄像头｜涩谷、新宿与浅草','汇集涩谷十字路口、新宿歌舞伎町和浅草寺的公开摄像头来源与旅行指南。是否正在直播请以原发布方为准。']],
 'osaka':[['Osaka live cameras: Dotonbori & city skyline','Compare public camera views of Dotonbori and the Osaka skyline, with original video sources and travel tips. Confirm current broadcast status with each provider.'],['大阪ライブカメラ｜道頓堀・街の夜景','道頓堀と大阪の街並みを公開カメラで比較。配信元と旅行情報を案内し、現在の配信状況は提供元で確認できます。'],['大阪实时摄像头｜道顿堀与城市夜景','比较道顿堀与大阪城市天际线的公开摄像头，查看原视频来源及旅行提示。当前直播状态以提供方为准。']],
 'kyoto':[['Kyoto live cameras: Arashiyama & bamboo grove','Find the Arashiyama public camera guide, bamboo grove travel tips and original video source. Confirm current broadcast status before planning a visit.'],['京都ライブカメラ｜嵐山・竹林','嵐山・竹林の公開カメラ案内と旅行のヒント、映像の配信元を確認。訪問前に現在の配信状況を提供元でご確認ください。'],['京都实时摄像头｜岚山与竹林','查找岚山竹林公开摄像头指南、旅行提示与原视频来源。到访前请向提供方确认当前直播状态。']],
 'fuji':[['Mt Fuji live cameras: Lake Kawaguchiko & visibility','Check the Lake Kawaguchiko camera guide for views of Mount Fuji, weather and visibility tips. Clouds can obscure the mountain; verify current broadcast status at the source.'],['富士山ライブカメラ｜河口湖・天気と見え方','河口湖から富士山を望むカメラ案内と天気・視界の確認方法。雲で見えない場合もあり、配信状況は提供元でご確認ください。'],['富士山实时摄像头｜河口湖、天气与能见度','查看河口湖富士山摄像头指南及天气、能见度提示。山体可能被云遮挡，当前直播状态请以原来源为准。']],
 'hokkaido':[['Sapporo live cameras: Odori Park, Hokkaido','Find the public camera guide for Sapporo Odori Park near the TV Tower, seasonal scenery and travel tips. Check current broadcasts and winter conditions before visiting.'],['札幌ライブカメラ｜北海道・大通公園','札幌テレビ塔・大通公園周辺の公開カメラ案内、季節の風景と旅行情報。訪問前に配信状況と冬の現地情報をご確認ください。'],['札幌实时摄像头｜北海道大通公园','查看札幌电视塔、大通公园周边的公开摄像头指南、季节景观与旅行提示。出发前请确认直播状态及冬季情况。']],
 'kyushu':[['Fukuoka & Okinawa live cameras: Hakata, Bise & Iki','Browse public camera guides for Hakata Station, Bise Coast and Kojima Shrine on Iki Island. These are separate destinations; verify current broadcasts and transport plans.'],['福岡・沖縄ライブカメラ｜博多駅・備瀬・壱岐','博多駅、沖縄備瀬、壱岐の小島神社の公開カメラと旅行情報。別々の目的地のため、配信状況と交通を個別に確認してください。'],['福冈与冲绳实时摄像头｜博多、备濑与壹岐','汇集博多站、冲绳备濑海岸和壹岐小岛神社的公开摄像头指南。各地为不同目的地，请分别确认直播状态与交通。']],
}
MAIN = {
 'run-eat/':[
 ['Japan running routes: Tokyo, Osaka, Kyoto & Fukuoka','Explore running routes at Tokyo Imperial Palace, Osaka Castle Park, Kyoto Kamo River and Fukuoka Ohori Park, with route previews and nearby travel and food information.'],
 ['日本のランニングコース｜皇居・大阪城・鴨川・大濠公園','東京の皇居、大阪城公園、京都の鴨川、福岡の大濠公園などのランニングコースを紹介。コースの見方と周辺の旅行・食事情報を確認できます。'],
 ['日本跑步路线｜东京皇居、大阪城、京都鸭川与福冈','查找东京皇居、大阪城公园、京都鸭川、福冈大濠公园等跑步路线，查看路线预览与周边旅行、美食信息。']],
 'local-food/':[
 ['Japan local food guide: Tokyo, Osaka, Kyoto & Fukuoka','Explore neighborhood restaurants in Tokyo, Osaka, Kyoto and Fukuoka using Japanese reviews and local reporting. Follow original sources to check menus, opening information and reviews.'],
 ['日本の地元グルメ｜東京・大阪・京都・福岡','日本語の口コミや地域メディアを参考に、東京・大阪・京都・福岡の街の飲食店を紹介。原文リンクでメニュー、営業情報、口コミを確認できます。'],
 ['日本当地美食指南｜东京、大阪、京都与福冈','参考日文评价与当地媒体介绍东京、大阪、京都、福冈的街区餐馆，通过原文来源确认菜单、营业信息及评价。']],
 'onsen/':[
 ['Japan hot springs: 15 areas, day-use baths & access','Compare 15 hot-spring areas including Hakone, Beppu, Yufuin, Kusatsu and Noboribetsu. Explore access, day-use facilities, fees and bathing conditions, then verify details with each facility.'],
 ['日本の温泉15地域｜日帰り入浴・料金・アクセス','箱根・別府・由布院・草津・登別など15地域の交通と温泉利用情報を比較。日帰り施設、料金、利用条件は各施設の公式案内でご確認ください。'],
 ['日本温泉15地区｜日归泡汤、费用与交通','比较箱根、别府、由布院、草津、登别等15个温泉地区的交通与使用信息，查找日归设施、费用及入浴条件，具体请以设施官网为准。']],
 'season/':[
 ['Japan seasonal travel: cherry blossoms, foliage & winter','Explore cherry blossom, autumn foliage and winter guides for Tokyo, Kyoto, Osaka and Sapporo. Compare places and day routes, then check weather and current local conditions.'],
 ['日本の季節旅行｜東京・京都・大阪・札幌の桜・紅葉・冬','東京・京都・大阪・札幌の桜、紅葉、冬の旅行ガイドを地域別に紹介。名所とモデルコースを比較し、天気と現地の最新状況をご確認ください。'],
 ['日本四季旅行｜东京、京都、大阪、札幌樱花红叶与冬季','按地区查看东京、京都、大阪、札幌的樱花、红叶与冬季旅行指南，比较景点和一日路线，出发前确认天气与当地最新情况。']],
 'move/':[
 ['Japan airport transfers: city routes, last trains & fares','Plan routes from Narita, Haneda, Kansai and New Chitose airports to the city. Check trains, fare sources, last services, terminal access and directions to your hotel with official operators.'],
 ['日本の空港から市内へ｜交通・運賃・終電・乗り換え','成田・羽田・関西・新千歳空港から市内への行き方、運賃の確認方法、終電、ターミナル移動、ホテルへの経路を案内。時刻と運賃は公式情報をご確認ください。'],
 ['日本机场到市区｜交通、票价、末班车与换乘','介绍成田、羽田、关西、新千岁机场到市区的交通、票价确认方式、末班车、航站楼移动及酒店路线。时刻与票价请以运营商官方信息为准。']],
}


def nodes(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from nodes(child)


def metadata(source):
    head = source.split('</head>', 1)[0]
    return unescape(re.search(r'<title>(.*?)</title>', head, re.S)[1]), unescape(re.search(r'<meta name="description" content="([^"]+)"', head)[1])


def apply(source, title, description, url, language, kind):
    source = re.sub(r'<title>.*?</title>', lambda m:'<title>'+escape(title)+'</title>', source, count=1, flags=re.S)
    # Preserve all non-metadata attributes and all page-body markup.
    for attr, key, value in [('name','description',description),('property','og:title',title),('property','og:description',description),('name','twitter:title',title),('name','twitter:description',description)]:
        pattern = r'(<meta\b(?=[^>]*\b'+attr+r'="'+re.escape(key)+r'")[^>]*\bcontent=")[^"]*(")'
        source = re.sub(pattern, lambda m:m[1]+escape(value, quote=True)+m[2], source)
        if key in ('og:title','og:description') and not re.search(pattern,source):
            source=source.replace('</head>','<meta property="'+key+'" content="'+escape(value,quote=True)+'"></head>',1)
    for key,value in [('og:url',url),('og:type','article' if kind=='Article' else 'website')]:
        if not re.search(r'<meta\b[^>]*property="'+key+'"',source):
            source=source.replace('</head>','<meta property="'+key+'" content="'+escape(value,quote=True)+'"></head>',1)
    found = False
    def schema(match):
        nonlocal found
        data = json.loads(match[2])
        for item in nodes(data):
            if item.get('@type') in ('WebPage','CollectionPage','Article') and item.get('url',url) == url:
                found = True
                item.update({'@type':kind,'name':title,'description':description,'url':url,'inLanguage':language})
                if kind == 'Article':item['headline']=title
        return match[1]+json.dumps(data,ensure_ascii=False,separators=(',',':'))+match[3]
    source = re.sub(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)',schema,source,flags=re.S)
    if not found:
        data={'@context':'https://schema.org','@type':kind,'name':title,'description':description,'url':url,'inLanguage':language}
        source=source.replace('</head>','<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False,separators=(',',':'))+'</script></head>',1)
    return source


def run():
    urls=re.findall(r'<loc>(.*?)</loc>',(ROOT/'sitemap.xml').read_text())
    inventory=[]; changed=[]
    for url in urls:
        route=url.removeprefix('https://japulse.com/')
        lang=next((x for x in LANGS if route.startswith(x+'/')),'ko')
        base=route[len(lang)+1:] if lang!='ko' else route
        path=ROOT/route/'index.html';source=path.read_text();title,description=metadata(source)
        ko=(ROOT/base/'index.html').read_text();ko_title,_=metadata(ko)
        kind='Article' if base.startswith('guides/') else 'CollectionPage' if base in ('','live/','now/','run-eat/','local-food/','season/','onsen/','move/') or base.startswith('regions/') else 'WebPage'
        if lang!='ko':
            i=LANGS.index(lang)
            if base in MAIN:title,description=MAIN[base][i];title+=' | JAPULSE'
            elif base.startswith('regions/'):
                slug=base.split('/')[1];title,description=REGIONS[slug][i];title+=' | JAPULSE'
            elif base.startswith('onsen/'):
                slug=base.split('/')[1];name=NAMES[route]['name'];aspect=ONSEN[slug][i]
                title=name+((' onsen: ' if 'Onsen' not in name else ': ') if lang=='en' else '｜')+aspect+' | JAPULSE'
                description=[f'{name}: {aspect}. Compare facility information and access; confirm current fees, opening hours and bathing rules with the official facility.',f'{name}の{aspect}を確認。施設別の利用情報と交通を比較し、最新の料金・営業時間・入浴条件は施設の公式案内でご確認ください。',f'查看{name}的{aspect}，比较设施使用信息与交通；最新费用、营业时间与入浴条件请以设施官方信息为准。'][i]
            elif base.startswith('move/'):
                stem=NAMES[route]['name'].removesuffix(' アクセス方法')
                title=[f'{stem}: time, fares & transfers | JAPULSE',f'{stem}の行き方｜所要時間・運賃・乗り換え | JAPULSE',f'{stem}怎么去｜时间、票价与换乘 | JAPULSE'][i]
                # Existing descriptions retain any named operator and route caveats.
                description=NAMES[route]['description']+[' Compare travel time, fares and transfers using official operator links and map directions.',' 所要時間・運賃・乗り換えを比較し、公式案内と地図で当日の移動をご確認ください。',' 比较所需时间、票价与换乘，通过官方来源与地图确认当天行程。'][i]
        if base=='season/winter/sapporo/' and lang=='ko':title=title.replace('겨울 여행 여행','겨울 여행')
        after=apply(source,title,description,url,LANG_CODES[lang],kind)
        if after!=source:path.write_text(after);changed.append(route)
        inventory.append({'source':base,'language':lang,'url':url,'source_title':ko_title,'title':title,'description':description,'page_type':kind})
    (ROOT/'content/search-intent-metadata.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
    print(f'{len(inventory)} indexed pages inventoried; {len(changed)} pages updated')


if __name__=='__main__':run()
