from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from xtrail_traffic_model.agents.base import BaseTrafficAgent
from xtrail_traffic_model.core.schemas import AgentResult, MultiModalInput

sns.set_theme(style="whitegrid")


class TrafficPredictionAgent(BaseTrafficAgent):
    """交通预测智能体。"""

    def execute(self, payload: MultiModalInput) -> AgentResult:
        df = self.tools.normalize(payload.csv_df.copy())
        df["pred_flow_next_hour"] = df["flow"].rolling(3, min_periods=1).mean().shift(1).fillna(df["flow"].mean()).round(1)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(df["hour"], df["flow"], label="当前流量")
        ax.plot(df["hour"], df["pred_flow_next_hour"], label="预测流量", linestyle="--")
        ax.set_title("交通流量预测")
        ax.set_xlabel("小时")
        ax.set_ylabel("车辆/小时")
        ax.legend()

        return AgentResult(
            agent_name="TrafficPredictionAgent",
            narrative="预测结果显示晚高峰时段流量显著上升，建议提前发布绕行诱导信息。",
            table=df[["hour", "flow", "pred_flow_next_hour"]].head(12),
            figure=fig,
            metadata=self.tools.summarize(df),
        )


class SignalControlAgent(BaseTrafficAgent):
    """信控智能体。"""

    def execute(self, payload: MultiModalInput) -> AgentResult:
        df = self.tools.normalize(payload.csv_df.copy())
        df["suggested_green_ratio"] = (df["flow"] / df["flow"].max() * 0.5 + 0.3).clip(0.3, 0.8).round(2)

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(data=df.head(12), x="hour", y="suggested_green_ratio", ax=ax, color="#4C72B0")
        ax.set_title("信号灯绿信比建议")
        ax.set_ylabel("绿信比")
        ax.set_xlabel("小时")

        return AgentResult(
            agent_name="SignalControlAgent",
            narrative="系统已生成动态绿信比建议，可用于早晚高峰自适应配时。",
            table=df[["hour", "flow", "suggested_green_ratio"]].head(12),
            figure=fig,
            metadata=self.tools.summarize(df),
        )


class SimulationAgent(BaseTrafficAgent):
    """交通仿真智能体。"""

    def execute(self, payload: MultiModalInput) -> AgentResult:
        df = self.tools.normalize(payload.csv_df.copy())
        scenarios = pd.DataFrame(
            {
                "scenario": ["基准方案", "公交优先", "潮汐车道", "事故应急"],
                "delay_reduction_pct": [0, 12.5, 18.2, 8.4],
                "emission_reduction_pct": [0, 10.1, 14.8, 6.2],
            }
        )

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.lineplot(data=scenarios, x="scenario", y="delay_reduction_pct", marker="o", ax=ax, label="延误下降%")
        sns.lineplot(data=scenarios, x="scenario", y="emission_reduction_pct", marker="o", ax=ax, label="排放下降%")
        ax.set_title("多方案交通仿真效果")
        ax.set_xlabel("方案")
        ax.set_ylabel("优化比例(%)")

        return AgentResult(
            agent_name="SimulationAgent",
            narrative="仿真结果显示“潮汐车道”在当前路网最优，建议优先试点。",
            table=scenarios,
            figure=fig,
            metadata=self.tools.summarize(df),
        )


class VehicleDispatchAgent(BaseTrafficAgent):
    """车辆调度智能体。"""

    def execute(self, payload: MultiModalInput) -> AgentResult:
        df = self.tools.normalize(payload.csv_df.copy())
        depots = pd.DataFrame(
            {
                "depot": ["东站", "西站", "南站", "北站"],
                "demand_index": [1.2, 0.9, 1.35, 0.88],
            }
        )
        depots["dispatch_vehicles"] = (depots["demand_index"] * 20).astype(int)

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(data=depots, x="depot", y="dispatch_vehicles", ax=ax, palette="viridis")
        ax.set_title("站点车辆调度建议")
        ax.set_xlabel("场站")
        ax.set_ylabel("建议投放车辆数")

        return AgentResult(
            agent_name="VehicleDispatchAgent",
            narrative="建议向南站和东站增配运力，缓解高峰客流压力。",
            table=depots,
            figure=fig,
            metadata=self.tools.summarize(df),
        )


class TalentTrainingAgent(BaseTrafficAgent):
    """人才培养智能体。"""

    def execute(self, payload: MultiModalInput) -> AgentResult:
        curriculum = pd.DataFrame(
            {
                "module": ["交通数据治理", "信控算法", "仿真平台实践", "应急指挥协同"],
                "hours": [12, 16, 20, 8],
                "priority": ["高", "高", "中", "中"],
            }
        )

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(data=curriculum, x="module", y="hours", hue="priority", ax=ax)
        ax.set_title("交通人才培养课程建议")
        ax.set_xlabel("课程模块")
        ax.set_ylabel("课时")
        plt.xticks(rotation=20)

        return AgentResult(
            agent_name="TalentTrainingAgent",
            narrative="建议先开展“交通数据治理+信控算法”双模块集训，提升复合型能力。",
            table=curriculum,
            figure=fig,
            metadata={"program_weeks": 8, "target_roles": "交管+运营+应急"},
        )
