from ..lang import tc as lang

######################### 遊戲規則設定 ##########################
gametype_tensuu_init_dict = { # 開局點數
    lang.yonin_ton: 25000,
    lang.yonin_ton_ikkyoku: 25000,
    lang.yonin_nan: 25000,
    lang.sannin_ton: 35000,
    lang.sannin_ton_ikkyoku: 35000,
    lang.sannin_nan: 35000
}

gametype_tensuu_over_dict = { # 最低結束點數
    lang.yonin_ton: 30000,
    lang.yonin_ton_ikkyoku: 30000,
    lang.yonin_nan: 30000,
    lang.sannin_ton: 40000,
    lang.sannin_ton_ikkyoku: 40000,
    lang.sannin_nan: 40000
}

is_tobitsuzuku = False # 是否擊飛繼續

is_last_oya_infinitely_renchan = False

shibarisuu = 1 # 飜縛

is_koyaku = False # 是否包含古役

is_aotenjyou = False # 是否使用青天井規則

is_kuitan = True # 是否有食斷

pinfu_ron_fusuu = 30 # 平和榮和符數

rienfontoitsu_fusuu = 2 # 連風對子符數

################################################################

######################### 基本字形定義 #########################
##### key 不得重複 #####
lang_paitype_dict = { # 不得重複 # 不得為數字
    lang.man: "m",
    lang.suo: "s",
    lang.pin: "p", 
    lang.zuu: "z"
}

paitype_sign_number_dict = {
    "m": 1, "s": 2, "p": 3, "z": 4
}

fonwei_tuple = ( # 不得重複
    lang.ton, lang.nan, lang.shaa, lang.pei
)

lang_yakuhai_painame_dict = {
    lang.yakuhai_ton: "1z", 
    lang.yakuhai_nan: "2z", 
    lang.yakuhai_shaa: "3z", 
    lang.yakuhai_pei: "4z", 
    lang.yakuhai_ton_chanfon: "1z", 
    lang.yakuhai_nan_chanfon: "2z", 
    lang.yakuhai_shaa_chanfon: "3z", 
    lang.yakuhai_pei_chanfon: "4z", 
    lang.yakuhai_haku: "5z", 
    lang.yakuhai_hatsu: "6z", 
    lang.yakuhai_chun: "7z"
}

fonwei_lang_tsufon_yaku_dict = {
    lang.ton: lang.yakuhai_ton, 
    lang.nan: lang.yakuhai_nan, 
    lang.shaa: lang.yakuhai_shaa, 
    lang.pei: lang.yakuhai_pei, 
}

fonwei_lang_chanfon_yaku_dict = {
    lang.ton: lang.yakuhai_ton_chanfon, 
    lang.nan: lang.yakuhai_nan_chanfon, 
    lang.shaa: lang.yakuhai_shaa_chanfon, 
    lang.pei: lang.yakuhai_pei_chanfon, 
}

lang_tsufon_yaku_fonwei_dict = {
    lang.yakuhai_ton: lang.ton, 
    lang.yakuhai_nan: lang.nan, 
    lang.yakuhai_shaa: lang.shaa, 
    lang.yakuhai_pei: lang.pei, 
}

lang_chanfon_yaku_fonwei_dict = {
    lang.yakuhai_ton_chanfon: lang.ton, 
    lang.yakuhai_nan_chanfon: lang.nan, 
    lang.yakuhai_shaa_chanfon: lang.shaa, 
    lang.yakuhai_pei_chanfon: lang.pei, 
}

lang_action_lang_option_dict = {
    lang.action_tsumo: lang.option_tsumo, 
    lang.action_ron: lang.option_ron, 
    lang.action_chii: lang.option_chii, 
    lang.action_pon: lang.option_pon, 
    lang.action_minkan : lang.option_minkan, 
    lang.action_kakan : lang.option_kakan, 
    lang.action_ankan : lang.option_ankan
}
################################################################

######################### 特殊牌組字形 ##########################

yaochuu_paitype_tuple = ("1m", "9m", "1p", "9p", "1s", "9s", "1z", "2z", "3z", "4z", "5z", "6z", "7z")
ryuuiisoopai_paitype_tuple = ("2s", "3s", "4s", "6s", "8s", "6z")
chinroutoupai_paitype_tuple = ("1m", "9m", "1p", "9p", "1s", "9s")
sanyuanpai_paitype_tuple = ("5z", "6z", "7z")
suushiipai_paitype_tuple = ("1z", "2z", "3z", "4z")

################################################################

######################### 基本遊戲設定 ##########################
gametype_player_num_dict = {
    lang.yonin_ton: 4,
    lang.yonin_ton_ikkyoku: 4,
    lang.yonin_nan: 4,
    lang.sannin_ton: 3,
    lang.sannin_ton_ikkyoku: 3,
    lang.sannin_nan: 3
}

chanfon_pos_dict = {
    lang.ton:0, lang.nan:1, lang.shaa:2, lang.pei:3
}

################################################################

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



