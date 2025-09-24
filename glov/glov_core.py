# ============================================================================.
#
# 変数共有用のモジュール.
#
# ============================================================================.


# -*- coding: utf-8 -*-



# ============================================================================.
# 開始 | 時間関連.


from GET_TIME import GET_TIME, SET_TIME_ZONE

TIME_ZONE = "Asia/Tokyo"
SET_TIME_ZONE(zone=TIME_ZONE)
SYSTEM_BOOT_TIME = GET_TIME() # (だいたいの)起動時刻.

ACTIVE_TIME = GET_TIME() - SYSTEM_BOOT_TIME # 稼働継続時間.


# 終了 | 時間関連.
# ============================================================================.



# ============================================================================.
# log関連.


from logs.log_stack import log_stacker
from glov import glov_log as gL # log用のデータ共有専用モジュールにアクセス. circlar import errorを回避するため.

#gL.LS.LOGGING(msg="")
LS = log_stacker()

# ============================================================================.



# ============================================================================.
# 開始 | ディレクトリ関連.


import os
SYSTEM_BOOT_DIR = os.getcwd() # 起動位置取得.



    #== ==========================================================================.
    # 開始 | プロセス関連.


from app.VANITAS.core import VANITATUM
ACTIVE_APPLICATION_ID = 0 # 起動中のアプリID.
ACTIVE_APPLICATION_INSTANCE = VANITATUM() # 起動中のアプリ用のインスタンス.

import json # アプリに対してIDを付けるので, それの対応表読み込み.
with open(os.path.join(SYSTEM_BOOT_DIR, "CONFIG\\APPLICATION_ID.json"), encoding="utf-8") as f:
    APPLICATION_ID2NAME_LIST = json.load(f) # アプリのID対応表読み込み.
ACTIVE_APPLICATION_NAME = ""
def RESET_APPLICATION():
    global ACTIVE_APPLICATION_NAME
    ACTIVE_APPLICATION_NAME = APPLICATION_ID2NAME_LIST[str(ACTIVE_APPLICATION_ID)] # 起動中のアプリ名.
    LS.VOMIT_LOG(msg=f"/*n|*//*<g>*/ RESET_APPLICATION : ACTIVE_APPLICATION_NAME == {ACTIVE_APPLICATION_NAME}")

RESET_APPLICATION()

    # 終了 | プロセス関連.
    #== ==========================================================================.

### ==========================================================================.

SYSTEM_URGENCY = 0 # システムの状態.

### ==========================================================================.


with open(os.path.join(SYSTEM_BOOT_DIR, "CONFIG\\NOX_DIR.json"), encoding="utf-8") as f:
    SYSTEM_NOX = json.load(f)
SYSTEM_NOX_DIR = SYSTEM_NOX["NOX_DIR"] # NOXのディレクトリの位置.
SYSTEM_NOX_SCREENCAP_DIR = SYSTEM_NOX["NOX_SCREENCAP_DIR"] # NOX内部でのスクショの一時保管場所.
SYSTEM_SCREENCAP_DIR = SYSTEM_NOX["SCREENCAP_DIR"] # 実行場所から見た相対的なスクショ保管位置.
SYSTEM_IMG_DIR = SYSTEM_NOX["IMG_DIR"]


APP_CORE_PATH = "" # 現在起動中のアプリのcore.pyの位置.
APP_SCREENSHOT_PATH = "" # 現在起動中のアプリでのPC側でのスクショの保管ディレクトリ.
APP_SCREENSHOT_IMG_PATH = "" # 現在起動中のアプリでのPC側でのスクショファイルの保管場所.
APP_IMGS_DIR = "" # 現在起動中のアプリの画像フォルダ.
def SET_SCREENSHOT_PATH(): # 撮影したスクショの保管場所設定.
    global APP_CORE_PATH, APP_SCREENSHOT_PATH, APP_SCREENSHOT_IMG_PATH, APP_IMGS_DIR
    APP_CORE_PATH = os.path.join(SYSTEM_BOOT_DIR, "app", ACTIVE_APPLICATION_NAME)
    APP_SCREENSHOT_PATH = os.path.join(SYSTEM_BOOT_DIR, "app", ACTIVE_APPLICATION_NAME, SYSTEM_SCREENCAP_DIR)
    APP_SCREENSHOT_IMG_PATH = os.path.join(APP_SCREENSHOT_PATH, "screenshot.png")
    APP_IMGS_DIR = os.path.join(SYSTEM_BOOT_DIR, "app", ACTIVE_APPLICATION_NAME, SYSTEM_IMG_DIR)
#    print(f"CHECK APP_SCREENSHOT_PATH == {APP_SCREENSHOT_PATH}")
SET_SCREENSHOT_PATH()



LS.SET_BASIC(COLOUR="37")
LS.LOGGING(msg=[f"NOW : {GET_TIME()}"])
LS.LOGGING(msg=["", LS.LOG_BLOCK(name="DIR", mode="LEFT"), f"SYSTEM_NOX_DIR : {SYSTEM_NOX_DIR}", f"SYSTEM_NOX_SCREENCAP_DIR : {SYSTEM_NOX_SCREENCAP_DIR}", f"SYSTEM_SCREENCAP_DIR : {SYSTEM_SCREENCAP_DIR}", f"APP_SCREENSHOT_PATH : {APP_SCREENSHOT_PATH}", ""])
LS.PUSH()

def SHOW_DIR():
    LS.SET_BASIC(COLOUR="33")
    LS.LOGGING(msg=[f"NOW : {GET_TIME()}"])
    LS.LOGGING(msg=["", LS.LOG_BLOCK(name="DIR", mode="LEFT"), ""])
    LS.NEW_LINE(l=1)
    LS.SET_BASIC(COLOUR="37")


# 終了 | ディレクトリ関連.
# ============================================================================.


if __name__ == "__main__":
    pass