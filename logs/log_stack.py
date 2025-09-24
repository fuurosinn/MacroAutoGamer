# ============================================================================.
#
# ログ出力関連の処理
#
# ============================================================================.


# ============================================================================.
#
# ---< Log Colouring Rules >---------------------------------------------------
#
# /*n*/ : CALL GET_TIME() FUNC AND INSERT IN A SENTENCE. AUTO COLOURING WITH YELLOW.
# "/*<NAME>*/" -> "< NAME >", INCLUDING {}. AUTO COLOURING WITH GREEN.
# The meaning of "/*<gC>*/" euqals "\033[32m< gC >\033[0m".
#
# ============================================================================.


from glov import glov_log as gL
from GET_TIME import GET_TIME
from logs._bar import BAR



class log_stacker(BAR):
    def __init__(self):
        super().__init__()
        gL.STACK = []
        gL.BASIC_COLOUR = "0"

    def SET_BASIC(self, COLOUR:str="0"):
        """
基本設定変更用関数

COLOUR -> 色

        """
        gL.BASIC_COLOUR = COLOUR

    def INTERPRETER_INSERTED_FNUCS(self, msg:str=""):
        while True: # 現在時刻表示.
            i = msg.find("/*n*/")
            if i == -1:
                break
            msg = msg[:i] + f"\033[33m{GET_TIME()}\033[{gL.BASIC_COLOUR}m" + msg[i+5:]
        while True: # 隔壁有りの現在時刻表示.
            i = msg.find("/*n|*/")
            if i ==-1:
                break
            msg = msg[:i] + f"\033[33m{GET_TIME()} | \033[{gL.BASIC_COLOUR}m" + msg[i+6:]
        while True: # ERROR.
            i = msg.find("/*e*/")
            if i == -1:
                break
            ia = msg.find("/*e_*/")
            if ia == -1:
                msg = msg[:i] + f"\033[31m[ERROR]\033[{gL.BASIC_COLOUR}m" + msg[i+5:]
            else:
                msg = msg[:i] + f"\033[31m[ERROR] " + msg[i+5:ia] + f"\033[{gL.BASIC_COLOUR}m" + msg[ia+6:]
        while True: # CAUTION.
            i = msg.find("/*c*/")
            if i == -1:
                break
            ia = msg.find("/*c_*/")
            if ia == -1:
                msg = msg[:i] + f"\033[33m[CAUTION]\033[{gL.BASIC_COLOUR}m" + msg[i+5:]
            else:
                msg = msg[:i] + f"\033[33m[CAUTION] " + msg[i+5:ia] + f"\033[{gL.BASIC_COLOUR}m" + msg[ia+6:]
        while True: # 改行.
            i = msg.find("/*l*/")
            if i == -1:
                break
            msg = msg[:i] + "\n" + msg[i+5:]
        while True: # 表示元.
            i = msg.find("/*<")
            if i == -1:
                break
            ia = msg.find(">*/")
            if ia == -1:
                raise
            msg = msg[:i] + "\033[32m< " + msg[i+3:ia] + f" >\033[{gL.BASIC_COLOUR}m" + msg[ia+3:]
        return msg

    def NEW_LINE(self, l:int=1):
        """
l : 改行数
        """
        gL.STACK += [""] * l

    def LOGGING(self, msg:str=""):
        """
ログ出力予定追加用関数.
        """
        def LOGGER(m:str=""):
#            p = m.find("@")
#            if p >= 0:
#                c = m[:p] # colouring.
#                m = m[p+1:]
#           else:
#                c = "0"
#            gL.STACK += [self.COLOUR(msg=m, colour=c)]
            gL.STACK += [self.COLOUR(msg=m, colour=gL.BASIC_COLOUR)]

        if type(msg) == str:
            LOGGER(m=msg)
        elif type(msg) in [list, tuple]:
            for temp in msg:
                LOGGER(m=temp)

    def VOMIT_LOG(self, msg:str="", dyeing:bool=True):
        print(self.COLOUR(msg=self.INTERPRETER_INSERTED_FNUCS(msg=msg), colour=gL.BASIC_COLOUR if dyeing else "0"))

    def PUSH(self):
        """
ログ出力.
        """
        for msg in gL.STACK:
            print(msg)
        gL.STACK = []

    def COLOUR(self, msg:str="", colour:str=gL.BASIC_COLOUR) -> str:
        return f"\033[{colour}m" + msg + gL.RESET_COLOUR

    def COLOUR_WITH_CODE(self, RGB:str="114514") -> str:
        """
    文字を染色するシーケンス(\033[38;2;RR;GG;BBm)を返す.
        """
        res = "\033[38;2"
        for i in range(3):
            res += ";" + str(int(RGB[i*2:i*2+2], 16))
        res += "m"
        return res

    def gene_bar(self, char:str="=", l:int="80") -> str:
        """
仕切り用の文字列を返す関数.
        """
        return char * l

    def BLOCK(self, msg:list|tuple=[], name:str="") -> list:
        """
        """
        m = [self.gene_bar()]
        msg = [" < " + name + " >"] + msg
        for msg_ in msg:
            m += ["|"+msg_]
        m += [self.gene_bar()]
        return m