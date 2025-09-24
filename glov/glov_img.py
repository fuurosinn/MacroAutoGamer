# ============================================================================.
#
#
#
# ============================================================================.



from json import load
with open(f"./CONFIG/IMG_EXTENSION.json") as f:
    IMG_EXTENSION = load(f) # load -> loads?.



IMG_SCREENSHOT = None # スクショ.
IMG_SCREENSHOT_GRAY = None # グレイスケール.

TEMP_NAME = "" # ボタン, アイコン, etc... などの名称.
TEMP_MATCH = None # 捜索対象.
TEMP_MATCH_GRAY = None # グレイスケール.


# ============================================================================.
# < START > | LOADING ICONS. 


import cv2

ITEM_ICONS = {} # アイコン類の画像まとめ.
APP_ICONS = {}

with open(f"./CONFIG/APPLICATION_ID.json", mode="r") as f:
    APP_LIST = load(f)

for num, app_name in zip(APP_LIST.keys(), APP_LIST.values()):
    APP_ICONS.update({num:cv2.cvtColor(cv2.imread(f"./app/{app_name}/Imgs/icon.png"), cv2.COLOR_BGR2GRAY)})


# < END > | LOADING ICONS.
# ============================================================================.



# ============================================================================.
# < START > | 探索結果格納変数.


MATCH_TEMPLATE_RES_X = -1
MATCH_TEMPLATE_RES_Y = -1


# < END > | 探索結果格納変数.
# ============================================================================.



# ============================================================================.
# < START > | 画像事前読み込み.

# BTN -> 画面遷移などはしないボタン.
# IMG -> 単なる画像.
# JMP -> 画面遷移するボタン.
# GRP -> ひとまとまりにしたほうが都合の良いボタンの集合.

IMGS = {}

# ============================================================================.



def RESET():
    global IMG_SCREENSHOT, IMG_SCREENSHOT_GRAY, TEMP_NAME, TEMP_MATCH, TEMP_MATCH_GRAY, MATCH_TEMPLATE_RES_X, MATCH_TEMPLATE_RES_Y, IMGS
    IMG_SCREENSHOT = None
    IMG_SCREENSHOT_GRAY = None
    TEMP_NAME = None
    TEMP_MATCH = None
    TEMP_MATCH_GRAY = None
    MATCH_TEMPLATE_RES_X = -1
    MATCH_TEMPLATE_RES_Y = -1
    IMGS = {}