# Rescue‑First A4 · ChatGPT 项目工作区

目的：在 ChatGPT Projects 内，以“首屏可用”为核心，稳定产出一页 A4 的学生讲解卡（结论→A1–A3→关键图→自查），并通过质量门（P#对齐、术语旁注、PHYS/CHEM 数值化例）。

核心文件
- ChatGPT_SOP_Min_v1.0.json：输出契约与规则（Rescue‑First / A4 限额 / 图示强制 / 精简顺序 / 质量门）
- Project_Instructions.md：项目级说明（强 System 规则与流程）
- templates/A4_Template.md：Rescue‑First 骨架（先首屏四件套，再补全）
- type_adapters.yaml：题型适配（CHOICE/BLANK/EXPERIMENT/FINAL × 学科差异）
- validators/validator.py：自动校验（首屏四件套 / A4 限额 / P#一致 / 术语旁注 / 数值化例）
- glossary/Terms_*.csv：术语→白话旁注（8–12字）
- figures/stencils/* + figures/index.json：学科×题型 → 默认图模板（SVG/ASCII）
- fewshot/*：每科×题型 1–2 份合格样例（可迭代增补）

最小流程
1) 贴题（学科/题型/难度/时间预算 + 题干/图片）
2) 先生成首屏四件套（模板：templates/A4_Template.md 顶部）
3) 运行 validators/validator.py 自检 → 不通过按指引重写
4) 生成 A4–A7、得分点清单（完整表）、B（等价且更快）、C（折叠）、回忆链、锚点、题干改写、微练
5) 复检 → 归档为 A4_{subject}_{type}_{date}.md 与 diagram.svg

