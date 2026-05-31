"""
观点演变时间线 - 观点演变追踪框架
追踪、分析和可视化观点的变化过程
"""

import json
import math
from datetime import datetime
from pathlib import Path
from typing import Optional


class TimelineTracker:
    """观点时间线追踪器"""

    def __init__(self, data_path: str):
        """
        初始化追踪器

        Args:
            data_path: 数据文件路径
        """
        self.data_path = Path(data_path)
        self.data = self._load_data()

    def _load_data(self) -> dict:
        """加载数据"""
        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_topics(self) -> list:
        """获取所有主题"""
        return [t['topic'] for t in self.data.get('topics', [])]

    def get_timeline(self, topic_name: str) -> list:
        """
        获取指定主题的时间线

        Args:
            topic_name: 主题名称

        Returns:
            时间线数据列表
        """
        for topic in self.data.get('topics', []):
            if topic['topic'] == topic_name:
                return topic['timeline']
        return []

    def build_timeline(self) -> dict:
        """
        构建完整的时间线数据

        Returns:
            {
                'topic': '主题名',
                'points': [{'date': '2024-01', 'position': 7, ...}, ...],
                'trend': '上升/下降/波动/稳定',
                'volatility': 波动率
            }
        """
        result = []

        for topic in self.data.get('topics', []):
            timeline = topic['timeline']
            # 按时间排序
            sorted_timeline = sorted(timeline, key=lambda x: x['date'])

            # 提取时间点列表
            points = [
                {
                    'date': entry['date'],
                    'position': entry['position'],
                    'statement': entry['statement'],
                    'confidence': entry.get('confidence', 5),
                    'context': entry.get('context', ''),
                    'source': entry.get('source', '')
                }
                for entry in sorted_timeline
            ]

            # 计算趋势
            trend = self._calculate_trend(points)
            volatility = self._calculate_volatility(points)
            total_shift = self._calculate_total_shift(points)

            result.append({
                'id': topic.get('id', ''),
                'topic': topic['topic'],
                'description': topic.get('description', ''),
                'tags': topic.get('tags', []),
                'points': points,
                'trend': trend,
                'volatility': round(volatility, 3),
                'total_shift': total_shift,
                'point_count': len(points),
                'date_range': {
                    'start': points[0]['date'] if points else '',
                    'end': points[-1]['date'] if points else ''
                }
            })

        return {'topics': result}

    def _calculate_trend(self, points: list) -> str:
        """计算趋势方向"""
        if len(points) < 2:
            return '稳定'

        positions = [p['position'] for p in points]
        first, last = positions[0], positions[-1]

        # 线性回归斜率
        n = len(positions)
        x_mean = (n - 1) / 2
        y_mean = sum(positions) / n

        numerator = sum((i - x_mean) * (pos - y_mean) for i, pos in enumerate(positions))
        denominator = sum((i - x_mean) ** 2 for i in range(n))

        slope = numerator / denominator if denominator != 0 else 0

        if slope > 0.3:
            return '上升'
        elif slope < -0.3:
            return '下降'
        else:
            # 检查是否大幅波动
            max_change = max(abs(positions[i] - positions[i - 1]) for i in range(1, n))
            if max_change > 3:
                return '波动'
            return '稳定'

    def _calculate_volatility(self, points: list) -> float:
        """计算波动率"""
        if len(points) < 3:
            return 0

        positions = [p['position'] for p in points]
        changes = [abs(positions[i] - positions[i - 1]) for i in range(1, len(positions))]
        return sum(changes) / len(changes)

    def _calculate_total_shift(self, points: list) -> int:
        """计算总偏移量"""
        if len(points) < 2:
            return 0
        return abs(points[-1]['position'] - points[0]['position'])

    def detect_changes(self) -> list:
        """
        检测观点转变点

        Returns:
            转变点列表
        """
        changes = []

        for topic in self.data.get('topics', []):
            timeline = topic['timeline']
            sorted_timeline = sorted(timeline, key=lambda x: x['date'])

            for i in range(1, len(sorted_timeline)):
                prev = sorted_timeline[i - 1]
                curr = sorted_timeline[i]
                shift = curr['position'] - prev['position']

                # 变化幅度超过阈值视为转变
                if abs(shift) >= 2:
                    changes.append({
                        'topic': topic['topic'],
                        'time': curr['date'],
                        'from_position': prev['position'],
                        'to_position': curr['position'],
                        'magnitude': abs(shift),
                        'direction': '正向' if shift > 0 else '负向',
                        'from_statement': prev['statement'],
                        'to_statement': curr['statement'],
                        'context': curr.get('context', ''),
                        'impact': '重大' if abs(shift) >= 3 else '中等'
                    })

        return sorted(changes, key=lambda x: x['time'])

    def get_critical_turning_points(self) -> list:
        """获取关键转折点"""
        changes = self.detect_changes()
        return [c for c in changes if c['impact'] == '重大']

    def generate_report(self) -> str:
        """生成观点演变分析报告"""
        timeline_data = self.build_timeline()
        changes = self.detect_changes()

        report = []
        report.append("=" * 60)
        report.append("观点演变时间线分析报告")
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("=" * 60)
        report.append("")

        report.append(f"共追踪 {len(timeline_data['topics'])} 个主题的观点演变")
        report.append("")

        for topic_data in timeline_data['topics']:
            report.append("-" * 50)
            report.append(f"主题: {topic_data['topic']}")
            report.append(f"  标签: {', '.join(topic_data['tags'])}")
            report.append(f"  时间跨度: {topic_data['date_range']['start']} → {topic_data['date_range']['end']}")
            report.append(f"  趋势: {topic_data['trend']}")
            report.append(f"  波动率: {topic_data['volatility']}")
            report.append(f"  总偏移量: {topic_data['total_shift']}")
            report.append(f"  记录数: {topic_data['point_count']}")
            report.append("")

            # 时间点详情
            report.append("  观点演变过程:")
            for point in topic_data['points']:
                confidence_bar = '█' * point['confidence'] + '░' * (10 - point['confidence'])
                report.append(f"    [{point['date']}] 位置: {point['position']}/10 | 确信度: {confidence_bar}")
                report.append(f"      {point['statement']}")

            # 转变检测
            topic_changes = [c for c in changes if c['topic'] == topic_data['topic']]
            if topic_changes:
                report.append(f"  关键转变: {len(topic_changes)} 次")
                for change in topic_changes:
                    report.append(f"    [{change['time']}] {change['direction']}转变 ({change['impact']})")
                    report.append(f"      从: {change['from_statement']}")
                    report.append(f"      到: {change['to_statement']}")

            report.append("")

        # 总结
        report.append("=" * 50)
        report.append("总结分析")
        report.append("=" * 50)
        report.append("")
        report.append(f"  观点转变总次数: {len(changes)}")
        report.append(f"  重大转变: {len([c for c in changes if c['impact'] == '重大'])} 次")
        report.append("")

        # 趋势分析
        upward = sum(1 for t in timeline_data['topics'] if t['trend'] == '上升')
        stable = sum(1 for t in timeline_data['topics'] if t['trend'] == '稳定')
        volatile = sum(1 for t in timeline_data['topics'] if t['trend'] == '波动')
        report.append(f"  上升趋势: {upward} 个主题")
        report.append(f"  稳定趋势: {stable} 个主题")
        report.append(f"  波动趋势: {volatile} 个主题")
        report.append("")
        report.append("=" * 60)

        return '\n'.join(report)

    def visualize(self, output_dir: str = 'output') -> None:
        """
        生成可视化HTML

        Args:
            output_dir: 输出目录
        """
        Path(output_dir).mkdir(exist_ok=True)
        timeline_data = self.build_timeline()
        changes = self.detect_changes()

        html_parts = []
        html_parts.append("""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>观点演变时间线</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-50 p-8">
            <div class="max-w-6xl mx-auto">
                <h1 class="text-3xl font-bold mb-8">观点演变时间线可视化</h1>
        """)

        for topic_data in timeline_data['topics']:
            topic_id = f"chart_{topic_data['id']}"
            dates = [p['date'] for p in topic_data['points']]
            positions = [p['position'] for p in topic_data['points']]
            statements = [p['statement'] for p in topic_data['points']]

            html_parts.append(f"""
                <div class="bg-white rounded-lg shadow mb-8 p-6">
                    <h2 class="text-xl font-bold mb-1">{topic_data['topic']}</h2>
                    <p class="text-gray-500 text-sm mb-2">趋势: {topic_data['trend']} | 波动率: {topic_data['volatility']} | 总偏移: {topic_data['total_shift']}</p>
                    <p class="text-gray-500 text-sm mb-4">{topic_data['description']}</p>
                    <div class="h-64">
                        <canvas id="{topic_id}"></canvas>
                    </div>
                    <div class="mt-4 space-y-2">
            """)

            for point in topic_data['points']:
                html_parts.append(f"""
                        <div class="text-sm p-2 bg-gray-50 rounded">
                            <span class="font-medium text-blue-600">{point['date']}</span>
                            <span class="mx-2 text-gray-400">位置:{point['position']}</span>
                            <span class="text-gray-700">{point['statement']}</span>
                        </div>
                """)

            html_parts.append("""
                    </div>
                </div>
                <script>
                """)

            html_parts.append(f"""
                new Chart(document.getElementById('{topic_id}'), {{
                    type: 'line',
                    data: {{
                        labels: {json.dumps(dates)},
                        datasets: [{{
                            label: '观点位置',
                            data: {json.dumps(positions)},
                            borderColor: 'rgb(59, 130, 246)',
                            backgroundColor: 'rgba(59, 130, 246, 0.1)',
                            fill: true,
                            tension: 0.3,
                            pointBackgroundColor: {json.dumps(positions)},
                            pointRadius: 6
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{
                                min: 0,
                                max: 10,
                                title: {{ display: true, text: '观点位置 (0=反对, 10=支持)' }}
                            }}
                        }},
                        plugins: {{
                            tooltip: {{
                                callbacks: {{
                                    afterLabel: function(context) {{
                                        return {json.dumps(statements)}[context.dataIndex];
                                    }}
                                }}
                            }}
                        }}
                    }}
                }});
                """)

            html_parts.append("""
                </script>
            """)

        # 关键转变列表
        if changes:
            html_parts.append("""
                <div class="bg-white rounded-lg shadow mb-8 p-6">
                    <h2 class="text-xl font-bold mb-4">关键观点转变</h2>
                    <table class="w-full text-sm">
                        <thead>
                            <tr class="bg-gray-100">
                                <th class="p-2 text-left">时间</th>
                                <th class="p-2 text-left">主题</th>
                                <th class="p-2 text-left">变化</th>
                                <th class="p-2 text-left">幅度</th>
                                <th class="p-2 text-left">上下文</th>
                            </tr>
                        </thead>
                        <tbody>
            """)
            for change in changes:
                html_parts.append(f"""
                            <tr class="border-t">
                                <td class="p-2">{change['time']}</td>
                                <td class="p-2 font-medium">{change['topic']}</td>
                                <td class="p-2">{change['from_position']} → {change['to_position']} ({change['direction']})</td>
                                <td class="p-2">{change['magnitude']}</td>
                                <td class="p-2 text-gray-500">{change.get('context', '')}</td>
                            </tr>
                """)
            html_parts.append("""
                        </tbody>
                    </table>
                </div>
            """)

        html_parts.append("""
            </div>
        </body>
        </html>
        """)

        output_path = Path(output_dir) / 'timeline.html'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html_parts))

        print(f"可视化已生成至: {output_path}")


if __name__ == '__main__':
    # 示例用法
    tracker = TimelineTracker('data/sample.json')

    # 生成时间线
    timeline = tracker.build_timeline()
    print(f"追踪主题: {', '.join(tracker.get_topics())}")
    print(f"主题数量: {len(timeline['topics'])}")

    # 检测转变
    changes = tracker.detect_changes()
    print(f"\n观点转变数: {len(changes)}")
    for change in changes:
        print(f"  [{change['time']}] {change['topic']}: {change['from_position']}→{change['to_position']} ({change['impact']})")

    # 生成报告
    report = tracker.generate_report()
    print(f"\n{report}")

    # 生成可视化
    tracker.visualize()