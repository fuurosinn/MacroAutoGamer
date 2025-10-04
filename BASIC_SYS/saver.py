### ==========================================================================.
#
#   セーブ用関数.
#
### ==========================================================================.


### ==========================================================================.
# import.

from glov import glov_core as g
from json import dump
import os

### ==========================================================================.

class SAVER:
    def __init__(self):
        """
self.DIR : データを保存するディレクトリ.
self.NAME : 保存するデータの名称. 自動的に設定した拡張子が付与される.
self.EXTENSION : 保存する形式(拡張子).
self.DUMP_DATA : 保存するデータ.
        """
        g.LS.VOMIT_LOG(msg="/*n|*//*<SAVER>*/ : /*st*/ACTIVE/*st_*/")
        self.SAVE_DIR:str # BASEMENTを継承しているならばself.SAVE_DIRは事前に生成される.
        self.SAVE_NAME:str
        self.SAVE_EXTENSION:str = ".json"
        self.DUMP_DATA:dict
        g.LS.VOMIT_LOG(msg="/*n|*//*<SAVER>*/ : /*st*/LAUNCHED/*st_*/")

    def SAVE_MAIN_DATA(self):
        with open(os.path.join(self.SAVE_DIR, self.SAVE_NAME+self.SAVE_EXTENSION), mode="w", encoding="unicode-escape") as f:
            dump(self.DUMP_DATA, f, indent=4, ensure_ascii=False)

    def SAVE_SUB_DATA(self, DATA:dict={}, SAVE_DIR:str="", NAME:str=""):
        with open(os.path.join(SAVE_DIR, NAME), mode="w", encoding="utf-8") as f:
            dump(DATA, f, indent=4, ensure_ascii=False)

