#!/usr/bin/env python3
"""
📚 学习日志生成器 — 考研复试准备工具
用法:
  python loggen.py                     交互模式，生成今日日志
  python loggen.py --date 2026-08-03   指定日期
  python loggen.py --week              生成本周周报
  python loggen.py --month             生成本月月报
  python loggen.py --stats             查看学习统计
"""

import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path

# ── 配置 ────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent.parent
DAILY_DIR = ROOT / "daily"
TEMPLATE_FILE = Path(__file__).resolve().parent / "template.md"

# ── 统计工具 ─────────────────────────────────────────
def parse_minutes(text: str) -> int:
    """从文本中解析学习时长（支持 h/m 格式）"""
    total = 0
    h_match = re.search(r'(\d+)\s*h', text)
    m_match = re.search(r'(\d+)\s*m', text)
    if h_match:
        total += int(h_match.group(1)) * 60
    if m_match:
        total += int(m_match.group(1))
    return total if total > 0 else None


def load_logs(year: int = None, month: int = None) -> dict:
    """加载指定月份的日志"""
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month
    month_dir = DAILY_DIR / str(year) / f"{month:02d}"
    if not month_dir.exists():
        return {}
    logs = {}
    for f in sorted(month_dir.glob("*.md")):
        content = f.read_text(encoding="utf-8")
        logs[f.stem] = content
    return logs


def get_stats(days: int = 30):
    """获取最近 N 天的学习统计"""
    today = datetime.now()
    total_minutes = 0
    active_days = 0
    subjects = {}
    daily_data = []

    for i in range(days):
        d = today - timedelta(days=i)
        date_str = d.strftime("%m-%d")
        file_path = DAILY_DIR / str(d.year) / f"{d.month:02d}" / f"{date_str}.md"
        if file_path.exists():
            content = file_path.read_text(encoding="utf-8")
            mins = parse_minutes(content)
            if mins and mins > 0:
                total_minutes += mins
                active_days += 1
                daily_data.append((date_str, mins))

            # 统计科目
            for subj in ["数据结构", "操作系统", "计算机网络", "计算机组成", "数据库", "算法", "项目开发", "英语", "数学"]:
                if subj in content:
                    subjects[subj] = subjects.get(subj, 0) + 1

    return {
        "total_hours": round(total_minutes / 60, 1),
        "active_days": active_days,
        "avg_per_day": round(total_minutes / max(active_days, 1) / 60, 1),
        "subjects": dict(sorted(subjects.items(), key=lambda x: -x[1])),
        "daily": daily_data,
    }


# ── 日志生成 ─────────────────────────────────────────
def generate_daily(date_str: str = None):
    """生成每日学习日志"""
    if date_str is None:
        target = datetime.now()
    else:
        target = datetime.strptime(date_str, "%Y-%m-%d")

    date_key = target.strftime("%m-%d")
    year = target.strftime("%Y")
    month = target.strftime("%m")
    full_date = target.strftime("%Y-%m-%d")
    weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][target.weekday()]

    # 确保目录存在
    month_dir = DAILY_DIR / year / month
    month_dir.mkdir(parents=True, exist_ok=True)

    file_path = month_dir / f"{date_key}.md"

    # 如果文件已存在，就不再覆盖
    if file_path.exists():
        print(f"⚠️  {full_date} 的日志已存在: {file_path}")
        print("内容预览:")
        print(file_path.read_text(encoding="utf-8")[:500])
        return str(file_path)

    content = f"""# 📅 {full_date} ({weekday})

## ⏱️ 今日学习时长

> 总计: __h __m

## 📖 今日学习内容

### 数据结构
-

### 操作系统
-

### 计算机网络
-

### 计算机组成原理
-

### 数据库
-

## 💻 项目进展

### learning-log（学习日志生成器）
- 进度:
- 收获:

## ✍️ 今日总结

> 今天学到了什么？有什么难点需要回顾？

## 📌 明日计划

- [ ]
- [ ]
- [ ]

---
*记录于 {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    file_path.write_text(content, encoding="utf-8")
    print(f"✅ 日志已生成: {file_path}")
    print(f"📝 请编辑此文件，填入今日学习内容")
    return str(file_path)


def generate_week():
    """生成本周周报"""
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())

    print(f"\\n{'='*50}")
    print(f"📊 本周周报 ({monday.strftime('%m.%d')} - {(monday + timedelta(days=6)).strftime('%m.%d')})")
    print(f"{'='*50}")

    daily_stats = []
    total_mins = 0
    for i in range(7):
        d = monday + timedelta(days=i)
        date_str = d.strftime("%m-%d")
        file_path = DAILY_DIR / str(d.year) / f"{d.month:02d}" / f"{date_str}.md"
        if file_path.exists():
            content = file_path.read_text(encoding="utf-8")
            mins = parse_minutes(content)
            if mins:
                total_mins += mins
                daily_stats.append((d.strftime("%m-%d %a"), mins))
            else:
                daily_stats.append((d.strftime("%m-%d %a"), 0))
        else:
            daily_stats.append((d.strftime("%m-%d %a"), 0))

    for day, mins in daily_stats:
        bar = "█" * (mins // 30) + "░" * max(0, 10 - mins // 30)
        status = "✅" if mins > 0 else "❌"
        print(f"  {status} {day}: {bar} {mins}分钟")

    print(f"\\n  总计: {round(total_mins / 60, 1)} 小时")
    print(f"  日均: {round(total_mins / 420, 1)} 小时")


def generate_month():
    """生成本月月报"""
    today = datetime.now()
    stats = get_stats(today.day)

    print(f"\\n{'='*50}")
    print(f"📊 {today.strftime('%Y年%m月')} 月报")
    print(f"{'='*50}")

    print(f"\\n📈 学习概览:")
    print(f"  总时长: {stats['total_hours']} 小时")
    print(f"  活跃天数: {stats['active_days']}/{today.day} 天")
    print(f"  日均学习: {stats['avg_per_day']} 小时/天")

    print(f"\\n📚 科目分布:")
    for subj, count in stats["subjects"].items():
        bar = "█" * count
        print(f"  {subj}: {bar} ({count}天)")

    print(f"\\n🗓️ 每日趋势:")
    for date_str, mins in stats["daily"]:
        h = round(mins / 60, 1)
        bar = "█" * int(h * 2)
        print(f"  {date_str}: {bar} {h}h")


# ── 主入口 ─────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser(description="📚 考研复试学习日志生成器")
    parser.add_argument("--date", help="指定日期 (YYYY-MM-DD)")
    parser.add_argument("--week", action="store_true", help="生成本周周报")
    parser.add_argument("--month", action="store_true", help="生成本月月报")
    parser.add_argument("--stats", action="store_true", help="查看学习统计")
    parser.add_argument("--push", action="store_true", help="生成日志后 commit + push")

    args = parser.parse_args()

    if args.week:
        generate_week()
    elif args.month:
        generate_month()
    elif args.stats:
        stats = get_stats()
        print(f"\\n📊 近30天学习统计:")
        print(f"  总时长: {stats['total_hours']} 小时")
        print(f"  活跃天数: {stats['active_days']}")
        print(f"  日均: {stats['avg_per_day']} 小时")
        print(f"  科目分布: {stats['subjects']}")
    else:
        path = generate_daily(args.date)
        if args.push and path:
            print("\\n🚀 已生成日志，请编辑后手动 commit & push:")
            print(f"  cd {ROOT}")
            print(f"  git add . && git commit -m '📝 更新学习日志 {args.date or datetime.now().strftime('%Y-%m-%d')}'")
            print(f"  git push")


if __name__ == "__main__":
    main()
