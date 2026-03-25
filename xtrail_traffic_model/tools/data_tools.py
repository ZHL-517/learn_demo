from __future__ import annotations

from typing import Dict

import pandas as pd

from xtrail_traffic_model.interfaces.tools import Tools


class DataTools(Tools):
    """智慧交通常用数据工具。"""

    def normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        """统一列名并填充缺失值。"""
        norm = df.copy()
        norm.columns = [c.strip().lower() for c in norm.columns]
        return norm.fillna(method="ffill").fillna(0)

    def summarize(self, df: pd.DataFrame) -> Dict[str, float]:
        """输出核心交通统计指标。"""
        summary: Dict[str, float] = {}
        if "flow" in df.columns:
            summary["avg_flow"] = float(df["flow"].mean())
            summary["peak_flow"] = float(df["flow"].max())
        if "speed" in df.columns:
            summary["avg_speed"] = float(df["speed"].mean())
        if "queue" in df.columns:
            summary["avg_queue"] = float(df["queue"].mean())
        return summary
