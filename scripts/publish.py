#!/usr/bin/env python3
"""用法: python scripts/publish.py <新的 herta_zh.json> [--no-push]
校验结构 -> 写 data/latest.json、data/latest.sha256、data/history/YYYYMMDD.json -> git commit/push"""
import hashlib, json, re, subprocess, sys, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODES = {"混沌回忆", "虚构叙事", "末日幻影", "异相仲裁"}
URL_RE = re.compile(r"(bilibili|youtube|youtu\.be|b23\.tv|uid|uploader)", re.I)


def validate(d):
    errs = []
    for k in ("source", "collected_at", "selection_rule", "targets"):
        if k not in d: errs.append(f"缺少顶层字段 {k}")
    t = d.get("targets")
    if not isinstance(t, list) or not t: return errs + ["targets 必须是非空列表"]
    for i, g in enumerate(t):
        for k in ("mode", "season", "stage", "category", "records"):
            if k not in g: errs.append(f"targets[{i}] 缺少 {k}")
        if g.get("mode") not in MODES: errs.append(f"targets[{i}] 未知模式 {g.get('mode')}")
        for j, r in enumerate(g.get("records") or []):
            lu = r.get("lineup")
            if not isinstance(lu, list) or not 1 <= len(lu) <= 4: errs.append(f"targets[{i}].records[{j}] lineup 异常")
            else:
                for c in lu:
                    if not isinstance(c.get("name"), str) or not isinstance(c.get("eidolon"), int) or not isinstance(c.get("superimposition"), int):
                        errs.append(f"targets[{i}].records[{j}] 角色字段异常")
            for k in ("ltd", "std", "date"):
                if k not in r: errs.append(f"targets[{i}].records[{j}] 缺少 {k}")
    body = json.dumps(d, ensure_ascii=False)
    if URL_RE.search(body.replace(d.get("source", ""), "")): errs.append("含上传者/视频链接等字段，请去除")
    return errs


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args: sys.exit(__doc__)
    d = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    errs = validate(d)
    if errs: sys.exit("校验失败:\n" + "\n".join(errs[:30]))
    raw = (json.dumps(d, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    sha = hashlib.sha256(raw).hexdigest()
    (ROOT / "data/latest.json").write_bytes(raw)
    (ROOT / "data/latest.sha256").write_text(sha + "  latest.json\n", encoding="utf-8")
    day = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).strftime("%Y%m%d")
    (ROOT / "data/history").mkdir(parents=True, exist_ok=True)
    (ROOT / f"data/history/{day}.json").write_bytes(raw)
    print("sha256", sha)
    git = lambda *a: subprocess.run(["git", "-C", str(ROOT), *a], check=True)
    git("add", "data")
    if subprocess.run(["git", "-C", str(ROOT), "diff", "--cached", "--quiet"]).returncode == 0:
        print("无变化"); return
    git("commit", "-m", f"数据更新 {day} ({d.get('collected_at','')})")
    if "--no-push" not in sys.argv: git("push")


if __name__ == "__main__":
    main()
