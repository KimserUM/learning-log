# learning-log

考研复试准备的仓库，记笔记和放项目代码用。

目标北理工，明年三四月复试。

## 复习科目

写了笔记的就放 notes/ 下面，目前还是空的..

- 数据结构
- 操作系统
- 计算机网络
- 计组
- 数据库

## 项目

准备了几个项目，做到哪算哪吧：

1. 学习日志工具 — 写了个python脚本，每天生成md文件记录学了啥
2. HTTP服务器 — 用C写，练习socket
3. KV存储引擎 — 用python写个分布式的，还没开工
4. Mini SQL — 想写个sql解析器，好像很难
5. CV项目 — 之前有一篇CV论文，接着做点东西
6. 个人博客 — 最后整合展示用

## 怎么用

```bash
# 生成今天的学习日志
python tools/loggen/loggen.py

# 看这周学了啥
python tools/loggen/loggen.py --week
```

daily/ 下面的日志就是每天写的，按日期放着。
