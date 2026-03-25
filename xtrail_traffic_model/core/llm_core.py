from __future__ import annotations

from dataclasses import dataclass

from xtrail_traffic_model.agents.traffic_agents import (
    SignalControlAgent,
    SimulationAgent,
    TalentTrainingAgent,
    TrafficPredictionAgent,
    VehicleDispatchAgent,
)
from xtrail_traffic_model.core.schemas import MultiModalInput, UnifiedOutput


@dataclass
class IntentRoute:
    intent: str
    route: str


class TrafficLLMCore:
    """行之 X-TRAIL 交通大模型中枢（简化实现）。"""

    def __init__(self) -> None:
        self.agents = {
            "traffic_prediction": TrafficPredictionAgent(),
            "signal_control": SignalControlAgent(),
            "traffic_simulation": SimulationAgent(),
            "vehicle_dispatch": VehicleDispatchAgent(),
            "talent_training": TalentTrainingAgent(),
        }

    def parse_intent(self, text: str) -> str:
        """意图解析：基于关键词进行交通场景识别。"""
        t = (text or "").lower()
        if any(k in t for k in ["预测", "forecast", "拥堵趋势", "流量"]):
            return "traffic_prediction"
        if any(k in t for k in ["信号", "红绿灯", "配时", "signal"]):
            return "signal_control"
        if any(k in t for k in ["仿真", "simulation", "场景对比"]):
            return "traffic_simulation"
        if any(k in t for k in ["调度", "dispatch", "运力", "车辆"]):
            return "vehicle_dispatch"
        if any(k in t for k in ["培训", "人才", "课程", "能力"]):
            return "talent_training"
        return "traffic_prediction"

    def smart_route(self, payload: MultiModalInput) -> IntentRoute:
        """智能路由调度：根据意图映射到对应智能体。"""
        intent = self.parse_intent(payload.text)
        route = f"router://xtrail/{intent}"
        return IntentRoute(intent=intent, route=route)

    def run(self, payload: MultiModalInput) -> UnifiedOutput:
        route_info = self.smart_route(payload)
        result = self.agents[route_info.intent].execute(payload)
        summary = f"已将请求路由到 {result.agent_name}，完成智慧交通分析。"
        return UnifiedOutput(
            intent=route_info.intent,
            route=route_info.route,
            summary=summary,
            result=result,
        )
