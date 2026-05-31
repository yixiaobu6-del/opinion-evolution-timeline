# 观点演变时间线

追踪个人或组织的观点随时间变化的轨迹，分析转变原因和模式。

## 项目简介

人的观点不是一成不变的。随着信息的积累、经历的丰富和认知的提升，观点会逐渐演进。本工具通过时间维度记录和分析观点的变化，帮助用户理解自己或他人的思维演变过程。

## 核心功能

- **观点时间线**：可视化展示观点随时间的变化
- **转变检测**：自动识别观点转变的关键节点
- **原因分析**：分析观点转变的驱动因素
- **趋势预测**：基于历史数据预测观点的未来走向
- **报告生成**：导出完整的观点演变分析报告

## 技术架构

```
观点演变时间线/
├── data/
│   └── sample.json      # 示例数据
├── timeline.py          # 观点演变追踪框架
├── requirements.txt
└── README.md
```

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行示例

```bash
python timeline.py
```

### 使用框架

```python
from timeline import TimelineTracker

tracker = TimelineTracker("data/sample.json")

# 生成时间线
timeline = tracker.build_timeline()
tracker.visualize()

# 分析转变
changes = tracker.detect_changes()
for change in changes:
    print(f"主题: {change['topic']}")
    print(f"转变时间: {change['time']}")
    print(f"转变幅度: {change['magnitude']}")
```

## 数据格式

参考 `data/sample.json`，每条记录包含：

```json
{
  "topic": "观点主题",
  "timeline": [
    {
      "date": "2024-01-15",
      "position": 0.7,
      "statement": "具体的观点陈述",
      "context": "背景说明",
      "confidence": 0.8,
      "source": "来源说明"
    }
  ]
}
```

## 可视化示例

系统支持以下可视化输出：
- 时间线折线图：展示观点位置的连续变化
- 转变节点标注：标记观点转变的关键时间点
- 多主题对比：在同一时间轴上展示多个主题的变化

## 应用场景

- **个人复盘**：回顾自身观点的演变过程
- **行业研究**：跟踪某个领域主流观点的变化
- **竞品分析**：分析竞争对手的立场变化
- **政策追踪**：追踪政策立场的演变历史

## 许可证

MIT License