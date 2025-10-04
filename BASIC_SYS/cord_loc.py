### ==========================================================================.
#
#
#   座標変換.
#
#
### ==========================================================================.


### ==========================================================================.
# import.



### ==========================================================================.



def CORD_LOC(cord:dict={}) -> list:
    """
ボタンがどこに存在するのか, ボタンの大きさなどを解析.
cord ; dict : ボタンの位置データ, xywhでもx0y0x1y1でも自動で判断する.
    """
    cord_keys:list = cord.keys()
    if all(i in cord_keys for i in ("x", "y", "w", "h")):
        x0 = cord["x"]
        y0 = cord["y"]
        w = cord["w"]
        h = cord["h"]
        if any(i == None for i in (x0, y0, w, h)):
            return []
        x1 = x0 + w
        y1 = y0 + h
    elif all(i in cord_keys for i in ("x0", "y0", "x1", "y0")):
        x0 = cord["x0"]
        y0 = cord["y0"]
        x1 = cord["x1"]
        y1 = cord["y1"]
        if any(i == None for i in (x0, y0, x1, y1)):
            return []
    else:
        return []
    return [x0, y0, x1, y1]