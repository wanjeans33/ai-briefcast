# -*- coding: utf-8 -*-
import os, sys, json
from pathlib import Path
sys.path.insert(0, "scripts")
import run_daily as rd, generate_broadcast as gb

rd.load_dotenv(rd.REPO_ROOT)
os.environ["VOLC_SPEECH_RATE"] = "36"          # 1.25×（文稿标注）
spk = os.getenv("VOLC_SPEAKER2")
print(f"[spk] {spk}", flush=True)

DATE = "2026-07-05"
md_path = Path(f"output/{DATE}/scripts/broadcast-0705-B-changed.md")
segs = gb.split_segments(rd.strip_header(md_path.read_text(encoding="utf-8")))
print(f"[segs] {len(segs)} 段", flush=True)
for i, s in enumerate(segs):
    print(f"  seg{i} ({len(s)}字): {s[:26]}…", flush=True)
assert len(segs) == 7, f"期望 7 段，实际 {len(segs)} 段——检查文稿空行分段"

audio_dir = Path(f"output/{DATE}/audio"); audio_dir.mkdir(parents=True, exist_ok=True)
mp3 = audio_dir / f"broadcast-{DATE}-spacex.mp3"
log = rd.Logger(rd.REPO_ROOT / "logs" / f"run-{DATE}.log")
durs = rd.synth_single_synced(segs, mp3, log, spk)
if durs is None:
    print("[FAIL] 合成失败", flush=True); sys.exit(1)
print(f"[durs] {[round(d,1) for d in durs]}  total={sum(durs):.1f}s", flush=True)
(audio_dir / "durs.json").write_text(json.dumps(durs, ensure_ascii=False), encoding="utf-8")
print("[done]", mp3, flush=True)
