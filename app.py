from __future__ import annotations

import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from xtrail_traffic_model.core.service import XTrailService

st.set_page_config(page_title="行之 X-TRAIL 智慧交通大模型", layout="wide")

st.title("🚦 行之 X-TRAIL 智慧交通大模型")
st.caption("多模态交互 + 智能路由调度 + 多智能体协同")

service = XTrailService()

with st.sidebar:
    st.header("输入层（多模态）")
    text_input = st.text_area("文本输入", value="请给出主干道晚高峰信号配时建议")
    audio_file = st.file_uploader("语音文件（wav/txt）", type=["wav", "txt"])
    csv_file = st.file_uploader("交通 CSV 文件", type=["csv"])

run_btn = st.button("运行 X-TRAIL", type="primary")

if run_btn:
    temp_audio_path = None
    temp_csv_path = None

    if audio_file:
        suffix = Path(audio_file.name).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as fp:
            fp.write(audio_file.read())
            temp_audio_path = fp.name

    if csv_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as fp:
            fp.write(csv_file.read())
            temp_csv_path = fp.name

    output = service.handle(text=text_input, audio_path=temp_audio_path, csv_path=temp_csv_path)

    st.subheader("核心后端输出")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**意图解析**: `{output.intent}`")
        st.markdown(f"**智能路由**: `{output.route}`")
        st.success(output.summary)
    with col2:
        st.info(output.result.narrative)
        st.json(output.result.metadata)

    st.subheader("输出层（文本 + 表格 + 图表）")
    st.dataframe(output.result.table, use_container_width=True)
    if output.result.figure:
        st.pyplot(output.result.figure, use_container_width=True)

    if csv_file:
        st.subheader("上传原始数据预览")
        raw_df = pd.read_csv(temp_csv_path)
        st.dataframe(raw_df.head(10), use_container_width=True)
