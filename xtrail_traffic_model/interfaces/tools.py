from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict

import pandas as pd


class Tools(ABC):
    """工具调用接口。"""

    @abstractmethod
    def normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def summarize(self, df: pd.DataFrame) -> Dict[str, float]:
        raise NotImplementedError
