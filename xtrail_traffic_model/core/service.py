from __future__ import annotations

from xtrail_traffic_model.core.client import XTrailDataClient
from xtrail_traffic_model.core.llm_core import TrafficLLMCore
from xtrail_traffic_model.core.schemas import UnifiedOutput


class XTrailService:
    """统一应用服务层。"""

    def __init__(self) -> None:
        self.client = XTrailDataClient()
        self.core = TrafficLLMCore()

    def handle(self, text: str = "", audio_path: str | None = None, csv_path: str | None = None) -> UnifiedOutput:
        payload = self.client.ingest(text=text, audio_path=audio_path, csv_path=csv_path)
        return self.core.run(payload)
