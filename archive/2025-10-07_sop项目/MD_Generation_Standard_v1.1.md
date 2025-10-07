# 《MD 生成规范（终极版）》v1.1
> 适用学科：**数学 / 物理 / 化学 / 生物**  
> 目标：**对话窗口所见 = 生成的 Markdown（MD）= 最终 PDF 打印**；零改正文、可校验、适配“快 → 稳”双渲染链。  
> 触发指令：你在对话里说 **“按标准生成 md”**，我即按本规范把当前解析 **1:1** 生成 `.md` 文件。

---

## 1. 文件结构（固定模板）
每个 `.md` 必须包含统一的 YAML 头（学生版紧凑 A4 参数）：
```yaml
---
title: "【题目名称】标准解析（学科）"
subject: 化学 | 物理 | 数学 | 生物
level: 高考
fontsize: 11pt
geometry: margin=18mm
pagestyle: empty
# 渲染链由二级系统选择：优先 KaTeX+mhchem（快），不支持即回退 Tectonic（稳）。
pdf-engine: xelatex
mainfont: "Noto Serif CJK SC"
sansfont: "Noto Sans CJK SC"
monofont: "JetBrains Mono"
header-includes:
  - \usepackage{xeCJK}
  - \usepackage[version=4]{mhchem}   # 化学 \ce{...}
  - \usepackage{amsmath,amssymb}     # 数学/物理公式
  - \usepackage{setspace}\setstretch{1.15}
assertions:
  - "官能团: 酮基"
  - "同分异构体数量: 7"
  - "NMR比例: 3:2:2:1:1:1"
  - "反应类型(D→E): 取代"
x-md-sha256: ""   # 由我生成签名时填写
---
```

正文分节（固定顺序与命名）：
```markdown
# 题目复述
# 答案一行
# 解题思路（WHY → HOW → RESULT）
# 逐问详解
# 四审自查
# 易错纠偏
# 口袋卡
# 附图（可选）
```
> 说明：四科通用骨架；具体表述按学科语境填充。

---

## 2. 书写与格式（白/黑名单）
**只使用下列“白名单”命令/环境；命中“黑名单”视为不合规。**

### ✅ 白名单（KaTeX 与 Tectonic 共同支持）
- **行内/行间**：`$ ... $`、`$$ ... $$`  
- **常用命令**：`\frac \dfrac \tfrac \sqrt \sum \int \lim \cdot \times \pm \mp \approx \propto \le \ge \vec \hat \bar \boldsymbol \mathbb \mathrm \text \left \right`  
- **环境**：`aligned cases matrix pmatrix bmatrix`  
- **化学**：**一律** `\ce{...}`（mhchem），含 `-> <- <=> \xrightarrow{...}`、电荷 `^+/-`、沉淀 `v`、同位素上下标等。

### ⛔ 黑名单（命中任一项则不合规）
```
\SI \si \qty \num \pu
\chemfig \tikz \pgf \pgfplots
\newcommand \def \renewcommand
\eqref \ref \label \cite
\footnote \begin{figure} \caption
```
> 理由：KaTeX 不支持、或涉及自定义/交叉引用/浮动体，极易改义或拖慢。

---

## 3. 单位与字符规范（避免误渲染与乱码）
- **单位**：只在数学环境中用 `\mathrm{}`，如：`$\,\mathrm{m\,s^{-2}}$`、`$\mathrm{kg\,m^{-3}}$`。  
  **禁止**：`\SI \si \qty \num \pu`。  
- **危险字符替换表（保持语义不变）**：  
  | 原字符 | 代码点 | 替换为 | 说明 |
  |---|---:|---|---|
  | − | U+2212 | `-` | 数学减号 → ASCII 减号 |
  | – — | U+2013/U+2014 | `-` | 短/长横线 → 连字符 |
  | × | U+00D7 | `\times` | 乘号 → LaTeX |
  | ± | U+00B1 | `\pm` | 正负号 → LaTeX |
  | · | U+00B7 | `\cdot` | 点乘 → LaTeX |
  | ° | U+00B0 | `\circ` | 度数符 → LaTeX |
  | µ | U+00B5 | `\mu` | 微符号 → LaTeX |
  |   | U+00A0 | 空格 | 不间断空格 → 普通空格 |
  | ‑ | U+2011 | `-` | 非断行连字符 → 连字符 |
  |   | U+2009/200A | 空格 | 窄空格 → 普通空格 |
- **括号**：数学环境仅用 ASCII `()` `[]`；**不**用全角括号。  
- **箭头**：化学反应箭头必须写在 `\ce{...}` 内（而非直接用 `→`）。

---

## 4. 文件/资源命名与路径
- **文件名/路径**：仅用 `A–Z a–z 0–9 _ - .`；不含空格、中文或外链；统一使用**相对路径**。  
- **图片**：SVG 优先（机理/图表）；PNG ≥ 300 dpi；放在 `./figures/` 目录；示例：`figures/mechanism_b2f.svg`。

---

## 5. 版式建议（作者侧，防跨页劈开）
- **行间公式**：当行内公式长度 ≥ 40 字符、或需要对齐（`aligned`）、或包含长分式时使用 `$$ ... $$`。  
- **对齐**：多步推导使用 `aligned`；长式分多行，不把超长公式塞入一行。  
- **表格/代码块**：避免在单元格内放超长公式；必要时拆为“表格 + 紧邻公式块”。列宽控制，防止跨页劈开。

---

## 6. 断言（assertions）写法（便于 PDF 文本比对）
- **只用纯文本/数字/ASCII**，**一条断言一件事实**，可直接在 PDF 文本中被定位；**不**写 LaTeX。  
- 建议 3–8 条，覆盖“关键结论/关键数值/关键关系/路线关键词”。  
- 示例：
```
官能团: 酮基
同分异构体数量: 7
NMR比例: 3:2:2:1:1:1
反应类型(D→E): 取代
路线: 脱水→断裂氧化→交叉缩合
```

---

## 7. 自动生成规则（由我执行，确保 1:1）
当你说 **“按标准生成 md”** 时，我将：  
1) 收集本次对话中的“解析正文”（你窗内所见版式）；  
2) **不改写内容**，按固定模板分节落盘；  
3) **字符安全化**（仅做等价替换：见第 3 节）；  
4) 自动提取 3–8 条断言写入 `assertions:`；  
5) 计算正文 SHA‑256 写入 `x-md-sha256`；  
6) 返回 `.md` 下载链接（必要时同时给 `.signed.md` 版）。

---

## 8. 快速合规清单（作者 10 秒自查）
- [ ] 标题/列表/表格只用 Markdown；无内联 HTML。  
- [ ] 数学 `$...$`/`$$...$$`；化学 `\ce{...}`；**无** `\SI \tikz \newcommand \eqref` 等黑名单。  
- [ ] 单位在 `\mathrm{}` 中书写；无危险 Unicode（见替换表）。  
- [ ] 图片相对路径、ASCII 文件名；SVG 或 PNG≥300dpi。  
- [ ] YAML 含 **assertions**（≥3 条，纯文本）；`x-md-sha256` 由系统写入。  
- [ ] 版式预期：A4 / 18mm / 11pt / 行距 1.15（由模板控制）。

---

（本规范只约束 **Step‑1：对话 → 标准 MD**。二级系统的预检/渲染/核对脚本另见工程包。）
