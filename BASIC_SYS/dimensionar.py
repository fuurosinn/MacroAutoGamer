### ==========================================================================.
#
#
#   ゲーム内での現在地までの経路を記録する.
#   例えば現在地が倉庫なら, ホーム画面 -> 倉庫がまず考えられる.
#   しかしホーム画面 -> キャラクター一覧 -> 特定のキャラ -> 倉庫という経路もあり得る.
#   このように同じ位置にいるけど経路が違うから, 戻るボタンを押したときに戻る場所が異なることが考えられる.
#   その問題を解決するための機能.
#
#
### ==========================================================================.


### ==========================================================================.
# import.

import os
from loader import LOADER

from BASIC_SYS.basement import BASEMENT

### ==========================================================================.
# dimensionar.


class DIMENSIONAR(BASEMENT):
    def __init__(self):
        # =====================================.
        self.PARENT:str

        self.GAME_INFO_DIR:str
        self.GAME_INFO_NAME:str

        self.GAME_DIR:str
        self.DATA_ID:str
        # =====================================.
        self.HOME = "LOGIN" # base.
        self.WAY = [] # 現在地までの道のり.
        self.ROOT = [] # 現在地までに使用した階層の情報. 例えば{"a":{"b":{~}}}なら, [{"b":{~}}, {~}]となる.

        self.SET_DIMENTION()

    def SET_DIMENTION(self):
        """
階層設定.
        """
        self.DIM_STRUC = LOADER(DIR=self.GAME_INFO_DIR, NAME=self.DATA_DIR["GAME_INFO_DIMENSION"])
#        self.DIM_STRUC = LOADER(DIR=f"./game_info/{self.PARENT}", NAME="dim.json")

    def ASCENT(self):
        """
上の階層に戻る.
        """
        if self.ROOT[-1] == self.HOME:
            raise
        del self.WAY[-1]
        del self.ROOT[-1]

    def DESCENT(self, NAME:str=""):
        """
下の階層に降りる.
NAME ; str : 指定する階層.
        """
        if NAME not in self.ROOT[-1].keys(): # 指定された階層が存在しない場合.
            raise
        self.WAY.append(NAME)
        self.ROOT.append(self.ROOT[-1][self.WAY[-1]])