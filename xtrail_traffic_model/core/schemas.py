from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import pandas as pd


@dataclass
class MultiModalInput:
    """多模态输入数据模型。"""

    text: str = ""
    audio_path: Optional[str] = None
    csv_df: Optional[pd.DataFrame] = None


@dataclass
class AgentResult:
    """智能体输出标准结构。"""

    agent_name: str
    narrative: str
    table: pd.DataFrame
    figure: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UnifiedOutput:
    """系统统一输出。"""

    intent: str
    route: str
    summary: str
    result: AgentResult
