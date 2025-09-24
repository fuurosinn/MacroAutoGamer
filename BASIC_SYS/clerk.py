### ==========================================================================.
#
#   キャラとかの様々な情報を表示するためのモジュール.
#
### ==========================================================================.


### ==========================================================================.
# import.

import os

from glov import glov_core as g
from glov.glov_core import LS

from BASIC_SYS.loader import LOADER

from BASIC_SYS.basement import BASEMENT
from BASIC_SYS.saver import SAVER

### ==========================================================================.

class CLERK(BASEMENT, SAVER):
    def __init__(self, PARENT:str="NOTHING", DATA_ID:str=""):
        self.PARENT:str

        self.GAME_INFO_DIR:str
        self.GAME_INFO_NAME:str

        self.GAME_DIR:str
        self.DATA_ID:str
        SAVER.__init__(self)
        self.SAVE_DIR:str
        self.SAVE_NAME:str = "chara"
        self.DUMP_DATA:dict

        self.LOAD_CHARACTER()
        self.SETTING()

    def LOAD_CHARACTER(self):
        self.CHARA_DATA = LOADER(DIR=self.SAVE_DIR, NAME="chara.json")
        self.DUMP_DATA = self.CHARA_DATA

    def SETTING(self):
        """
表示ルールとかの設定.
        """
        pass

    def show(self, chara_name:str=""):
        data = self.CHARA_DATA[chara_name]
        self.NAME = data["NAME"]
        self.RARITY = data["RARITY"]
        self.LVL = data["LVL"]
        self.MAX_LVL = data["LVL_LIMIT"]
        if self.SYSTEM_CHARA_EXP:
            self.EXP = data["EXP"]
            self.NEXT_LVL = data["NEXT_LVL"] # 次レベルまでの必要経験値量.

        self.LOCKED:bool = data["LOCKED"]

        self.SKILL = data["SKILL"]
        self.GEAR = data["GEAR"]
        self.SKIN = data["SKIN"]

    def SKINS(self):
        msg = [""]
        for i in self.SKIN.values():
            m = []
            skin_name = i["NAME"]
            skin_got = i["GOT"]
            skin_cate = i["CATEGORY"]
            skin_equipped = i["EQUIPPED"]
            m += []

            msg += LS.BLOCK(msg=m, name=skin_name)

        LS.BLOCK(msg=msg, name="SKIN")