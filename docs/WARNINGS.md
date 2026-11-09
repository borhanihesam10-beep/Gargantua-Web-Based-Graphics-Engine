# ℹ️ Performance notes

GARGANTUA is a physically-based WebGL renderer: it computes gravitational lensing in
real time on your **GPU**, entirely in the browser. There is nothing to install — it
runs like any other modern 3D web application.

## Requirements

- A browser with **WebGL** — all modern browsers (Chrome, Edge, Firefox, Safari) include it.
- **Hardware acceleration enabled** — this is ON by default on virtually every normal
  desktop and laptop. Only VMs, remote-desktop sessions or machines with disabled
  graphics drivers fall back to software rendering, where 3D content in general runs slowly.

## What to expect by device

| Device | What to expect |
|---|---|
| Desktop / laptop with hardware WebGL | Runs well. Higher quality tiers give the sharpest image. |
| Older laptop with integrated graphics | Runs; pick a lower quality tier if you want more frames per second. |
| Phone / tablet | Runs in mobile browsers; a lower quality tier keeps it smooth. |
| No WebGL / software rendering | 3D content generally won't run well — enable hardware acceleration first. |

## If the frame rate feels low

The engine already ships with **five built-in quality presets** and full manual settings —
no code changes, no extra files:

1. Open the settings panel (`P`) and choose a **lower quality preset**.
2. Reduce **geodesic steps** for extra speed — the photon ring thins slightly; the physics stays real.
3. Press `F` to cap frame pacing at 60 fps — less heat, no quality loss.
4. A smaller window renders fewer pixels — resizing gives an instant boost.

Full tuning guide: [`docs/PERFORMANCE.md`](PERFORMANCE.md).

## The home-page device check

`index.html` runs a **local, private** check before the engine starts: it confirms that
WebGL is available and whether graphics are hardware-accelerated. Nothing is uploaded,
and nothing is stored beyond a single `sessionStorage` flag. Three outcomes:

- **READY** → auto-continues into the engine after a 3-second countdown.
- **NOTE** (phone/tablet, or software rendering) → a one-line heads-up, then you decide.
- **WEBGL UNAVAILABLE** → a short explanation of how to enable it.

Bypasses, if you prefer to skip the check: append `?skip` to the home-page URL, or open
`GARGANTUA.html` directly. The engine itself is never modified by the check and contains
no gating of its own.

---

*Developers: [`benchmarks/perf_harness.py`](../benchmarks/perf_harness.py) is an optional
stress-test harness (Playwright + CPU throttling) used for regression testing. It is not
needed to run the engine.*
