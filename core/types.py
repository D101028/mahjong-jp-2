from typing import Any, Literal, TypedDict

PaiDictType = TypedDict('PaiDictType', {
    "name": str
})
FuroDictType = TypedDict('FuroDictType', {
    "type": int, 
    "self-pai-tuple": tuple[PaiDictType, ...] | None, 
    "received-pai": PaiDictType | None, 
    "from-player-id": int | None, 
    "self-koutsu-furo": "None | FuroDictType"
})
TehaiDictType = TypedDict('TehaiDictType', {
    "pai-list": list[PaiDictType], 
    "furo-list": list[FuroDictType], 
    "penuki-list": list[PaiDictType], 
    "new-pai": PaiDictType | None
})

RiverDictType = TypedDict('RiverDictType', {
    "pai-list": list[PaiDictType], 
    "riichi-hai-pos": int | None
})

HyoujihaiInfoDictType = TypedDict('HyoujihaiInfoDictType', {
    "dora-hyouji-list": list[PaiDictType], 
    "uradora-hyouoji-list": None | list[PaiDictType]
})

PlayerTehaiUpdateNotationContentType = TypedDict('PlayerTehaiUpdateNotationContentType', {
    "tehai-info": TehaiDictType
}) # Response: None
PlayerDatsuhaiNotationContentType = TypedDict('PlayerDatsuhaiNotationContentType', {
    "player-id": int, 
    "datsuhai": PaiDictType, 
    "to-riichi": bool
}) # Response: None
PlayerMinpaiNotationContentType = TypedDict('PlayerMinpaiNotationContentType', {
    "player-id": int, 
    "furo-info": FuroDictType
}) # Response: None
PlayerPenukiNotationContentType = TypedDict('PlayerPenukiNotationContentType', {
    "player-id": int, 
    "penuki-pai": PaiDictType
}) # Response: None
PlayerRonNotationContentType = TypedDict('PlayerRonNotationContentType', {
    "player-id": int, 
    "tehai-info": TehaiDictType, 
    "ron-pai": PaiDictType, 
    "from-player-id": int
}) # Response: None
PlayerTsumoNotationContentType = TypedDict('PlayerTsumoNotationContentType', {
    "player-id": int, 
    "tehai-info": TehaiDictType
}) # Response: None
HyoujihaiUpdateNotationContentType = TypedDict('HyoujihaiUpdateNotationContentType', {
    "hyoujihai-info": HyoujihaiInfoDictType
}) # Response: None
AskToDatsuhaiContentType = TypedDict('AskToDatsuhaiContentType', {
    "datsuhai-choices": list[int | None] | list[int] # None 表示摸切
}) # Response: int
AskToDatsuhaiOrOtherChoicesContentType = TypedDict('AskToDatsuhaiOrOtherChoicesContentType', {
    "datsuhai-choices": list[int | None] | list[int],  # None 表示摸切
    "other-choices": list[Literal['ankan', 'kakan', 'penuki', 'tsumo', 'kyuushukyuhai', 'riichi', 'cancel']]
}) # Response: int
AskToChoicesContentType = TypedDict('AskToChoicesContentType', {
    "choices": list[Literal['chi', 'pon', 'minkan', 'ron', 'cancel']]
}) # Response: int
AskToChooseMinpaiCombContentType = TypedDict('AskToChooseMinpaiCombContentType', {
    "pai-comb-list": list[list[PaiDictType]]
}) # Response: int
AskToPlayRiichiContentType = TypedDict('AskToPlayRiichiContentType', {
    "datsuhai-choices": list[int | None] | list[int], 
    "choices": list[Literal['cancel']]
})