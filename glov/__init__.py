# ============================================================================.
#
# データ共有用のモジュールをパッケージ化
#
# ============================================================================.

from glov import glov_core as g # 通常のデータ共有用モジュール.
from glov import glov_log as gL # ログ関連.
from glov import glov_controll as gC # 操作系統.
from glov import glov_img as gI # 画像系統.

__all__ = ["g", "gL", "gC", "gI"]