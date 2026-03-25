from __future__ import annotations

from xtrail_traffic_model.core.schemas import MultiModalInput
from xtrail_traffic_model.interfaces.base_client import BaseClient
from xtrail_traffic_model.utils.io_utils import load_csv_or_sample, pseudo_transcribe


class XTrailDataClient(BaseClient):
    """BaseClient 实现：汇聚文本/语音/CSV。"""

    def ingest(self, text: str = "", audio_path: str | None = None, csv_path: str | None = None) -> MultiModalInput:
        df = load_csv_or_sample(csv_path)
        audio_text = pseudo_transcribe(audio_path)
        merged_text = "\n".join(part for part in [text.strip(), audio_text.strip()] if part)
        return MultiModalInput(text=merged_text, audio_path=audio_path, csv_df=df)
