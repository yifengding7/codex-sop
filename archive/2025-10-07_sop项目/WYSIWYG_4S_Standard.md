# WYSIWYG‑4S v2.0 标准（数学/物理/生物/化学）
> 目标：**你在对话窗口看到的样式（标题、加粗、列表、公式、箭头、上下标、物理单位、化学方程式）== 打印出的 PDF 样式**。  
> 方法：内容一律用“可移植 Markdown（P‑MD）+ LaTeX 受限子集”，转换智能体按本标准的两条路线之一生成 PDF，并**嵌入字体**。

---

## A. 作者侧写作规则（我生成 MD 的约束）
1. **结构**：只用标准 Markdown（CommonMark）：`#`~`###` 标题、段落、`**加粗**`、_斜体_、有序/无序列表、表格、引用、代码块。
2. **数学**：LaTeX 受限子集  
   - 内联 `$ ... $`；行间 `$$ ... $$`。  
   - 允许：`frac sqrt sum int lim log ln cdot times pm mp approx propto le ge vec hat bar boldsymbol mathbb`；环境 `aligned cases matrix pmatrix bmatrix`。  
   - **不使用**：`tikz`, `pgfplots`, `chemfig`, 自定义 `\newcommand`（保证跨引擎一致）。
3. **化学**：**全部使用 `\ce{...}`（mhchem）**，含箭头/电荷/沉淀/同位素等；`-> <- <=> <=>` 与 `\xrightarrow{条件}` 皆可。  
4. **物理单位**：直接写 `$\,\mathrm{m\cdot s^{-1}}$` 这类标准 LaTeX 表达；不强制依赖 `siunitx`（为 KaTeX 兼容）。
5. **生物命名**：种名 *E. coli* 用_斜体_；基因 **斜体**（如 *lacZ*），蛋白 **正体**（LacZ）。核酸/氨基酸序列放代码块（等宽）。
6. **图像**：**SVG 首选**，PNG ≥ 300 dpi；使用相对路径 `./figures/xxx.svg`。不嵌入位图公式。
7. **字符**：全部使用 ASCII 标点（普通空格、连字符 `-`），**禁用** `U+2011` 非断行连字符、特殊空格与数学减号 `−`；用 `-` 与 `-` 组合表示范围。
8. **YAML 头**：每个 `.md` 顶部包含如下（供 Pandoc 路线使用；Node 路线会忽略不报错）：
```yaml
---
title: ""
pdf-engine: xelatex
mainfont: "Noto Serif CJK SC"
sansfont: "Noto Sans CJK SC"
monofont: "JetBrains Mono"
geometry: margin=22mm
header-includes:
  - \usepackage{xeCJK}
  - \usepackage{mhchem}
  - \usepackage{amsmath,amssymb}
---
```

---

## B. 转换智能体的**两条合格路线**（二选一）
无论采用哪条，**必须：嵌入字体（Embedded Subset）、A4、页边距 22 mm**。

### 路线 A（教材级，推荐）：Pandoc + XeLaTeX
- 读取 `.md` 的 YAML 头；自动加载 `mhchem/amsmath/xeCJK`。  
- 命令：`pandoc input.md -o output.pdf`。  
- 字体：`Noto Serif/Sans CJK` 或等价思源/本地可用字体；**嵌入**。

### 路线 B（免 TeX）：Node(md-to-pdf) + KaTeX + katex‑mhchem
- remark‑math + rehype‑katex 渲染 `$...$` 与 `\ce{...}`；  
- 注入 CSS：`katex.min.css` 与 `katex-mhchem`；  
- `pdf_options.printBackground = true`；字体指定 `"Noto Sans CJK SC","Noto Sans","DejaVu Sans",sans-serif`；**嵌入**。

---

## C. 四科“所见=所得”要点清单
- **通用**：H1/H2/H3、**加粗**、列表、表格的缩进与行距一致；禁止转换器替换字体为未嵌入的系统字体。  
- **数学**：分式、根号、向量粗体、对齐（`aligned`）、分段（`cases`）、矩阵（`bmatrix`）正确。  
- **物理**：单位处于 `\mathrm{}`；矢量符号 `\vec{E}` 或 `\boldsymbol{E}`；上下角标堆叠不错位。  
- **化学**：`$\ce{ ... }$` 中箭头、沉淀符号 `v`、电荷 `^+/^-`、同位素 `_` 正确；反应条件可用 `\xrightarrow{...}`。  
- **生物**：_斜体_ 种名与基因名保持；序列等宽；pH、pKₐ 等上下标清晰。  
- **图像**：SVG 渲染锐利；PNG ≥300 dpi；打印不糊。

---

## D. 交付包结构（建议）
```
project/
  content/
    main.md
  figures/
    mechanism.svg
  build/
    header.yaml        # Pandoc 路线复用
    md2pdf.mjs         # Node 路线
    Makefile
```

---

## E. 验收（对转换智能体/流程的硬性检查）
- [ ] PDF 属性→Fonts：所有字体均 *Embedded/Embedded Subset*。  
- [ ] 随机抽 3 处 `\ce{}` 与 3 处数学公式：箭头/上下标/电荷正确，未出现方块。  
- [ ] H1/H2/**加粗** 与窗口渲染一致；表格边距与对齐不变形。  
- [ ] 打印 A4：页边距 22 mm，跨页分割不破坏公式/图形。

---

## F. 常见翻车与规避
- **方块/烂码**：未嵌入字体或用 Base‑14 字体（Helvetica）。→ 强制嵌入 Noto/DejaVu。  
- **公式当文本**：渲染器没启用 math/mhchem。→ 路线 A/B 必须齐备。  
- **错位**：插入了奇怪的 Unicode（非断行连字符、窄空格）。→ 按规则 7 写作。

