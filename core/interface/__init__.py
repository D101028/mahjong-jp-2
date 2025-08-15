"""
Intent purpose 對應 content 及 response 格式：
- *-notation: {
    ...
  }; None
- ask-to-datsuhai: {
    "datsuhai-choices": list[int] # 每個選項代表對映 tehai.pai_list 的字典序
  }; int # 代表選取的選項字典序 (e.g. 如果是 2，則表示選 choices_list[2])
- ask-to-datsuhai-or-other-choices: {
    "datsuhai-choices": list[int], 
    "other-choices": list[Literal['ankan', 'kakan', 'penuki', 'tsumo', 'cancel']]
  }; int # 兩個 choices 列表合併後的字典序
- ask-to-choices: {
    "choices": list[Any] # 如吃、碰、槓、和等
  }; int
"""
from .intent import *
from .prompt import *
from .interactor import *

