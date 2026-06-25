#!/usr/bin/env python3
"""Export Cursor agent transcript jsonl to readable Markdown."""
import json
import re
import sys
from pathlib import Path


def export(src: Path, out: Path, report_rel: str, session_id: str) -> int:
    lines: list[str] = []
    prompt_num = 0
    fence = "```"

    for raw in src.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        obj = json.loads(raw)
        if obj.get("type") == "turn_ended":
            continue
        role = obj.get("role")
        msg = obj.get("message", {})
        texts: list[str] = []
        for part in msg.get("content", []):
            if part.get("type") == "text":
                t = part.get("text", "")
                t = re.sub(r"<user_query>\s*", "", t)
                t = re.sub(r"\s*</user_query>", "", t)
                t = re.sub(r"\[REDACTED\]", "", t).strip()
                if t:
                    texts.append(t)
        if not texts:
            continue
        body = "\n".join(texts)
        if role == "user":
            prompt_num += 1
            lines.append(f"## Prompt {prompt_num}\n\n**User**\n\n{fence}\n{body}\n{fence}\n")
        elif role == "assistant":
            if len(body) > 4000:
                body = body[:4000] + "\n\n...(truncated)..."
            lines.append(f"**Cursor**\n\n{body}\n\n---\n")

    header = f"""# 01. Mom Test · Product Spec — Prompt Transcript

| 항목 | 내용 |
|------|------|
| 작성일 | 2026-06-25 |
| 프로젝트 | MagicSquare_1004 |
| 관련 보고서 | [{report_rel}]({report_rel}) |
| 세션 ID | {session_id} |
| 원본 JSONL | [Transcript.jsonl](./Transcript.jsonl) |

---

"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(header + "\n".join(lines), encoding="utf-8")
    return prompt_num


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "prompt/01.mom-test-product-spec/Transcript.jsonl"
    out = root / "prompt/01.mom-test-product-spec/Transcript.md"
    n = export(
        src,
        out,
        "../../report/01.mom-test-product-spec.REPORT.md",
        "a761c7b3-dc61-43db-bba8-dbb2941515d0",
    )
    print(f"exported {n} prompts -> {out}")
