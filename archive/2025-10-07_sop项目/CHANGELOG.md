# CHANGELOG · 答题SOP工程

> 维护策略：**单文件累积**（按时间倒序追加）。每次迭代把本次“修改块”直接追加到最上方即可。

---

## 2025-10-03 · v1.1 发布（解题思路图 + 学科出场矩阵）
**摘要**：
- 将“路径图”统一更名为 **“解题思路图（WHY→HOW→RESULT）”**
- 引入 **学科出场矩阵**（强约束）：数学/物理=ABC；化学=AB；生物=A
- A 方案每步增加 **“对应 HOW(k)”** 标注，强化“思路图 ↔ 步骤”对齐
- 新增 **subject_module_policy.yaml**（矩阵 require/forbid）
- 质量闸新增 **S4（学科矩阵断言）**：缺必出/出现禁用 → 自动重写
- 更新分步 Prompts：`step3_solve_A.md` / `step4_solve_B.md` / `step5_solve_C.md` 内嵌矩阵提醒
- 同步模板：`student_A4_v1.1.md` 使用“解题思路图”，并加入 HOW 对齐占位

**受影响文件**：
- `docs/SRS.md`（v1.1 约束）
- `docs/StyleGuide_Template_v1.1.md`（十模块 + 学科矩阵 + MOJI 对齐）
- `docs/Architecture_Delta_v1.1.md`（相对 v1.0 的变更）
- `project/instructions/base_instructions.md`
- `project/instructions/guardrails.md`（新增 S4）
- `project/subject_module_policy.yaml`（新增）
- `project/templates/student_A4_v1.1.md`
- `project/prompts/step3_solve_A.md`
- `project/prompts/step4_solve_B.md`
- `project/prompts/step5_solve_C.md`

**迁移指引**：
1) 将以上“受影响文件”上传覆盖项目同名文件；
2) 运行“启动自检 Prompt”（建议固定为项目置顶）；
3) 之后按 step1→step10 流程运行；若触发 S4，按提示重写。

---

## 2025-10-03 · v1.0 首发（工程化基线）
**摘要**：
- 发布完整工程：**SRS / HLD-LLD / Style Guide / Implementation Modes / QA Test Plan**
- 提供 `project/` 目录资产：**instructions / templates / glossary / scorepoints / entrypoints / prompts / inputs**
- 模板十模块（v1.0）：含“路径图（WHY→HOW→RESULT）”、A/B/C 解法、P点、易错、口诀、自测2题（含答案）
- 质量闸 S1/S2/S3：考纲术语守护 / 正确性（数值/单位/极限/边界）/ 闭环（十模块齐全、禁占位）

**受影响文件**（新增）：
- `docs/SRS.md`
- `docs/Architecture_HLD_LLD.md`
- `docs/StyleGuide_Template_v1.0.md`
- `docs/Implementation_Modes.md`
- `docs/QA_TestPlan.md`
- `project/instructions/base_instructions.md`
- `project/instructions/style_guide_v1.0.md`
- `project/instructions/guardrails.md`
- `project/templates/student_A4_v1.0.md`
- `project/glossary/syllabus_whitelist.md`
- `project/glossary/forbidden_terms.md`
- `project/scorepoints/*.md`
- `project/entrypoints/*.md`
- `project/prompts/step1_analyze.md` … `step10_qgate.md`
- `project/inputs/problem_example_*.json`

**上线指引**：
1) 将 `project/` 资产导入 ChatGPT“项目”，把 `instructions/base_instructions.md` 设为项目指令；
2) 优先使用方案A（项目化流水线）；少量临时题可用方案B（one-shot）；
3) 验收对照 `docs/QA_TestPlan.md` 的 KPI 与断言。

---

## 模板（每次追加时沿用此块的项目化说明）
- **条目格式**：日期 + 版本名 + 摘要 + 受影响文件 + 迁移/上线指引
- **禁止**：出现“占位/待补/略”等占位词；写明所有改动点，能回溯
- **建议**：重要规则用**粗体**；文件名用反引号 `code`
