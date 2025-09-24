### ==========================================================================.
#
#   倉庫内のアイテム管理システム.
#   to manege items in storage.
#
### ==========================================================================.

### ==========================================================================.
# import.

import os
from basement import BASEMENT
from loader import LOADER
from glov.glov_core import LS

### ==========================================================================.


### ==========================================================================.
# STORAGE.

class STORAGE_MANAGER():
    def __init__(self, PARENT:str="NOTHING"):
        """
PARENT : 親クラスのログ上での名称. <gC> とか.

GAME_INFO_DIR : ゲームの様々な情報が記述されたファイルが格納されたディレクトリ.
GAME_INFO_NAME : 使用するファイルの名称.

GAME_DIR : ゲーム名ごとのデータ保管ディレクトリ.
DATA_ID : データ名.
        """
        LS.VOMIT_LOG(msg=f"/*n|*//*<STORAGE>*/ | CALLED BY /*<{PARENT}*/")

        # =======================================.
        self.PARENT:str

        self.GAME_INFO_DIR:str
        self.GAME_INFO_NAME:str

        self.GAME_DIR:str
        self.DATA_ID:str
        self.SAVE_DIR:str
        # =======================================.
        self.INFO:dict
        # =======================================.

        RES, self.STORAGE = LOADER(DIR=self.SAVE_DIR, NAME=self.DATA_ID)
        if RES: # 倉庫情報読み込み.
            LS.VOMIT_LOG(msg="/*n|*//*<STORAGE>*/ | STORAGE INFO LOADED SUCCESSFULLY.")
        else:
            LS.VOMIT_LOG(msg="/*n|*//*<STORAGE>*/ | /*e*/FAILED TO LOAD STORAGE INFO./*e_*/")

        if self.LOAD_TRANS(): # アイテムIDとアイテム名の変換情報読み込み.
            LS.VOMIT_LOG(msg="/*n|*//*<STORAGE>*/ | TRANS LOADED SUCCESSFULLY.")
        else:
            LS.VOMIT_LOG(msg="/*n|*//*<STORAGE>*/ | /*e*/FAILED TO LOAD TRANS./*e_*/")

    def LOAD_TRANS(self) -> bool:
        try:
            self.ITEM = self.INFO["ITEM"]
            self.ITEM_ID = self.ITEM["ID"]
            self.ITEM_NAME = self.ITEM["NAME"]

            self.TRANS_ITEM_ID2NAME = dict(self.ITEM_ID, self.ITEM_NAME)
            self.TRANS_ITEM_NAME2ID = dict(self.ITEM_NAME, self.ITEM_ID)
            return True
        except:
            return False

    def GET_ITEM_ID(self, ID:int|str=0, num:int=0):
        """
**GET_ITEM : ITEMSではないので, 1種類のアイテムを入手した場合の処理.

ID ; int | str : アイテムのID.
num ; int : 入手個数.
        """
        FLAG_INVALID_OPERATION = False
        if num <= 0:
            LS.VOMIT_LOG(msg="/*n|*//*<STORAGE>*/ /*c*/num == 0 ; THE NUMBER OF GOT ITEM MUST BE OVER THAN ZERO.")
            FLAG_INVALID_OPERATION = True
        if str(ID) not in self.TRANS_ITEM_ID2NAME:
            LS.VOMIT_LOG(msg=f"/*n|*//*<STORAGE>*/ /*e*/ ID;{ID} DOES NOT EXIST.")
            FLAG_INVALID_OPERATION = True

        if FLAG_INVALID_OPERATION:
            LS.VOMIT_LOG(msg="/*n|*//*<STORAGE>-<GET_ITEM>*/ | FAILED")
            return
        self.STORAGE[str(ID)] += num
        LS.VOMIT_LOG(msg=f"/*n|*//*<STORAGE>-<GET_ITEM>*/ | GOT {num} {self.TRANS_ITEM_ID2NAME[str(ID)]}")

    def GET_ITEM_NAME(self, NAME:str="", num:int=0):
        """
基本はGET_ITE_ID()と同じ.
IDがNAMEになっているだけ.

NAME ; str : アイテム名:
        """
        FLAG_INVALID_OPERATION = False
        if num <= 0:
            LS.VOMIT_LOG(msg="/*n|*//*<STORAGE>*/ /*c*/num == 0 ; THE NUMBER OF GOT ITEM MUST BE OVER THAN ZERO.")
            FLAG_INVALID_OPERATION = True
        if str(NAME) not in self.TRANS_ITEM_NAME2ID:
            LS.VOMIT_LOG(msg=f"/*n|*//*<STORAGE>*/ /*e*/ NAME;{NAME} DOES NOT EXIST.")
            FLAG_INVALID_OPERATION = True

        if FLAG_INVALID_OPERATION:
            LS.VOMIT_LOG(msg="/*n|*//*<STORAGE>-<GET_ITEM>*/ | FAILED")
            return
        self.STORAGE[self.TRANS_ITEM_NAME2ID[NAME]] += num
        LS.VOMIT_LOG(msg=f"/*n|*//*<STORAGE>-<GET_ITEM>*/ | GOT {num} {self.TRANS_ITEM_NAME2ID[str(NAME)]}")

    def STOCK_CONFIRMATION_ID(self, ID:int|str=0, num:int=0):
        """
在庫確認用の関数

ID : アイテムID
num : 個数
        """
        if self.STORAGE[str(ID)] >= num:
            return True
        else:
            return False

    def STOCK_CONFIRMATION_NAME(self, NAME:str=0, num:int=0):
        """
アイテム名で在庫確認

NAME : アイテム名
num : 個数
        """
        return self.STOCK_CONFIRMATION_ID(ID=self.TRANS_ITEM_NAME2ID[NAME], num=num)


    def CONSUME_STOCK_ID(self, ID:int|str=0, num:int=0):
        """
アイテム消費

ID : アイテムID
num : 個数
        """
        if self.STOCK_CONFIRMATION_ID(ID=ID, num=num):
            self.STORAGE[str(ID)] -= num
        else:
            pass # FAILED.

    def CONSUME_STOCK_NAME(self, NAME:str="", num:int=0):
        """
アイテム消費

NAME : アイテム名
num : 個数
        """
        if self.STOCK_CONFIRMATION_NAME(NAME=NAME, num=num):
            self.STORAGE[self.TRANS_ITEM_NAME2ID[NAME]] -= num

### ==========================================================================.