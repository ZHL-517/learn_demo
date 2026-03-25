# 行之 X-TRAIL 智慧交通大模型（Vibe Coding Demo）

本项目基于“行之 X-TRAIL 智慧交通大模型架构”实现，具备：
- **输入层多模态**：文本、语音文件（wav/txt）、CSV 数据。
- **双入口交互**：Streamlit Web UI + CLI 命令行。
- **核心中枢**：意图解析 + 智能路由调度。
- **多智能体协同**：
  - 交通预测智能体
  - 信控智能体
  - 交通仿真智能体
  - 车辆调度智能体
  - 人才培养智能体
- **接口层解耦**：`BaseClient`、`AgentExecutor`、`Tools`。
- **多模态输出**：文本说明、表格数据、图像可视化图表。

---

## 1. 项目目录结构

```text
learn_demo/
├── app.py
├── cli.py
├── requirements.txt
├── README.md
└── xtrail_traffic_model/
    ├── __init__.py
    ├── agents/
    │   ├── base.py
    │   └── traffic_agents.py
    ├── core/
    │   ├── client.py
    │   ├── llm_core.py
    │   ├── schemas.py
    │   └── service.py
    ├── interfaces/
    │   ├── agent_executor.py
    │   ├── base_client.py
    │   └── tools.py
    ├── tools/
    │   └── data_tools.py
    └── utils/
        └── io_utils.py
```

---

## 2. 安装与启动

### 2.1 安装依赖

```bash
python -m venv .venv
source .venv/bin/activate   # Windows 用 .venv\Scripts\activate
pip install -r requirements.txt
```

### 2.2 启动 Web 界面（Streamlit）

```bash
streamlit run app.py
```

打开浏览器访问终端输出的本地地址即可。

### 2.3 启动 CLI 命令行

```bash
python cli.py --text "请进行晚高峰流量预测" --csv your_data.csv
```

可选参数：
- `--audio`：语音文件路径（支持 `.wav` / `.txt`）
- `--csv`：交通数据 CSV 文件
- `--save-fig`：图表保存路径

---

## 3. CSV 数据建议字段

推荐字段（至少含 `hour` 与业务字段）：
- `hour`：小时（0-23）
- `flow`：流量（车辆/小时）
- `speed`：平均速度
- `queue`：排队长度

如不传 CSV，系统会自动生成示例交通数据用于演示。

---

## 4. 架构说明（与要求映射）

1. **输入层**：`XTrailDataClient.ingest()` 聚合文本、语音、CSV。
2. **前端层**：`app.py` 提供 Web UI，`cli.py` 提供命令行交互。
3. **核心后端**：`TrafficLLMCore` 实现意图解析与智能路由。
4. **智能体层**：五类智能体在 `traffic_agents.py` 中实现。
5. **接口层**：
   - `BaseClient`：输入处理接口
   - `AgentExecutor`：智能体执行接口
   - `Tools`：工具接口
6. **输出层**：统一输出文本、表格、图表（Matplotlib/Seaborn）。

---

## 5. 注意事项

- 本项目为可运行的教学/演示版本，核心逻辑采用可解释的规则引擎 + 多智能体编排。
- 适合扩展为接入真实 ASR、交通仿真平台、信控系统与城市级数字孪生平台。
