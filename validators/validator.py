"""
Rescue‑First A4 Validator (for ChatGPT Code Interpreter)

Usage (inside Projects with Code Interpreter):
1) Provide the A4 markdown content as string to `validate(a4_md: str, subject: str, qtype: str)`
2) Or upload a4.md and run: python validators/validator.py a4.md --subject PHYS --type CHOICE

Checks:
- first_screen_quartet: 结论 + A1–A3 + 图(在 A3 后) + 自查≥3
- a4_budget: chars<=1200, equations<=12, max_lines_per_block<=7
- figure_mandatory_by_subject: subject-specific presence
- pmap_consistency: steps mention P#; 得分点清单包含相同 P# 集
- glossary: terms have 8–12 char parentheses note (heuristic)
- quantified_example: required for PHYS/CHEM (numbers+units or pH etc.)

Returns JSON-like dict with pass/fail and actionable errors.
"""

import re
import sys
import json
from typing import Dict, List, Tuple

HEADINGS = [
    "# 标题条",
    "# 结论",
    "# 具体解答（A/B/C）",
    "# 30秒自查卡",
    "# 得分点对齐清单",
]

SUBJECT_FIG_HINTS = {
    "MATH": ["号线", "函数", "几何"],
    "PHYS": ["FBD", "电路"],
    "CHEM": ["芳环", "ICE", "机理"],
    "BIO":  ["对照", "Punnett", "判别树"],
}

UNIT_TOKENS = ["m", "s", "kg", "N", "J", "V", "A", "mol", "Pa", "pH", "K"]

def section_indices(text: str) -> Dict[str, int]:
    idx = {}
    for h in HEADINGS:
        m = re.search(re.escape(h), text)
        if m: idx[h] = m.start()
    return idx

def count_equations(text: str) -> int:
    # crude: count occurrences of '=' in math-like lines
    return sum(1 for line in text.splitlines() if '=' in line and len(line.strip()) > 0)

def find_a_steps(text: str) -> List[str]:
    # extract lines that look like Step1/Step2/Step3 in A section
    a_start = re.search(r"A｜保分直推", text)
    if not a_start:
        return []
    a_text = text[a_start.start():]
    lines = [ln for ln in a_text.splitlines() if re.search(r"Step[1-7]", ln)]
    return lines

def has_first_screen_quartet(text: str, subject: str) -> Tuple[bool, List[str]]:
    errs = []
    # 结论存在
    if "# 结论" not in text:
        errs.append("缺少‘结论’段")
    # A1–A3 单行存在
    steps = find_a_steps(text)
    needed = {"Step1", "Step2", "Step3"}
    have = {s for s in [re.findall(r"Step[0-9]", ln) for ln in steps] for s in s}
    if not needed.issubset(have):
        errs.append("缺少 A1–A3 步骤或未按 Step1–3 标注")
    # 图在 A3 后：简化为存在 svg 或 ASCII 代码块指示词
    after_a3 = re.search(r"Step3[\s\S]*?(```svg|<svg|ASCII|受力图|电路|号线|芳环|ICE|Punnett)", text)
    if not after_a3:
        errs.append("缺少‘A3 后关键图’或未识别到图形占位")
    # 自查卡≥3 条
    cz = re.search(r"# 30秒自查卡[\s\S]*?\n(.*)\n(.*)\n(.*)", text)
    if not cz:
        errs.append("自查卡少于 3 条或段落缺失")
    return (len(errs) == 0, errs)

def a4_budget(text: str) -> Tuple[bool, List[str]]:
    errs = []
    chars = len(text)
    if chars > 1200:
        errs.append(f"总字数超限：{chars} > 1200")
    eqs = count_equations(text)
    if eqs > 12:
        errs.append(f"等式数超限：{eqs} > 12")
    # 粗糙块行数：检查主要块是否超过 7 行
    for h in HEADINGS:
        m = re.search(re.escape(h) + r"([\s\S]*?)(\n# |\Z)", text)
        if m:
            block = m.group(1)
            lines = [ln for ln in block.strip().splitlines() if ln.strip()]
            if len(lines) > 7 and h in ("# 结论", "# 30秒自查卡"):
                errs.append(f"{h} 段落行数超限：{len(lines)} > 7")
    return (len(errs) == 0, errs)

def figure_mandatory(text: str, subject: str) -> Tuple[bool, List[str]]:
    hints = SUBJECT_FIG_HINTS.get(subject.upper(), [])
    if not hints:
        return True, []
    if not any(h in text for h in hints) and not re.search(r"```svg|<svg", text):
        return False, [f"未检测到学科关键图（{subject}）"]
    return True, []

def pmap_consistency(text: str) -> Tuple[bool, List[str]]:
    # collect P# in A-steps and in mapping table
    p_in_steps = set(re.findall(r"P#\s*([0-9]+)", text))
    mapping_section = re.search(r"# 得分点对齐清单([\s\S]*)", text)
    p_in_table = set()
    if mapping_section:
        p_in_table = set(re.findall(r"P#\s*([0-9]+)", mapping_section.group(1)))
    missing = p_in_steps - p_in_table
    if missing:
        return False, [f"得分点清单缺少：P# {','.join(sorted(missing))}"]
    return True, []

def glossary_notes(text: str) -> Tuple[bool, List[str]]:
    # heuristic: any term-like word followed by （..8-12 chars..）
    # If there is '术语' keyword but no parentheses notes, warn.
    if "（" in text and "）" in text:
        return True, []
    # relax: only warn
    return False, ["未检测到术语旁注（8–12字），请在术语首次出现加括注"]

def quantified_example(text: str, subject: str) -> Tuple[bool, List[str]]:
    if subject.upper() not in ("PHYS", "CHEM"):
        return True, []
    # look for numeric + unit tokens
    if any(tok in text for tok in UNIT_TOKENS) and re.search(r"[0-9]", text):
        return True, []
    return False, ["缺少数值化/代入闭环示例（PHYS/CHEM 必须）"]

def validate(a4_md: str, subject: str, qtype: str) -> Dict:
    results = {}
    ok1, e1 = has_first_screen_quartet(a4_md, subject)
    ok2, e2 = a4_budget(a4_md)
    ok3, e3 = figure_mandatory(a4_md, subject)
    ok4, e4 = pmap_consistency(a4_md)
    ok5, e5 = glossary_notes(a4_md)
    ok6, e6 = quantified_example(a4_md, subject)
    passed = all([ok1, ok2, ok3, ok4, ok5, ok6])
    errors = e1 + e2 + e3 + e4 + e5 + e6
    return {"passed": passed, "errors": errors, "checks": {
        "first_screen_quartet": ok1,
        "a4_budget": ok2,
        "figure_mandatory": ok3,
        "pmap_consistency": ok4,
        "glossary_notes": ok5,
        "quantified_example": ok6,
    }}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validators/validator.py a4.md --subject PHYS --type CHOICE")
        sys.exit(1)
    md = open(sys.argv[1], 'r', encoding='utf-8').read()
    subj = "PHYS"
    qtype = "CHOICE"
    for i, arg in enumerate(sys.argv):
        if arg == "--subject" and i+1 < len(sys.argv):
            subj = sys.argv[i+1]
        if arg == "--type" and i+1 < len(sys.argv):
            qtype = sys.argv[i+1]
    print(json.dumps(validate(md, subj, qtype), ensure_ascii=False, indent=2))

