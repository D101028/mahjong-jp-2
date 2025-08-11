from .. import lang

######################### 役種相關 ##############################
class Yaku():
    def __init__(self, yakuname: str, 
                 hansuu: int, 
                 is_furo_minus: bool = False, 
                 is_menchin_only: bool = False, 
                 is_yakuman: bool = False): 
        self.yakuname = yakuname
        self.ori_hansuu = hansuu 
        self.is_furo_minus = is_furo_minus
        self.is_menchin_only = is_menchin_only
        self.is_yakuman = is_yakuman
    
    def __eq__(self, other):
        if not isinstance(other, Yaku):
            return False
        return other.yakuname == self.yakuname

    def __str__(self):
        return self.yakuname

    def copy(self):
        return Yaku(self.yakuname, self.ori_hansuu, self.is_furo_minus, self.is_menchin_only, self.is_yakuman)

# 役種名稱不可重複
# 通常役
ichihan_yaku_list = [
    lang.riichi,
    lang.ippatsu,
    lang.tsumo,
    lang.chyankan,
    lang.haiteiraoyue,
    lang.houteiraoyui,
    lang.tanyaochuu,
    lang.yakuhai_ton,
    lang.yakuhai_nan,
    lang.yakuhai_shaa,
    lang.yakuhai_pei,
    lang.yakuhai_ton_chanfon,
    lang.yakuhai_nan_chanfon,
    lang.yakuhai_shaa_chanfon,
    lang.yakuhai_pei_chanfon,
    lang.yakuhai_haku,
    lang.yakuhai_hatsu,
    lang.yakuhai_chun,
    lang.pinfu,
    lang.iipeekoo,
    lang.rinshankaihou
]
nihan_yaku_list = [
    lang.dabururiichi,
    lang.chiitoitsu,
    lang.sanshokudoujun,
    lang.ikkitsuukan,
    lang.honchantaiyaochuu,
    lang.toitoihoo,
    lang.sanankoo,
    lang.honroutou,
    lang.sanshokudookoo,
    lang.sankantsu,
    lang.shousangen
]
sanhan_yaku_list = [
    lang.honiisoo,
    lang.junchantaiyaochuu,
    lang.ryanpeekoo
]
rokuhan_yaku_list = [
    lang.chiniisoo
]
yakuman_yaku_list = [
    lang.tenhou,
    lang.chiihou,
    lang.kokushimusou,
    lang.suuankoo,
    lang.daisangen,
    lang.tsuuiisoo,
    lang.shousuushii,
    lang.ryuuiisoo,
    lang.chinroutou,
    lang.chuurenpouton,
    lang.suukantsu
]
daburu_yakuman_yaku_list = [
    lang.kokushimusoujuusanmen,
    lang.suuankootanki,
    lang.junseichuurenpouton,
    lang.daisuushii
]
mechin_only_yaku_list = [
    lang.riichi,
    lang.tsumo,
    lang.pinfu,
    lang.iipeekoo,
    lang.chiitoitsu,
    lang.dabururiichi,
    lang.ryanpeekoo,
    lang.kokushimusou,
    lang.suuankoo,
    lang.chuurenpouton,
    lang.chiihou,
]
furo_minus_yaku_list = [
    lang.sanshokudoujun,
    lang.ikkitsuukan,
    lang.honchantaiyaochuu,
    lang.honiisoo,
    lang.junchantaiyaochuu,
    lang.chiniisoo
]

# 古役
ichihan_koyaku_list = [
    lang.tsubamegaeshi, 
    lang.kanfuri, 
    lang.shiiaruraotai, 
    lang.shousanfon
]
nihan_koyaku_list = [
    lang.sanrenkoo, 
    lang.sanfonkoo, 
    lang.chaopaikoo, 
    lang.teinsankoo, 
    lang.chinpaikoo, 
    lang.uumensai, 
    lang.ryanankan
]
sanhan_koyaku_list = [
    lang.isshokusanjun, 
    lang.tanhonhoo, 
    lang.ryansuushun
]
rokuhan_koyaku_list = [
    lang.chitanhonhoo
]
yakuman_koyaku_list = [
    lang.suurenkoo, 
    lang.isshokuyonjun, 
    lang.gozokukyouwa, 
    lang.renhou, 
    lang.suukantsuraotai, 
    lang.suukanrinshan, 
    lang.katengecchi, 
    lang.ishiuesannen, 
    lang.sanankan, 
    # can be daburu yakuman
    lang.heiiisoo, 
    lang.benikujyaku, 
    lang.daisharin, 
    lang.daisuurin, 
    lang.daichikurin, 
    lang.sanshokudooankoo
]
daburu_yakuman_koyaku_list = [
    lang.junseisuurenkoo, 
    lang.daichisei, 
    lang.junseiheiiisoo, 
    lang.sanshokudookan, 
    lang.suuankan
]
mechin_only_koyaku_list: list[str] = []
furo_minus_koyaku_list: list[str] = []

lang_yaku_dict: dict[str, Yaku] = {}

for yakuname in ichihan_yaku_list:
    yaku = Yaku(yakuname = yakuname, 
                hansuu = 1, 
                is_furo_minus = (yakuname in furo_minus_yaku_list),
                is_menchin_only = (yakuname in mechin_only_yaku_list))
    lang_yaku_dict.update({yakuname: yaku})
for yakuname in nihan_yaku_list:
    yaku = Yaku(yakuname = yakuname, 
                hansuu = 2, 
                is_furo_minus = (yakuname in furo_minus_yaku_list),
                is_menchin_only = (yakuname in mechin_only_yaku_list))
    lang_yaku_dict.update({yakuname: yaku})
for yakuname in sanhan_yaku_list:
    yaku = Yaku(yakuname = yakuname, 
                hansuu = 3, 
                is_furo_minus = (yakuname in furo_minus_yaku_list),
                is_menchin_only = (yakuname in mechin_only_yaku_list))
    lang_yaku_dict.update({yakuname: yaku})
for yakuname in rokuhan_yaku_list:
    yaku = Yaku(yakuname = yakuname, 
                hansuu = 6, 
                is_furo_minus = (yakuname in furo_minus_yaku_list),
                is_menchin_only = (yakuname in mechin_only_yaku_list))
    lang_yaku_dict.update({yakuname: yaku})
for yakuname in yakuman_yaku_list:
    yaku = Yaku(yakuname = yakuname, 
                hansuu = 13, 
                is_furo_minus = (yakuname in furo_minus_yaku_list),
                is_menchin_only = (yakuname in mechin_only_yaku_list),
                is_yakuman = True)
    lang_yaku_dict.update({yakuname: yaku})
for yakuname in daburu_yakuman_yaku_list:
    yaku = Yaku(yakuname = yakuname, 
                hansuu = 26, 
                is_furo_minus = (yakuname in furo_minus_yaku_list),
                is_menchin_only = (yakuname in mechin_only_yaku_list),
                is_yakuman = True)
    lang_yaku_dict.update({yakuname: yaku})

################################################################

######################### 複合役 ################################

koumokukoukan_lang_dict: dict[str, tuple[Yaku]] = { # 不可複合役之組合
    lang.honroutou: (lang_yaku_dict[lang.honchantaiyaochuu], ), 
    lang.junchantaiyaochuu: (lang_yaku_dict[lang.honchantaiyaochuu], ), 
    lang.ryanpeekoo: (lang_yaku_dict[lang.iipeekoo], )
}

oatenjyou_koumokukoukan_lang_dict: dict[str, tuple[Yaku, ...]] = { # 不可複合之役(for 青天井)組合
    lang.tenhou: (lang_yaku_dict[lang.tsumo], ), 
    lang.chiihou: (lang_yaku_dict[lang.tsumo], ), 
    lang.suuankoo: (lang_yaku_dict[lang.sanankoo], 
                    lang_yaku_dict[lang.toitoihoo]), 
    lang.kokushimusou: (lang_yaku_dict[lang.honroutou], ), 
    lang.kokushimusoujuusanmen: (lang_yaku_dict[lang.honroutou], ), 
    lang.tsuuiisoo: (lang_yaku_dict[lang.honchantaiyaochuu], 
                     lang_yaku_dict[lang.honroutou]), 
    lang.chinroutou: (lang_yaku_dict[lang.honchantaiyaochuu], 
                      lang_yaku_dict[lang.honroutou]), 
    lang.daisuushii: (lang_yaku_dict[lang.toitoihoo], ), 
    lang.chuurenpouton: (lang_yaku_dict[lang.chiniisoo], ), 
    lang.junseichuurenpouton: (lang_yaku_dict[lang.chiniisoo], )
}

koumokukoukan_koyaku_lang_dict: dict[str, tuple[Yaku]] = {}
oatenjyou_koumokukoukan_koyaku_lang_dict: dict[str, tuple[Yaku]] = {}

################################################################


