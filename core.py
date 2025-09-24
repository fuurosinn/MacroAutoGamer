# ============================================================================.
#
# 起動はこいつから
#
# ============================================================================.


# -*- coding: utf-8 -*-

### ==========================================================================.
# import.

import os
from time import sleep

# ==================================================================.
# app関連.

#import app.app_module
import app
from glov import *
import app_instance as api

# ==================================================================.

import argparse # 引数入れてみるぞ---!!.

import threading
import McrDiscoRepo.core


### ==========================================================================.

#DEBUG = [False, True] # デバッグ用.
PARSER = argparse.ArgumentParser()
PARSER.add_argument("--core", help="Boot up the main program", action="store_false") # アプリ操作コードを管理する中心プログラム.
PARSER.add_argument("--disco", help="Execute Discord BOT", action="store_false") # ディスコードのBOT起動. 指定しなければ起動しない.
ARGS = PARSER.parse_args()

BOOT_UP = [ARGS.core, ARGS.disco]


THREADS = []

class core():
    def __init__(self):
        gC.CONT.GET_SCREENCAP()
        self.BOOT_APP(APP_ID=2)

    def SETUP(self):
        g.ACTIVE_APPLICATION_INSTANCE

    def BOOT_APP(self, APP_ID:int=1):
        # アプリ起動のログ出力処理が必要.
        g.LS.VOMIT_LOG(msg=f"/*n|*//*<core>*/ BOOT UP : ID == {APP_ID}")
        g.ACTIVE_APPLICATION_ID = APP_ID
        g.ACTIVE_APPLICATION_INSTANCE = api.APP_INSTANCE[APP_ID]() # はえ-, この処理通るんだ---(知ってたけど).

if __name__ == "__main__":
    THREADS.append(threading.Thread(target=core))
    THREADS.append(threading.Thread(target=McrDiscoRepo.core.CLIENT, kwargs={"intents":McrDiscoRepo.core.INTENTS, "token":McrDiscoRepo.core.TKN}))

    for num, flag in enumerate(BOOT_UP):
        if flag:
            THREADS[num].start()
    """
    if DEBUG[0]:
        THREADS[0].start()
    if DEBUG[1]:
        THREADS[1].start()

    if DEBUG[0]:
        THREADS[0].join()
    if DEBUG[1]:
        THREADS[1].join()
    """

#    ACT_CORE = core()
#    print(gC.CONT.cmd(command="nox_adb shell logcat -v time -d"))