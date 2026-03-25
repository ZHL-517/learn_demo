from __future__ import annotations

import os
import wave
from pathlib import Path

import numpy as np
import pandas as pd


def load_csv_or_sample(csv_path: str | None = None) -> pd.DataFrame:
    """优先加载用户 CSV，否则生成示例交通流数据。"""
    if csv_path and Path(csv_path).exists():
        return pd.read_csv(csv_path)

    hours = np.arange(0, 24)
    flow = 600 + 250 * np.sin((hours - 7) / 24 * 2 * np.pi) + np.random.randint(-40, 40, size=24)
    speed = 42 - 10 * np.sin((hours - 7) / 24 * 2 * np.pi) + np.random.uniform(-2, 2, size=24)
    queue = np.clip(30 + 20 * np.sin((hours - 8) / 24 * 2 * np.pi) + np.random.randint(-8, 8, size=24), 0, None)
    return pd.DataFrame({"hour": hours, "flow": flow.astype(int), "speed": speed.round(1), "queue": queue.astype(int)})


def pseudo_transcribe(audio_path: str | None) -> str:
    """轻量语音解析：读取 wav 基本信息并返回可用于意图判断的文本。"""
    if not audio_path:
        return ""
    if not os.path.exists(audio_path):
        return ""

    suffix = Path(audio_path).suffix.lower()
    if suffix == ".txt":
        return Path(audio_path).read_text(encoding="utf-8")

    if suffix == ".wav":
        with wave.open(audio_path, "rb") as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            duration = frames / float(rate) if rate else 0
        return f"语音请求：时长{duration:.1f}秒，疑似包含交通调度诉求"

    return f"语音文件已接收：{Path(audio_path).name}"
