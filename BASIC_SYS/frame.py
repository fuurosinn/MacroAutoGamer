### ==========================================================================.
#
#
#   FRAME.
#
#
### ==========================================================================.


### ==========================================================================.
# import.

from BASIC_SYS.cord_loc import CORD_LOC
from copy import deepcopy

### ==========================================================================.


class FRAME():
    def __init__(self, frame_data:dict={}):
        self.data = frame_data
        self.dest:dict
        self.frame_list()

    def frame_list(self):
        """
PALの名称の1文字目にアスタリスクを使用してはならない.
        """
        self.dest:dict = {}
        for name, frame in zip(self.data.keys(), self.data.values()):
            f_cord = CORD_LOC(cord=frame["RECT"]) # frame cord, フレームの大きさ.
            if f_cord == []:
                continue
            if "PAL" not in frame.keys():
                continue

            s_frame:dict = {"*frame_cord":f_cord} # sub frame.
            sub_frame = frame["PAL"]
            for sub_name, sub_frame_data in zip(sub_frame.keys(), sub_frame.values()):
                sf_btn_cord = CORD_LOC(cord=sub_frame_data["C_BTN"]) # SubFrame_BuTonN_COoRDinate.
                sf_btns = sub_frame_data["C_BTN"] # func
                if "SET_FUNC" in sub_frame_data.keys(): # 任意関数設定.
                    pass
                if sub_name in s_frame.keys():
                    if type(sub_frame[sub_name]) == dict:
                        sub_frame[sub_name] = [sub_frame[sub_name], {sub_name:CORD_LOC(cord=f_cord)}]
                    elif type(sub_frame[sub_name]) == list:
                        sub_frame[sub_name] += [{sub_name:CORD_LOC(cord=f_cord)}]
                    else:
                        pass
                else:
                    s_frame |= {sub_name:{"*r_btn_cord":sf_btn_cord}} # r_cord : Relative BuTtoN COoRDinate.
            self.dest |= {name:deepcopy(s_frame)}
