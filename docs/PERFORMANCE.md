# ⚡ Performance Guide

How GARGANTUA spends its frame budget, what each tier costs, and how to tune it
on any hardware — from an office laptop to a gaming rig.

---

## 1 · What a frame actually costs

Per frame, per pixel:

1. **The geodesic march** — up to `uSteps` integration steps (dominant cost; each
   step is ~30–50 ALU ops, more with Kerr dragging active and near-hole RK2 substeps).
2. **Bloom stack** — high-pass + 5 mip Gaussian pairs + composite + blend (half-res,
   fixed cost).
3. **Shutter + composite** — two cheap full-screen passes.

The cost scales with `pixels × steps`, which is exactly how the tier system is built:
**steps and a pixel budget per tier**, so quality scales predictably instead of
silently thrashing.

---

## 2 · The five tiers

| Tier | Geodesic steps | DPR cap | Pixel budget | Typical 1080p buffer |
|---|---|---|---|---|
| 🟢 LOW | 90 | 0.75 | 0.9 MP | ~0.5 MP (scaled) |
| 🟢 MEDIUM | 170 | 1.0 | 1.6 MP | ~1.0 MP |
| 🟡 HIGH | 260 | 1.35 | 2.4 MP | ~1.9 MP |
| 🟠 EXTRA | 380 | 1.7 | 3.2 MP | ~2.2 MP |
| 🔴 MAX | 520 | 2.2 | 4.8 MP | ~2.1–3.1 MP (budget-capped) |

- The actual buffer scale is `min(device DPR, tier DPR cap, √(budget / screen px))`,
  floored at 0.65 — a 4K screen does not explode the budget.
- The **default** profile is the engine's internal CINEMATIC baseline (460 steps,
  3.8 MP budget). Clicking the quality button once lands on **EXTRA**, never LOW —
  a first click must not tank your graphics.
- **The tier you pick is never lowered by itself.** The adaptive-resolution governor
  is strictly opt-in via `AUTO RES`.

### Choosing a tier

| Hardware | Suggested |
|---|---|
| Integrated GPU (Iris, Vega iGPU, UHD) | LOW–MEDIUM |
| Laptop dGPU (MX, 1650-class) | MEDIUM–HIGH |
| Desktop dGPU (RTX/RX class) | EXTRA–MAX |
| Phones / tablets | LOW (MEDIUM on flagships) |

View-dependent tip: near-edge-on views at CLOSE range (heavy disk traversal) cost
more than distant poster views — if a scene drops frames, one tier down usually
restores 60 fps without a visible quality change.

---

## 3 · FPS target (NATIVE / 120 / 60)

- **NATIVE** — uncapped `requestAnimationFrame`. On a 120 Hz display the engine
  genuinely renders 120 fps when the GPU allows it.
- **120 / 60** — presentation pacing: surplus rAF ticks are skipped *before any state
  mutation*, so simulation time stays exact and motion never stutters or slows.
- These caps **never** upscale or downgrade graphics — they only skip surplus ticks.

Toggle with <kbd>F</kbd> or the `FPS:` deck button.

---

## 4 · AUTO RES — the opt-in governor

When enabled (and outside CINEMATIC), a hardened governor protects the frame budget:

```
trigger:   fps < 32 sustained for 4 consecutive 4-second windows
action:    render scale −0.12 (floor 0.62) → backing store reallocates
spacing:   hard 6 s minimum between steps (reallocs hitch; storms are worse)
recovery:  fps > 66 for 3 windows → +0.08, locked out 20 s after any down-step
exit:      CINEMATIC mode or AUTO RES OFF → scale resets to 100%
```

This is deliberately conservative: on a machine hovering at ~35 fps, **nothing
happens** — the tier you chose is what you keep.

---

## 5 · Troubleshooting

### 🖤 The screen goes (almost) black
- You are probably inside ~4.5 rs looking at the shadow — the shadow legitimately
  swallows the sky. Zoom out or press <kbd>1</kbd>.
- After a tier change there is intentionally **no** black flash (the resize guard
  refills the buffer from the previous frame). If you ever see one, please report it.

### 🐌 Low FPS
- Check `RENDER PROFILE` in the HUD — if it shows `· AUTO`, the governor is active;
  turn AUTO RES OFF to lock the tier.
- Drop one tier; or halve the window size (cost scales with pixels × steps).
- On Hybrid-Graphics laptops, force the discrete GPU for the browser
  (Windows: Settings → Display → Graphics; macOS: automatic).

### 🔊 SOUND: BLOCKED
- Browser autoplay policy: interact with the page (any click/keypress) first, then
  press <kbd>M</kbd>. The engine flags blocked audio instead of failing silently.

### 📱 Mobile
- Tier LOW is selected territory; the deck and console are touch-sized (≥ 40 px
  controls below 720 px viewport width).
- iOS Safari: audio requires a gesture; performance varies strongly by device —
  LOW + 60 fps cap is the smooth combo.

### 💥 The fatal card ("SIGNAL LOST" / "SHADER FAULT")
- `REINITIALISE` reloads; `LOWER QUALITY` wipes stored settings and boots one tier
  lower via `?q=`. Shader faults on ancient drivers are the usual cause — the engine
  needs WebGL 1 with decent GLSL compiler support, WebGL 2 + half-float for the
  full pipeline.

### 🔍 Verify what the engine is doing
- `RENDER PROFILE` shows tier · AUTO · render-scale % · FPS cap live.
- `?debug=3` (geodesic-step heatmap) makes cost *visible*: bright pixels are the
  expensive ones. `window.__G.S.fpsSmooth` gives you the exact smoothed FPS.
