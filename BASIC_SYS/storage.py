### ==========================================================================.
#
#   倉庫内のアイテム管理システム.
#   to manege items in storage.
#
### ==========================================================================.

### ==========================================================================.
# import.

import os
from BASIC_SYS.basement import BASEMENT
from BASIC_SYS.loader import LOADER
from BASIC_SYS.saver import SAVER
from json import load, dump
from glov.glov_core import LS

from BASIC_SYS.Exceptions.storage_exception import *

### ==========================================================================.


### ==========================================================================.
# STORAGE.

class STORAGE_MANAGER(SAVER):
    def __init__(self, PARENT:str="NOTHING"):
        """
PARENT : 親クラスのログ上での名称. <gC> とか.

GAME_INFO_DIR : ゲームの様々な情報が記述されたファイルが格納されたディレクトリ.
GAME_INFO_NAME : 使用するファイルの名称.

GAME_DIR : ゲーム名ごとのデータ保管ディレクトリ.
DATA_ID : データ名.
        """
        self.VL_STORAGE_PRESET = "/*n|*//*<STORAGE>*/ | "
        self.VL_GET_ITEM_PRESET = "/*|*//*<STORAGE.GET_ITEM>*/ | "
        LS.VOMIT_LOG(msg=self.VL_STORAGE_PRESET+f"CALLED BY /*<{PARENT}>*/")

        # =======================================.
        self.PARENT:str

        self.GAME_INFO_DIR:str
        self.GAME_INFO_NAME:str

        self.GAME_DIR:str
        self.DATA_ID:str
        self.DATA_DIR:dict
        self.SAVE_DIR:str

        self.FLAG_SET_DATA_ID:bool
        self.FLAG_ITEM_INFO_LOADED:bool = False
        self.FLAG_STORAGE_LOADED:bool = False
        # =======================================.
        self.INFO:dict
        # =======================================.
        self.SET_STORAGE()

    def SET_STORAGE(self):
        if self.FLAG_SET_DATA_ID:
            self.STORAGE_SAVE_DIR = self.DATA_DIR["STORAGE_DIR"] # 保管場所. storage.json .
            try:
                with open(os.path.join(self.SAVE_DIR, self.STORAGE_SAVE_DIR), mode="r", encoding="unicode-escape") as f:
                    self.STORAGE = load(f)
                RES = True
            except:
                RES = False
            if RES: # 倉庫情報読み込み.
                self.FLAG_STORAGE_LOADED = True
                LS.VOMIT_LOG(msg=self.VL_STORAGE_PRESET+"STORAGE INFO LOADED SUCCESSFULLY.")
            else:
                self.FLAG_STORAGE_LOADED = False
                LS.VOMIT_LOG(msg=self.VL_STORAGE_PRESET+"/*e*/FAILED TO LOAD STORAGE INFO./*e_*/")

            if self.LOAD_TRANS(): # アイテムIDとアイテム名の変換情報読み込み.
                LS.VOMIT_LOG(msg=self.VL_STORAGE_PRESET+"TRANS LOADED SUCCESSFULLY.")
            else:
                LS.VOMIT_LOG(msg=self.VL_STORAGE_PRESET+"/*e*/FAILED TO LOAD TRANS./*e_*/")
        else:
            LS.VOMIT_LOG(msg="/*n|*//*<STORAGE>*/ ; /*st*/INVALID/*st_*/")

    def LOAD_TRANS(self) -> bool:
        try:
            self.ITEM = self.INFO["ITEM"]
            self.ITEM_NAME = self.ITEM["NAME"]

            self.FLAG_ITEM_INFO_LOADED = True
            return True
        except:
            self.FLAG_ITEM_INFO_LOADED = False
            return False

### ==========================================================================.

    def CHECK_INVALID_ITEM_AMOUNT(self, num:int):
        if num == None:
            raise NoneAmount(num)
        if not isinstance(num, (int, float, complex)):
            raise NotNumericAmount(num)
        elif isinstance(num, complex):
            raise ComplexAmount(num)
        if num < 0:
            raise NegativeAmount(num)
        if type(num) == float:
            if num != int(num):
                raise FloatAmount(num)

### ==========================================================================.

    def GET_ITEM(self, item_name:str="unknown", item_amount:int=0):
        self.CHECK_INVALID_ITEM_AMOUNT(num=item_amount) # 指定されたアイテムの量が不正な値ではないかどうかを確認.
        self.STORAGE[item_name]["AMOUNT"] += item_amount

### ==========================================================================.

    def CONFIRM_ITEM_EXIST(self, item_name:str="unknown"):
        """
ゲーム内部に存在しているアイテムかどうか確認.
        """
        if item_name in self.STORAGE.keys():
            return True
        else:
            return False

    def CONFIRM_STOCK(self, item_name:str="unknown", item_amount:int=0):
        """
在庫確認.
        """
        if item_amount < 0:
            LS.VOMIT_LOG(msg=self.VL_STORAGE_PRESET+f"/*st*/WARINIG/*st_*/ ; The arg value must be positive integar. ({item_amount} < 0)")
            return False
        if self.STORAGE[item_name]["AMOUNT"] >= item_amount:
            return True
        else:
            return False

### ==========================================================================.

    def CONSUME_STOCK(self, item_name:str, item_amount:int):
        """
アイテム消費.
        """
        if not self.CONFIRM_ITEM_EXIST(item_name=item_name):
            return
        self.CHECK_INVALID_ITEM_AMOUNT(num=item_amount)
        self.STORAGE[item_name]["AMOUNT"] -= item_amount

### ==========================================================================.

    def SAVE_STORAGE(self):
        self.SAVE_SUB_DATA(DATA=self.STORAGE, SAVE_DIR=self.SAVE_DIR, NAME="storage.json")
#        with open(os.path.join(self.SAVE_DIR, "storage.json", ), mode="w") as f:
#            dump(self.STORAGE, f, indent=4)