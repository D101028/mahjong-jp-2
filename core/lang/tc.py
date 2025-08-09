# -*- coding: utf-8 -*-
#python 3.7.2 3.7.3
# title="麻將詞彙"

yonin_ton_ikkyoku = "四人東一局"
yonin_ton = "四人東"
yonin_nan = "四人南"
sannin_ton_ikkyoku = "三人東一局"
sannin_ton = "三人東"
sannin_nan = "三人南"

# round_ton_ikkyoku = "東一局"
# round_ton_nikyoku = "東二局"
# round_ton_sankyoku = "東三局"
# round_ton_yonkyoku = "東四局"
# round_nan_ikkyoku = "南一局"
# round_nan_nikyoku = "南二局"
# round_nan_sankyoku = "南三局"
# round_nan_yonkyoku = "南四局"
# round_shaa_ikkyoku = "西一局"
# round_shaa_nikyoku = "西二局"
# round_shaa_sankyoku = "西三局"
# round_shaa_yonkyoku = "西四局"
# round_pei_ikkyoku = "北一局"
# round_pei_nikyoku = "北二局"
# round_pei_sankyoku = "北三局"
# round_pei_yonkyoku = "北四局"

# action_tsumo = "行為：自摸"
# action_ron = "行為：榮和"
# action_chii = "行為：吃"
# action_pon = "行為：碰"
# action_minkan = "行為：明槓"
# action_kakan = "行為：加槓"
# action_ankan = "行為：暗槓"
# action_kyuushukyuuhai_ryukyoku = "行為：九種九牌流局"
# action_riichi = "行為：立直"
# option_tsumo = "自摸"
# option_ron = "榮和"
# option_chii = "吃"
# option_pon = "碰"
# option_minkan = "槓"
# option_kakan = "槓"
# option_ankan = "槓"
# option_kyuushukyuuhai_ryukyoku = "行為：九種九牌"

ton = "東"
nan = "南"
shaa = "西"
pei = "北"
haku = "白"
hatsu = "發"
chun = "中"
# zero, one, two, three, four, five, six, seven, eight, nine, ten = "零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"

man = "萬"
suo = "索"
pin = "餅"
zuu = "字"

# mentsu = "面子"
koutsu = "刻子"
shuntsu = "順子"
# kan = "槓"
minkan = "明槓"
ankan = "暗槓"
kakan = "加槓"

# shibari = "番縛"

# kamichya = "上家"
# shimochya = "下家"
# toichya = "對家"

# status_agari = "和了"
# status_agari_renchan = "和了連莊"
# status_ryukyoku_renchan = "流局連莊"
# status_huanpai_ryukyoku = "荒牌流局"
# status_suukansanra = "四槓散了"
# status_suuhonrenda = "四風連打"
# status_kyuushukyuuhai_ryukyoku = "九種九牌"
# status_suuchariichi = "四家立直"
# status_sanchahoo = "三家和"

# yakuman_level_list=('','役滿','兩倍役滿','三倍役滿','四倍役滿','五倍役滿','六倍役滿','七倍役滿')
# kazoeyakuman='累計役滿'
# tehai="手牌"
dora='寶牌'
akadora='紅寶牌'
uradora='裡寶牌'

# 聽牌型
ryanmenmachi = "兩面聽" # 聽順子的左右兩張
tankimachi = "單騎聽" # 聽對子的其中一張
henchoomachi = "邊張聽" # 聽順子的左或右一張
kanchoomachi = "崁張聽" # 聽順子中洞
soohoomachi = "雙碰聽" # 聽兩對子其中任一對為刻子
chiitoitsutanmenmachi = "七對子單面聽"
kokushimusoutanmenmachi = "國士無雙單面聽"
kokushimusoujuusanmenmachi = "國士無雙十三面聽"

# 胡牌型
chiitoitsu_agari_type = "七對子型"
kokushimusou_agari_type = "國士無雙型"
normal_agari_type = "普通型"
special_koyaku_agari_type = "特殊古役型"

# 役
# 1
riichi='立直'
ippatsu="一發"
tsumo='自摸'
chyankan='搶槓'
haiteiraoyue='海底撈月'
houteiraoyui='河底撈魚'
tanyaochuu='斷么九'
yakuhai_ton='役牌：東'
yakuhai_nan='役牌：南'
yakuhai_shaa='役牌：西'
yakuhai_pei='役牌：北'
yakuhai_ton_chanfon='役牌：東（場風）'
yakuhai_nan_chanfon='役牌：南（場風）'
yakuhai_shaa_chanfon='役牌：西（場風）'
yakuhai_pei_chanfon='役牌：北（場風）'
yakuhai_haku='役牌：白'
yakuhai_hatsu='役牌：發'
yakuhai_chun='役牌：中'
pinfu='平和'
iipeekoo='一盃口'
rinshankaihou='嶺上開花'
# 2
dabururiichi='雙立直'
chiitoitsu='七對子'
sanshokudoujun='三色同順'
ikkitsuukan='一氣通貫'
honchantaiyaochuu='混全帶么九'
toitoihoo='對對和'
sanankoo='三暗刻'
honroutou='混老頭'
sanshokudookoo='三色同刻'
sankantsu='三槓子'
shousangen='小三元'
# 3
honiisoo='混一色'
junchantaiyaochuu='純全帶么九'
ryanpeekoo='二盃口'
# 6
chiniisoo='清一色'
# 13
tenhou='天和'
chiihou='地和'
kokushimusou='國士無雙'
suuankoo='四暗刻'
daisangen='大三元'
tsuuiisoo='字一色'
shousuushii='小四喜'
ryuuiisoo='綠一色'
chinroutou='清老頭'
chuurenpouton='九蓮寶燈'
suukantsu='四槓子'
# 26
kokushimusoujuusanmen='國士無雙十三面'
suuankootanki='四暗刻單騎'
junseichuurenpouton='純正九蓮寶燈'
daisuushii='大四喜'
# ?
beginning_of_the_cosmos='天地創世'
# other
nagashimankan = "流局滿貫"

# hoora="和了"
# fuu="符"
# han="番"
# ten="點"
# not_hoora="沒有和了"
# da="打"
# karaten="空聽"
# tenpai="聽牌"
# nooten="沒有聽牌"
# furiten="振聽"

# colon="："
# ideographic_comma="、"
# question_mark="？"

# has_koyaku="已開啟古役"
# not_has_koyaku="已關閉古役"
# koyaku="古役"
# 1
tsubamegaeshi = "燕返"
kanfuri = "槓振"
shiiaruraotai = "十二落抬"
shousanfon = "小三風"
# 2
sanrenkoo = "三連刻"
sanfonkoo = "三風刻"
chaopaikoo = "跳牌刻"
teinsankoo = "頂三刻"
chinpaikoo = "筋牌刻"
uumensai="五門齊"
ryanankan = "二暗槓"
# 3
isshokusanjun="一色三同順"
tanhonhoo = "斷紅和"
ryansuushun = "同順二盃口"
# 6
chitanhonhoo = "清斷紅和"
# 13
suurenkoo = "四連刻"
isshokuyonjun = "一色四同順"
suuchyaopaikoo = "四跳牌刻"
gozokukyouwa = "五族協和"
renhou = "人和"
suukantsuraotai = "四槓落抬"
suukanrinshan = "四槓花開"
katengecchi = "花天月地"
ishiuesannen = "石上三年"
sanankan = "三暗槓"
# 13 or 26
heiiisoo = "黑一色"
benikujyaku = "紅孔雀"
daisharin = "大車輪"
daisuurin = "大數鄰"
daichikurin = "大竹林"
sanshokudooankoo = "三色同暗刻"
# 26
junseisuurenkoo = "純正四連刻"
daichisei = "大七星"
junseiheiiisoo = "純正黑一色"
sanshokudookan = "三色同槓"
suuankan = "四暗槓"

paarenchan = "八連莊"
