# ⚠️ Performance warnings & device requirements

> **TL;DR** — GARGANTUA is a **GPU-bound physics renderer**: it integrates a relativistic
> geodesic ODE *per pixel, per frame*. It is built for **mid-to-high-end desktops**.
> It will **not** run on browsers without hardware acceleration (measured: < 0.2 fps),
> and on budget or mid-range phones it will fall far below interactive rates.
> The project home page (`index.html`) runs a quick local device check and shows this
> warning automatically before the engine starts.

---

## 1. Who should (and should not) run it

| Device class | Verdict | What to expect |
|---|---|---|
| Desktop, discrete GPU (GTX 1050 / RX 560 or better) | ✅ **Designed for this** | MEDIUM → MAX tiers, full frame rate |
| Desktop, modern integrated GPU (Intel Iris Xe, AMD 680M) | 🟡 Works | LOW → MEDIUM tiers, 30–60 fps |
| Desktop, old integrated GPU (Intel HD 4000–UHD 630) | 🟠 Marginal | LOW tier only, reduced window size |
| Desktop/laptop **without GPU acceleration** (drivers off, VM, remote desktop) | ❌ **Do not run** | Measured **< 0.2 fps** — a still image |
| Flagship phone/tablet (8 GB+ RAM, flagship GPU, ~2020+) | 🟡 Works | LOW tier, short sessions, gets warm |
| Mid-range phone | 🟠 Marginal | LOW tier, below 30 fps at full screen |
| Budget phone / phone in a low-power mode | ❌ **Do not run** | Far below interactive rates, heat, battery drain |

The engine never *lies* about quality — the tier you pick is never silently lowered — but
an underpowered device will simply deliver the frames it can. This page exists so you find
out **before** you blame your browser.

---

## 2. Why it is heavy — the actual cost model

Rendering cost ≈ **pixels × geodesic steps × post effects**, every single frame:

| Quality tier | Geodesic steps / ray | Pixel budget | Per-frame pixel-work (≈ steps × MP) |
|---|---|---|---|
| 🟢 LOW | 90 | 0.9 MP | ~81 units |
| 🟢 MEDIUM | 170 | 1.6 MP | ~272 units |
| 🟡 HIGH | 260 | 2.4 MP | ~624 units |
| 🟠 EXTRA | 380 | 3.2 MP | ~1,216 units |
| 🔴 MAX | 520 | 4.8 MP | ~2,496 units |

Going LOW → MAX is a **~30× increase in per-frame GPU work**, before counting the
5-mip HDR bloom chain that runs at every tier. There is no asset to stream and no
frame to reuse — *every* frame re-integrates every ray from scratch. That is the price
of physically-computed lensing, and it is paid by the GPU alone; a weak GPU cannot be
compensated by a strong CPU.

---

## 3. Measured reference data (lab)

To ground these warnings in numbers rather than vibes, the engine was benchmarked in a
**CPU-only software-rendering environment** (headless Chromium, ANGLE/SwiftShader — the
exact path a device takes when no real GPU driver is available). CPU throttling via the
Chrome DevTools Protocol emulates slower hardware:

| Scenario | Canvas | Tier | Measured frame rate |
|---|---|---|---|
| Baseline, software WebGL | 832×468 | MEDIUM | **< 0.1 fps** (~1 frame per 10 s) |
| + 4× CPU throttled (weak laptop class) | 832×468 | MEDIUM | **< 0.1 fps** |
| Baseline, software WebGL | 832×468 | LOW | **0.2 fps** |
| Baseline, software WebGL | 240×135 | LOW | **1.4 fps** |

**Reading the table**

- With **no hardware GPU, the engine is unplayable at every tier** — even the cheapest
  tier in a tiny window. If your browser reports software rendering, this page will
  block entry with a clear message instead of wasting your time.
- Frame cost scales with pixels × steps: cutting the canvas from 832×468 to 240×135
  (~11× fewer pixels) sped the LOW tier up ~7×. This is why the LOW tier pairs a small
  pixel budget with only 90 steps, and why shrinking the window helps so much on
  marginal devices.
- Methodology: settle 5 s, sample ≥ 4 s of `requestAnimationFrame` frames plus the
  engine's own EMA FPS counter (`window.__G.S.fpsSmooth`); boot `?nocine&cam=poster`.
  The exact harness is committed at **[`benchmarks/perf_harness.py`](../benchmarks/perf_harness.py)**
  (Playwright + CDP CPU throttling), so the numbers are reproducible, not anecdotal.

> **Honesty note:** real GPUs are hardware-accelerated and are **orders of magnitude**
> faster than this lab — do not read "0.2 fps" as "my RTX 3060 will get 0.2 fps".
> The lab reproduces the *worst case* (software rendering) and the *relative* scaling
> between tiers and resolutions. The device-class table in §1 is guidance informed by
> the cost model in §2 and the lab data in §3, not a substitute for trying it.

---

## 4. Making it lighter — in order of effect

1. **Enter with the LOW preset** — the device-check page offers this button; it is
   `GARGANTUA.html?q=low`.
2. **Shrink the window** — halving width quarters the pixel count (cost is quadratic).
3. **Lower geodesic steps** — press `P` → *Geodesic steps* → 60–90. The photon ring
   thins slightly; the physics stays real.
4. **FPS target 60** — press `F` to cap pacing (no quality loss, less heat).
5. **Disable HUD** — press `H` (the 4 Hz DOM telemetry refresh costs CPU on weak machines).
6. Full tuning guide, per-hardware advice and troubleshooting:
   **[`docs/PERFORMANCE.md`](PERFORMANCE.md)**.

---

## 5. About the automatic device check

The project home page (`index.html`) runs a **local, private** check before the engine
boots. It looks at: the WebGL renderer string (real GPU vs software), `navigator.deviceMemory`,
`navigator.hardwareConcurrency`, and coarse device class. Three outcomes:

- **PASSED** → auto-continues into the engine after a 3-second countdown.
- **WEAK DEVICE** → you must click an explicit button; the recommended path pre-sets the
  LOW quality tier via `?q=low`.
- **CANNOT RUN** (software rendering / no WebGL) → entry is refused with an explanation,
  because it was measured to be a still image.

**Bypasses**, for people who know what they are doing: append `?skip` to the home page
URL, or open `GARGANTUA.html` directly — the engine itself is never modified by the check
and contains no gating of its own. The check stores nothing outside `sessionStorage`
(one flag, cleared when the tab closes) and sends nothing anywhere.

---

*Questions about a specific device? Open an issue with your GPU string
(`chrome://gpu` → GL_RENDERER), browser, and the tier you tried.*
