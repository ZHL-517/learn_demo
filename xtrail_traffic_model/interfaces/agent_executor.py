from __future__ import annotations

from abc import ABC, abstractmethod

from xtrail_traffic_model.core.schemas import AgentResult, MultiModalInput


class AgentExecutor(ABC):
    """智能体执行接口。"""

    @abstractmethod
    def execute(self, payload: MultiModalInput) -> AgentResult:
        """执行智能体任务并返回标准结果。"""
        raise NotImplementedError
