# 📚 learning-log

> 考研复试学习日志生成器 & 项目记录仓库  
> 目标院校：**北京理工大学** | 专业：**计算机科学与技术**  
> 复试时间：2027年3-4月

---

## 🎯 复试准备路线图

| 阶段 | 项目 | 技术栈 | 状态 |
|------|------|--------|------|
| 1 | 学习日志生成器 | Python CLI + GitHub API | 🚧 进行中 |
| 2 | HTTP 服务器 | C socket 编程 | ⏳ 计划中 |
| 3 | 分布式 KV 存储引擎 | Python + Raft 协议 | ⏳ 计划中 |
| 4 | Mini SQL 解释器 | Python + 编译原理 | ⏳ 计划中 |
| 5 | 计算机视觉实战 | Python + PyTorch/OpenCV | ⏳ 计划中 |
| 6 | 个人技术博客 | Next.js 全栈 | ⏳ 计划中 |

## 🗂️ 目录结构

```
learning-log/
├── README.md                 # 项目总览
├── daily/                    # 📅 每日学习记录
│   ├── 2026/
│   │   ├── 08/
│   │   │   ├── 08-03.md
│   │   │   └── ...
│   │   └── ...
│   └── README.md
├── projects/                 # 💻 项目代码（submodule 或引用）
│   └── README.md
├── notes/                    # 📝 学科复习笔记
│   ├── data-structure/       # 数据结构
│   ├── os/                   # 操作系统
│   ├── network/              # 计算机网络
│   ├── composition/          # 计算机组成原理
│   └── db/                   # 数据库
├── tools/                    # 🔧 学习工具脚本
│   └── loggen/              # 日志生成器源码
│       ├── loggen.py
│       └── template.md
└── papers/                   # 📄 论文阅读笔记
    └── cv/                   # 计算机视觉
```

## ✨ 日志生成器功能

- 📝 交互式/命令行生成每日学习 Markdown 日志
- 📊 统计学习时长和任务完成度
- 🔗 一键 Git commit + push
- 📈 生成周报/月报总结

## 🗓️ 每日记录

查看 [daily/](daily/) 目录获取每日学习记录。
