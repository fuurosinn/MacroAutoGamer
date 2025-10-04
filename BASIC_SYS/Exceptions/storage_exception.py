### ==========================================================================.
#
#
#   storageでの例外クラス.
#
#
### ==========================================================================.



class FuncCallError(Exception):
    """
StorageFuncCallError
STORAGEの関数を呼び出しで問題があった場合の例外.
    """
    pass

class InvalidArg(FuncCallError):
    """
無効な引数.
    """
    def __init__(self, arg=""):
        self.arg = arg

class InvalidAmount(InvalidArg):
    """
引数で無効なアイテム量が指定された場合.
    """
    def __str__(self):
        return f"{self.arg} <--- Item amount is invalid."

class NoneAmount(InvalidAmount):
    """
アイテム個数が指定されていない, Noneの場合.
    """
    def __str__(self):
        return f"Item amount is None."

class NotNumericAmount(InvalidAmount):
    """
アイテムの個数指定がそもそも数値型ではない場合.
    """
    def __str__(self):
        return f"{self.arg} <--- Item amount is not numeric type."

class NegativeAmount(InvalidAmount):
    """
アイテムの個数で負の値が設定されていた場合.
    """
    def __str__(self):
        return f"{self.arg} <--- Item amount is set to a Negative value."

class ComplexAmount(InvalidAmount):
    """
複素数個指定すんな.
    """
    def __str__(self):
        return f"{self.arg} <--- Item amount is complex number."

class FloatAmount(InvalidAmount):
    """
個数指定が整数に変換できないfloat型の場合.
1.0は1と解釈できるから問題無い.
    """
    def __str__(self):
        return f"{self.arg} <--- Item amount is float, unable to translate int."

