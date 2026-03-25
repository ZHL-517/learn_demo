from __future__ import annotations

import argparse
from pathlib import Path

from xtrail_traffic_model.core.service import XTrailService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="行之 X-TRAIL 智慧交通大模型 CLI")
    parser.add_argument("--text", type=str, default="请预测今天晚高峰流量", help="文本输入")
    parser.add_argument("--audio", type=str, default=None, help="语音文件路径（支持 .wav/.txt）")
    parser.add_argument("--csv", type=str, default=None, help="交通数据 CSV 路径")
    parser.add_argument("--save-fig", type=str, default="output_chart.png", help="图表保存路径")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    service = XTrailService()
    output = service.handle(text=args.text, audio_path=args.audio, csv_path=args.csv)

    print("=" * 60)
    print("[X-TRAIL 智慧交通输出]")
    print(f"意图: {output.intent}")
    print(f"路由: {output.route}")
    print(f"总结: {output.summary}")
    print(f"智能体: {output.result.agent_name}")
    print(f"解读: {output.result.narrative}")
    print("\n[表格输出]")
    print(output.result.table.to_string(index=False))

    if output.result.figure:
        fig_path = Path(args.save_fig)
        output.result.figure.tight_layout()
        output.result.figure.savefig(fig_path, dpi=120)
        print(f"\n图表已保存到: {fig_path.resolve()}")


if __name__ == "__main__":
    main()
