from __future__ import annotations

from abc import ABC, abstractmethod

from xtrail_traffic_model.core.schemas import AgentResult, MultiModalInput
from xtrail_traffic_model.interfaces.agent_executor import AgentExecutor
from xtrail_traffic_model.tools.data_tools import DataTools


class BaseTrafficAgent(AgentExecutor, ABC):
    """交通智能体基类。"""

    def __init__(self) -> None:
        self.tools = DataTools()

    @abstractmethod
    def execute(self, payload: MultiModalInput) -> AgentResult:
        raise NotImplementedError
