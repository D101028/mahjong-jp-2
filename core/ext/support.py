from .. import lang

######################### 遊戲規則設定 ##########################
# gametype_tensuu_init_dict = { # 開局點數
#     lang.yonin_ton: 25000,
#     lang.yonin_ton_ikkyoku: 25000,
#     lang.yonin_nan: 25000,
#     lang.sannin_ton: 35000,
#     lang.sannin_ton_ikkyoku: 35000,
#     lang.sannin_nan: 35000
# }

# gametype_tensuu_over_dict = { # 最低結束點數
#     lang.yonin_ton: 30000,
#     lang.yonin_ton_ikkyoku: 30000,
#     lang.yonin_nan: 30000,
#     lang.sannin_ton: 40000,
#     lang.sannin_ton_ikkyoku: 40000,
#     lang.sannin_nan: 40000
# }

# is_tobitsuzuku = False # 是否擊飛繼續

# is_last_oya_infinitely_renchan = False

# shibarisuu = 1 # 飜縛

# is_koyaku = False # 是否包含古役

# is_aotenjyou = False # 是否使用青天井規則

# is_kuitan = True # 是否有食斷

# pinfu_ron_fusuu = 30 # 平和榮和符數

# rienfontoitsu_fusuu = 2 # 連風對子符數

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

######################### 特殊牌組字形 ##########################

yaochuu_paitype_tuple = ("1m", "9m", "1p", "9p", "1s", "9s", "1z", "2z", "3z", "4z", "5z", "6z", "7z")
ryuuiisoopai_paitype_tuple = ("2s", "3s", "4s", "6s", "8s", "6z")
chinroutoupai_paitype_tuple = ("1m", "9m", "1p", "9p", "1s", "9s")
sanyuanpai_paitype_tuple = ("5z", "6z", "7z")
suushiipai_paitype_tuple = ("1z", "2z", "3z", "4z")

################################################################

