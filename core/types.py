from typing import Any, Literal, TypedDict, Union

PaiDictType = TypedDict('PaiDictType', {
    "name": str
})
FuroDictType = TypedDict('FuroDictType', {
    "type": int, 
    "self-pai-tuple": tuple[PaiDictType, ...] | None, 
    "received-pai": PaiDictType | None, 
    "from_player_id": int | None, 
    "self-koutsu-furo": Union[None, 'FuroDictType']
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
})
PlayerDatsuhaiNotationContentType = TypedDict('PlayerDatsuhaiNotationContentType', {
    "player-id": int, 
    "datsuhai": PaiDictType, 
    "is-riichi": bool
})
RiverUpdateNotationContentType = TypedDict('RiverUpdateNotationContentType', {
    "player-id": int, 
    "river-info": RiverDictType
})
HyoujihaiUpdateNotationContentType = TypedDict('HyoujihaiUpdateNotationContentType', {
    "hyoujihai-info": HyoujihaiInfoDictType
})
AskToDatsuhaiContentType = TypedDict('AskToDatsuhaiContentType', {
    "datsuhai-choices": list[int]
})
AskToDatsuhaiOrOtherChoicesContentType = TypedDict('AskToDatsuhaiOrOtherChoicesContentType', {
    "datsuhai-choices": list[int], 
    "other-choices": list[Literal['ankan', 'kakan', 'penuki', 'tsumo', 'cancel']]
})
AskToChoicesContentType = TypedDict('AskToChoicesContentType', {
    "choices": list[Literal['chi', 'pon', 'minkan', 'ron', 'cancel']]
})
