#!/usr/bin/env python3
"""Benchmark GARGANTUA.html under CPU throttling (software WebGL, worst case).

Grounds the numbers published in docs/WARNINGS.md §3. The engine file is opened
read-only; nothing is modified.

Usage:
    pip install playwright && playwright install chromium
    python3 perf_harness.py [case-index ...]     # e.g. `0 2 3`; default: all cases

Outputs bench_results.json next to this script (incremental, per case)."""
import json, os, sys, time
from playwright.sync_api import sync_playwright

_HERE = os.path.dirname(os.path.abspath(__file__))
HTML = "file://" + os.path.join(_HERE, "..", "GARGANTUA.html")
OUT_JSON = os.path.join(_HERE, "bench_results.json")
# exact args proven to boot WebGL in this sandbox (from the earlier capture sessions)
ARGS = ["--enable-unsafe-swiftshader", "--use-angle=swiftshader",
        "--disable-gpu-sandbox", "--enable-webgl", "--ignore-gpu-blocklist"]

# (label, cpu_throttle, viewport w x h, device_scale_factor, q_param)
# Small canvases: SwiftShader is ~50x slower than real GPUs; earlier capture
# sessions proved 832x468 q=medium completes. Relative throttled comparison is
# what matters; absolute lab numbers are labelled as software-rendered.
CASES = [
    ("capable-desktop",      1,  832, 468, 1, "medium"),  # baseline
    ("weak-laptop-4x",       4,  832, 468, 1, "medium"),  # mid/weak laptop class
    ("very-weak-desktop-8x", 8,  832, 468, 1, "medium"),  # old desktop class
    ("weak-laptop-4x-low",   4,  832, 468, 1, "low"),     # LOW-tier rescue
    ("mid-phone-6x",         6,  390, 844, 1, "medium"),  # mid-range phone canvas
    ("weak-phone-10x-low",   10, 390, 844, 1, "low"),     # weak phone, LOW tier
]

SETTLE_S, SAMPLE_S = 5, 4

import sys
SEL = [int(a) for a in sys.argv[1:]] or list(range(len(CASES)))

def run_case(pw, label, rate, w, h, dsf, q):
    browser = pw.chromium.launch(channel="chromium", headless=True, args=ARGS)
    ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=dsf)
    cdp = ctx.new_cdp_session(ctx.pages[0] if ctx.pages else ctx.new_page())
    cdp.send("Emulation.setCPUThrottlingRate", {"rate": rate})
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    url = f"{HTML}?nocine&cam=poster" + (f"&q={q}" if q else "")
    page.on("pageerror", lambda e: print("   [pageerror]", str(e)[:120], flush=True))
    page.goto(url, wait_until="domcontentloaded", timeout=240000)
    page.wait_for_function("() => window.__G && window.__G.S && window.__G.S.fpsSmooth > 0",
                           timeout=240000)
    page.wait_for_timeout(int(SETTLE_S * 1000))          # governor + bloom settle
    # independent rAF frame count over SAMPLE_S seconds
    frames = page.evaluate(f"""() => new Promise(res => {{
        let n = 0; const t0 = performance.now();
        const tick = () => {{
            n++;
            if (performance.now() - t0 < {SAMPLE_S * 1000}) requestAnimationFrame(tick);
            else res({{frames: n, ms: performance.now() - t0}});
        }};
        requestAnimationFrame(tick);
    }})""")
    state = page.evaluate("() => ({fps: window.__G.S.fpsSmooth, quality: window.__G.S.quality})")
    renderer = page.evaluate("""() => {
        const c = document.createElement('canvas');
        const gl = c.getContext('webgl2') || c.getContext('webgl');
        if (!gl) return 'no-webgl';
        const e = gl.getExtension('WEBGL_debug_renderer_info');
        return e ? gl.getParameter(e.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER);
    }""")
    raf_fps = frames["frames"] / (frames["ms"] / 1000)
    row = {"label": label, "cpu_throttle": rate, "viewport": f"{w}x{h}@{dsf}",
           "q_param": q or "(auto)", "engine_quality": state["quality"],
           "engine_fps_ema": round(state["fps"], 1),
           "raf_fps": round(raf_fps, 1),
           "gl_renderer": renderer[:70]}
    browser.close()
    return row

import os
store = {"meta": {"settle_s": SETTLE_S, "sample_s": SAMPLE_S,
                  "renderer_note": "SwiftShader (software GL) — CPU-bound, throttled via CDP"},
         "results": []}
if os.path.exists(OUT_JSON):                       # merge with previous batches
    try: store = json.load(open(OUT_JSON))
    except Exception: pass
done = {r.get("label") for r in store["results"]}

import time as _t
with sync_playwright() as pw:
    for i in SEL:
        case = CASES[i]
        if case[0] in done:
            print("skip (done):", case[0], flush=True); continue
        print(f"running [{i}]:", case[0], "...", flush=True); t0 = _t.time()
        try:
            row = run_case(pw, *case)
            store["results"].append(row)
            print(f"   OK ({_t.time()-t0:.0f}s) ->", row, flush=True)
        except Exception as ex:
            store["results"].append({"label": case[0], "error": str(ex)[:200]})
            print(f"   ERROR ({_t.time()-t0:.0f}s):", str(ex)[:200], flush=True)
        json.dump(store, open(OUT_JSON, "w"), indent=1)   # incremental save

print("\nsaved -> scripts/bench_results.json")
