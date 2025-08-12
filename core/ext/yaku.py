from core.ext import tokens

######################### 役種相關 ##############################
class Yaku():
    def __init__(self, yakutoken: int, 
                 hansuu: int, 
                 is_furo_minus: bool = False, 
                 is_menchin_only: bool = False, 
                 is_yakuman: bool = False): 
        self.yakutoken = yakutoken
        self.ori_hansuu = hansuu 
        self.is_furo_minus = is_furo_minus
        self.is_menchin_only = is_menchin_only
        self.is_yakuman = is_yakuman
    
    def __eq__(self, other):
        if not isinstance(other, Yaku):
            return False
        return other.yakutoken == self.yakutoken

    def __str__(self):
        return self.yakutoken

    def copy(self):
        return Yaku(self.yakutoken, self.ori_hansuu, self.is_furo_minus, self.is_menchin_only, self.is_yakuman)

# 役種名稱不可重複
# 通常役
ichihan_yaku_list = [
    tokens.riichi,
    tokens.ippatsu,
    tokens.tsumo,
    tokens.chyankan,
    tokens.haiteiraoyue,
    tokens.houteiraoyui,
    tokens.tanyaochuu,
    tokens.yakuhai_ton,
    tokens.yakuhai_nan,
    tokens.yakuhai_shaa,
    tokens.yakuhai_pei,
    tokens.yakuhai_ton_chanfon,
    tokens.yakuhai_nan_chanfon,
    tokens.yakuhai_shaa_chanfon,
    tokens.yakuhai_pei_chanfon,
    tokens.yakuhai_haku,
    tokens.yakuhai_hatsu,
    tokens.yakuhai_chun,
    tokens.pinfu,
    tokens.iipeekoo,
    tokens.rinshankaihou
]
nihan_yaku_list = [
    tokens.dabururiichi,
    tokens.chiitoitsu,
    tokens.sanshokudoujun,
    tokens.ikkitsuukan,
    tokens.honchantaiyaochuu,
    tokens.toitoihoo,
    tokens.sanankoo,
    tokens.honroutou,
    tokens.sanshokudookoo,
    tokens.sankantsu,
    tokens.shousangen
]
sanhan_yaku_list = [
    tokens.honiisoo,
    tokens.junchantaiyaochuu,
    tokens.ryanpeekoo
]
rokuhan_yaku_list = [
    tokens.chiniisoo
]
yakuman_yaku_list = [
    tokens.tenhou,
    tokens.chiihou,
    tokens.kokushimusou,
    tokens.suuankoo,
    tokens.daisangen,
    tokens.tsuuiisoo,
    tokens.shousuushii,
    tokens.ryuuiisoo,
    tokens.chinroutou,
    tokens.chuurenpouton,
    tokens.suukantsu
]
daburu_yakuman_yaku_list = [
    tokens.kokushimusoujuusanmen,
    tokens.suuankootanki,
    tokens.junseichuurenpouton,
    tokens.daisuushii
]
mechin_only_yaku_list = [
    tokens.riichi,
    tokens.tsumo,
    tokens.pinfu,
    tokens.iipeekoo,
    tokens.chiitoitsu,
    tokens.dabururiichi,
    tokens.ryanpeekoo,
    tokens.kokushimusou,
    tokens.suuankoo,
    tokens.chuurenpouton,
    tokens.chiihou,
]
furo_minus_yaku_list = [
    tokens.sanshokudoujun,
    tokens.ikkitsuukan,
    tokens.honchantaiyaochuu,
    tokens.honiisoo,
    tokens.junchantaiyaochuu,
    tokens.chiniisoo
]

# 古役
ichihan_koyaku_list = [
    tokens.tsubamegaeshi, 
    tokens.kanfuri, 
    tokens.shiiaruraotai, 
    tokens.shousanfon
]
nihan_koyaku_list = [
    tokens.sanrenkoo, 
    tokens.sanfonkoo, 
    tokens.chaopaikoo, 
    tokens.teinsankoo, 
    tokens.chinpaikoo, 
    tokens.uumensai, 
    tokens.ryanankan
]
sanhan_koyaku_list = [
    tokens.isshokusanjun, 
    tokens.tanhonhoo, 
    tokens.ryansuushun
]
rokuhan_koyaku_list = [
    tokens.chitanhonhoo
]
yakuman_koyaku_list = [
    tokens.suurenkoo, 
    tokens.isshokuyonjun, 
    tokens.gozokukyouwa, 
    tokens.renhou, 
    tokens.suukantsuraotai, 
    tokens.suukanrinshan, 
    tokens.katengecchi, 
    tokens.ishiuesannen, 
    tokens.sanankan, 
    # can be daburu yakuman
    tokens.heiiisoo, 
    tokens.benikujyaku, 
    tokens.daisharin, 
    tokens.daisuurin, 
    tokens.daichikurin, 
    tokens.sanshokudooankoo
]
daburu_yakuman_koyaku_list = [
    tokens.junseisuurenkoo, 
    tokens.daichisei, 
    tokens.junseiheiiisoo, 
    tokens.sanshokudookan, 
    tokens.suuankan
]
mechin_only_koyaku_list: list[int] = []
furo_minus_koyaku_list: list[int] = []

token_yaku_dict: dict[int, Yaku] = {}

for yakutoken in ichihan_yaku_list:
    yaku = Yaku(yakutoken = yakutoken, 
                hansuu = 1, 
                is_furo_minus = (yakutoken in furo_minus_yaku_list),
                is_menchin_only = (yakutoken in mechin_only_yaku_list))
    token_yaku_dict.update({yakutoken: yaku})
for yakutoken in nihan_yaku_list:
    yaku = Yaku(yakutoken = yakutoken, 
                hansuu = 2, 
                is_furo_minus = (yakutoken in furo_minus_yaku_list),
                is_menchin_only = (yakutoken in mechin_only_yaku_list))
    token_yaku_dict.update({yakutoken: yaku})
for yakutoken in sanhan_yaku_list:
    yaku = Yaku(yakutoken = yakutoken, 
                hansuu = 3, 
                is_furo_minus = (yakutoken in furo_minus_yaku_list),
                is_menchin_only = (yakutoken in mechin_only_yaku_list))
    token_yaku_dict.update({yakutoken: yaku})
for yakutoken in rokuhan_yaku_list:
    yaku = Yaku(yakutoken = yakutoken, 
                hansuu = 6, 
                is_furo_minus = (yakutoken in furo_minus_yaku_list),
                is_menchin_only = (yakutoken in mechin_only_yaku_list))
    token_yaku_dict.update({yakutoken: yaku})
for yakutoken in yakuman_yaku_list:
    yaku = Yaku(yakutoken = yakutoken, 
                hansuu = 13, 
                is_furo_minus = (yakutoken in furo_minus_yaku_list),
                is_menchin_only = (yakutoken in mechin_only_yaku_list),
                is_yakuman = True)
    token_yaku_dict.update({yakutoken: yaku})
for yakutoken in daburu_yakuman_yaku_list:
    yaku = Yaku(yakutoken = yakutoken, 
                hansuu = 26, 
                is_furo_minus = (yakutoken in furo_minus_yaku_list),
                is_menchin_only = (yakutoken in mechin_only_yaku_list),
                is_yakuman = True)
    token_yaku_dict.update({yakutoken: yaku})

################################################################

######################### 複合役 ################################

koumokukoukan_token_dict: dict[int, tuple[Yaku]] = { # 不可複合役之組合
    tokens.honroutou: (token_yaku_dict[tokens.honchantaiyaochuu], ), 
    tokens.junchantaiyaochuu: (token_yaku_dict[tokens.honchantaiyaochuu], ), 
    tokens.ryanpeekoo: (token_yaku_dict[tokens.iipeekoo], )
}

oatenjyou_koumokukoukan_token_dict: dict[int, tuple[Yaku, ...]] = { # 不可複合之役(for 青天井)組合
    tokens.tenhou: (token_yaku_dict[tokens.tsumo], ), 
    tokens.chiihou: (token_yaku_dict[tokens.tsumo], ), 
    tokens.suuankoo: (token_yaku_dict[tokens.sanankoo], 
                    token_yaku_dict[tokens.toitoihoo]), 
    tokens.kokushimusou: (token_yaku_dict[tokens.honroutou], ), 
    tokens.kokushimusoujuusanmen: (token_yaku_dict[tokens.honroutou], ), 
    tokens.tsuuiisoo: (token_yaku_dict[tokens.honchantaiyaochuu], 
                     token_yaku_dict[tokens.honroutou]), 
    tokens.chinroutou: (token_yaku_dict[tokens.honchantaiyaochuu], 
                      token_yaku_dict[tokens.honroutou]), 
    tokens.daisuushii: (token_yaku_dict[tokens.toitoihoo], ), 
    tokens.chuurenpouton: (token_yaku_dict[tokens.chiniisoo], ), 
    tokens.junseichuurenpouton: (token_yaku_dict[tokens.chiniisoo], )
}

koumokukoukan_koyaku_token_dict: dict[int, tuple[Yaku]] = {}
oatenjyou_koumokukoukan_koyaku_token_dict: dict[int, tuple[Yaku]] = {}

################################################################


