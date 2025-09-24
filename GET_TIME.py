from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from zoneinfo import *
from json import load


with open("./CONFIG/TIME.json", mode="r") as f:
    TIME_CONFIG = load(f)
ZONE = TIME_CONFIG["TIMEZONE"]

def SET_TIME_ZONE(zone:str=ZONE):
    """
ZONE設定とTIME_ZONE設定.
    """
    global ZONE, TIME_ZONE
    ZONE = zone
    print(f"\033[32m< GET_TIME >\033[0m ; SET_TIME_ZONE : ZONE == {zone}")
    TIME_ZONE = ZoneInfo(ZONE)
    print(f"\033[32m< GET_TIME >\033[0m ; SET_TIME_ZONE : TIME_ZONE WAS CHANGED.")

# SET_TIME_ZONE(zone="Asia/Tokyo")

def GET_TIME(tz:ZoneInfo=TIME_ZONE): # 現在時刻取得.
    return datetime.now(tz)


if __name__ == "__main__":
    print(f"\033[32m< GET_TIME >\033[0m ; ZONE == {ZONE}")
    print(f"\033[32m< GET_TIME >\033[0m ; GET_TIME : {GET_TIME()}")
else:
    print(f"\033[33m{GET_TIME()} |\033[0m \033[32m< GET_TIME >\033[0m ; IMPORTED")