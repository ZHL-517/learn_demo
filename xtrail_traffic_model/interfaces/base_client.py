from __future__ import annotations

from abc import ABC, abstractmethod

from xtrail_traffic_model.core.schemas import MultiModalInput


class BaseClient(ABC):
    """数据处理接口：统一接收多模态输入并转化为标准结构。"""

    @abstractmethod
    def ingest(self, text: str = "", audio_path: str | None = None, csv_path: str | None = None) -> MultiModalInput:
        """将原始输入转为 MultiModalInput。"""
        raise NotImplementedError
