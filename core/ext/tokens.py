import sys
import inspect

from config import Config

def to_lang(token: int | None) -> str | None:
    if token is None:
        return None
    current_module = sys.modules[__name__]
    module_locals = dict(inspect.getmembers(current_module))
    for key, value in module_locals.items():
        if value == token:
            return Config.lang["core.pai"].get(key)
    else:
        return None

ton = 11
nan = 12
shaa = 13
pei = 14
haku = 15
hatsu = 16
chun = 17

man = 21
suo = 22
pin = 23
zuu = 24

# mentsu = "面子"
koutsu = 31
shuntsu = 32
# kan = 33
minkan = 34
ankan = 35
kakan = 36

# yakuman_level_list=('','役滿','兩倍役滿','三倍役滿','四倍役滿','五倍役滿','六倍役滿','七倍役滿')
# kazoeyakuman='累計役滿'

dora = 41
akadora = 42
uradora = 43

# 聽牌型
ryanmenmachi = 51  # 聽順子的左右兩張
tankimachi = 52  # 聽對子的其中一張
henchoomachi = 53  # 聽順子的左或右一張
kanchoomachi = 54  # 聽順子中洞
soohoomachi = 55  # 聽兩對子其中任一對為刻子
chiitoitsutanmenmachi = 56
kokushimusoutanmenmachi = 57
kokushimusoujuusanmenmachi = 58

# 胡牌型
chiitoitsu_agari_type = 61
kokushimusou_agari_type = 62
normal_agari_type = 63
special_koyaku_agari_type = 64

# 役
# 1
riichi = 101
ippatsu = 102
tsumo = 103
chyankan = 104
haiteiraoyue = 105
houteiraoyui = 106
tanyaochuu = 107
yakuhai_ton = 108
yakuhai_nan = 109
yakuhai_shaa = 110
yakuhai_pei = 111
yakuhai_ton_chanfon = 112
yakuhai_nan_chanfon = 113
yakuhai_shaa_chanfon = 114
yakuhai_pei_chanfon = 115
yakuhai_haku = 116
yakuhai_hatsu = 117
yakuhai_chun = 118
pinfu = 119
iipeekoo = 120
rinshankaihou = 121
# 2
dabururiichi = 201
chiitoitsu = 202
sanshokudoujun = 203
ikkitsuukan = 204
honchantaiyaochuu = 205
toitoihoo = 206
sanankoo = 207
honroutou = 208
sanshokudookoo = 209
sankantsu = 210
shousangen = 211
# 3
honiisoo = 301
junchantaiyaochuu = 302
ryanpeekoo = 303
# 6
chiniisoo = 601
# 13
tenhou = 1301
chiihou = 1302
kokushimusou = 1303
suuankoo = 1304
daisangen = 1305
tsuuiisoo = 1306
shousuushii = 1307
ryuuiisoo = 1308
chinroutou = 1309
chuurenpouton = 1310
suukantsu = 1311
# 26
kokushimusoujuusanmen = 2601
suuankootanki = 2602
junseichuurenpouton = 2603
daisuushii = 2604
# ?
beginning_of_the_cosmos = 666666
# other
nagashimankan = 9901

# 古役
# 1
tsubamegaeshi = 151
kanfuri = 152
shiiaruraotai = 153
shousanfon = 154
# 2
sanrenkoo = 251
sanfonkoo = 252
chaopaikoo = 253
teinsankoo = 254
chinpaikoo = 255
uumensai = 256
ryanankan = 257
# 3
isshokusanjun = 351
tanhonhoo = 352
ryansuushun = 353
# 6
chitanhonhoo = 651
# 13
suurenkoo = 1351
isshokuyonjun = 1352
suuchyaopaikoo = 1353
gozokukyouwa = 1354
renhou = 1355
suukantsuraotai = 1356
suukanrinshan = 1357
katengecchi = 1358
ishiuesannen = 1359
sanankan = 1360
# 13 or 26
heiiisoo = 1461
benikujyaku = 1462
daisharin = 1463
daisuurin = 1464
daichikurin = 1465
sanshokudooankoo = 1466
# 26
junseisuurenkoo = 2651
daichisei = 2652
junseiheiiisoo = 2653
sanshokudookan = 2654
suuankan = 2655

paarenchan = 9951
