### ==========================================================================.
#
#
#   アカウントIDからセーブデータの名前を返答する.
#
#
### ==========================================================================.


### ==========================================================================.
# import.

from glov import *
from glov.glov_core import LS
import os
from json import load

### ==========================================================================.


class BOOKLET():
    def __init__(self):
        self.VL_BOOKLET_PREFIX = f"/*n|*//*<BOOKLET>*/ : "
        LS.VOMIT_LOG(msg=self.VL_BOOKLET_PREFIX+"/*st*/ACTIVE/*st_*/")

        self.PARENT:str
        self.BOOKLET_DIR:str
        self.BOOKLET_PATH = os.path.join(self.BOOKLET_DIR, self.PARENT+".json") # booklet内部のアカウント情報のパス生成.

        self.LOADING_BOOKLET()

        LS.VOMIT_LOG(msg=self.VL_BOOKLET_PREFIX+"/*st*/LAUNCHED/*st_*/")

    def LOADING_BOOKLET(self):
        with open(self.BOOKLET_PATH, mode="r", encoding="unicode-escape") as f:
            self.BOOKLET_LIST = load(f)

    def TRANS_ID2NAME(self, ID:str="") -> str:
        """
アカウントIDでセーブデータの名前を取得.
        """
        try:
            RES = self.BOOKLET_LIST[ID]
        except KeyError as e:
            LS.VOMIT_LOG(msg=self.VL_BOOKLET_PREFIX+f"/*e*/ID == {ID} ; NOT EXIST/*e_*/")
            return ""
        LS.VOMIT_LOG(msg=self.VL_BOOKLET_PREFIX+f"ID == {ID} --> NAME == {RES}")
        return RES