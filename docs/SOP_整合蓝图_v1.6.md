# SOP 整合蓝图 v1.6（三视角对齐）

目的：将你一个月高强度迭代成果沉淀为“单一事实源（SSOT）→ 路由 → 渲染 → 检查/交付”的稳定产线，统一命题专家、满分教练与错题学生三视角的意图与约束。

—

一、整合目标（Intent）
- 单一事实源：以 SSOT 为唯一事实，其它模块仅消费，不改写核心结论与推导。
- 三解一致：A/B/C 方案可复制、可验证、可审计，严格对齐评分点与真题锚点。
- 两轮输出：Round1（B/C 极简，限额）→ Round2（RCI 完整逐步）。
- 考纲锁 + 效率优先：越纲即替换/回退；在校解内实现步数/运算/时间/风险优势。
- 锚点刚性：每方法≥1、全局≥2、近5年≥50%；缺失则占位并标注“待补”。

—

二、三视角意图（Roles → Constraints）
1) 高考出题专家（命题意图与评分）
- 步骤↔评分点一一映射；“不得合并/省略评分关键步”。
- 真题锚点字段齐全（年/卷/题/科/考点）与新鲜度阈值；方法映射清晰。
- 学科硬门：
  - 数学：bridge_statement / key_criterion / 常量或索引来源 / 一处校验
  - 物理：受力/图示指令 / 方程列式 / 单位量纲 / 极限检查
  - 化学：配平或 ICE / K vs Q 或 5%规则 / 单位与有效数字 / 守恒检查
  - 生物：假设与对照 / 变量界定 / 统计方法+理由 / 结论含误差

2) 高考满分教练（提分与稳态）
- 效率面板：steps/ops/time/risk 胜（或持平但更清晰）。
- B/C 门控：Chem/Bio 白名单扩展；其余默认折叠；紧急模式可简化。
- 学习负担控制：RCI 规范、每 3–4 步设检查口、正向强化、错因与自检。

3) 错题学生（修复与迁移）
- Round1“能抄能用”：B ≤5 步/≤120 字/≤3 公式；C ≤3 要点/≤90 字。
- Round2“能跟能复现”：WHY→HOW→RESULT + 等式 + 评分；逐步编号可回放。
- 迁移微练：仅给题源标签+思路标签（不贴答案全文）；附 30s 自检与常见错因。

—

三、统一架构（v1.6 Pipeline）
- SSOT Core（L1）
  - 模块：meta/parse/notation/assumptions/classification/derivation/results/validation/rubric_map/pitfalls/true_exam_anchors/methods_abc。
  - MTV 壳：meta/solve(A/B/C)/verify 作为外层包装（兼容已有 MTV_schema_v3.0）。
  - Handoff：明确“must_not_change”与渲染 section 绑定（结果、评分映射、锚点）。

- Routing（类型路由）
  - subject×question_type → route_priority（如 A>B>C）、stoploss（30/90/180s）、profile 切换。
  - 学科政策：Chem/Bio 的 B 扩展白名单；Math/Phys ABC 全开；紧急/日常档。

- Rendering（L2 学生渲染）
  - 步进格式：steps[*]={why,how,result,eq,score}；score_map 对齐 rubric。
  - 版式限额：≤1–2 页、块内 ≤7 行、平均句长 ≤22 字；高亮 KEY/RISK/CHECK/SCORE 有上限。
  - 净化：禁内部词；模块顺序与门控遵循 Output_Standard。

- Checks & Delivery（检查与交付）
  - T0–T6：解析完整、链路可逆、校验充分、评分映射、锚点充足、效率面板、学科硬门。
  - 专项：Round1_BC_Minimal、Round2_RCI、TCI/CLI/SAR/EFI/PRI、高亮覆盖。
  - 策略：失败→重写；最终回退“school_solution_refactor”；AB 内部不对学生暴露。

—

四、文件角色与当前基线（关键参考）
- SSOT 锁与质量门：SOP_SSOT_merged_LOCK_v1.5.json
- 输出与轮次管控：SOP_Output_Standard.json
- 类型路由与学生面向：SOP_TypeRouting_DSA_v4.3.2-student-max-top-tutoring.json
- 学生渲染契约：L2_Student_Renderer_v2.3.1_with_switch.json
- MTV 外壳（meta/solve/verify）：MTV_schema_v3.0.json

—

五、目录建议（非破坏性归档）
- 00-SSOT：SSOT_lock / SSOT_stable / SSOT_v1.6_skeleton
- 01-Routing：TypeRouting_* / subject_profiles
- 02-Renderer：L2_* / MD_Generation_Standard / header.yaml
- 03-Standards：Output_Standard / NoDrift / Explainer
- 90-Archive：历史版本与 zip 归档
- 99-Indexes：索引、映射、迁移记录、兼容矩阵

—

六、落地步骤（整理优先）
1) 资产索引：生成“文件→角色/版本/状态/推荐/替代关系”索引表。
2) 意图模型：用三视角写“目标-约束-成功标准”，固化 SOP_intent 1 页。
3) SSOT_v1.6 骨架：合并 MTV+SSOT_lock 字段，给出可消费 skeleton.json。
4) 路由协议：subject×question_type 决策表、B/C 白名单、紧急与 stoploss。
5) 渲染契约：对齐 L2 的 step/schema/分页/净化；定义学生/教师可见边界。
6) 检查一体化：Round1/RCI/Advanced/高亮 合并为 checks.json 统一调用。
7) 首个试点：物理（电路/受力/能量其一），按 T0–T6 自测闭环后固化流程。

—

七、对外口令（运行绑定示例）
- “按这个SOP解析 / 按SOP执行”：绑定 runtime.autorun → R1 → R2 → Checks → Deliver
- “只跑Round1 / 先出Round1”：R1 + 最小检查
- “只跑Round2 / 补全RCI”：R2 + RCI 检查

（本蓝图不移动或覆盖原文件，仅提供整合视角与执行路线。）

