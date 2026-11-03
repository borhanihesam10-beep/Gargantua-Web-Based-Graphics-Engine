# 🔬 Technical Notes — Architecture, Analysis & Roadmap

An engineering deep-dive into GARGANTUA v12.1: how the single file is organized,
what the implementation does unusually well, where the honest trade-offs and rough
edges are, and where the engine should go next. Written to be read by contributors,
not to flatter the code.

```
Artifact        GARGANTUA.html — 2.2 MB, 4,864 lines, 0 external references
Composition     ~2.0 MB two base64-inlined MP3 tracks · ~660 lines CSS+HTML
                · ~4,060 lines JavaScript+GLSL (ES5-style, one IIFE, strict mode)
Surface         WebGL 2 (fallback WebGL 1), no libraries, no build, runs from file://
```

---

## 1 · Architecture map

The file is strictly sectioned with banner comments; here is the map (approximate
line numbers refer to `GARGANTUA.html`):

| Region | Lines (≈) | Contents |
|---|---|---|
| CSS + DOM | 8–784 | Spacecraft-terminal UI: HUD, deck, params console, mission ops, intro, fatal card; ARIA roles; responsive + reduced-motion paths |
| GLSL: ray kernel | 793–1152 | `RAY_FRAG` — noise/STARfield, blackbody ramp, `accAt()` (geodesic ODE), `diskCross()` (analytic plane-crossing sampling + turbulence + Doppler), march loop with ZAMO dragging, volumetric halo, debug outputs 0–9 |
| GLSL: post chain | 1154–1300 | High-pass, separable Gaussian (5 kernels), bloom composite, additive blend, temporal shutter, ACES/vignette/grain/CA composite |
| Constants & state | 1303–1497 | Quality tiers + pixel budgets, camera presets, cinematic keys, 23 parameter definitions, runtime state `S`, storage merge with clamping, URL overrides |
| WebGL engine | 1500–1678 | GL2→GL1 fallback, half-float render-target probe (with an actual render probe, not just extension checks), shader/program plumbing, fullscreen triangle, 15 render targets |
| Camera system | 1681–3507 | Exact-semantics three.js math shims (Vector3/Quaternion/Spherical/Matrix4/Plane/Ray), observer camera, **verbatim OrbitControls port** (r169-style: pointer FSM, wheel/pinch, damping, pole safety), cinematic Catmull-Rom loop, spherical-arc preset flights, manual takeover |
| Mode physics | 3509–3707 | `MODE_LOOK` tables, `kerrDerived()` (closed-form horizon/ISCO/photon orbits), mode snapshot/restore, scientific panel (DOM-diffed at 4 Hz) |
| Audio | 3720–3821 | Two embedded tracks, cinema-phase-locked main loop, fades, autoplay-blocked UX |
| HUD & mission ops | 3823–4122 | Telemetry, deck sync, toasts; objectives engine, deep-field scan report, mission log, WebAudio Quindar beeps |
| Params console | 4124–4223 | 23 live sliders, persistence, reset semantics |
| Quality & pacing | 4225–4346 | Tier system, FPS caps, opt-in resolution governor |
| Render & loop | 4348–4678 | Frame pipeline (ray → high-pass → 10 blur passes → bloom composite → blend → shutter → ACES composite), shutter weight logic, FPS EMA, governor, visibility pause |
| Boot & QA handle | 4680–4861 | URL parsing (`?mode/?spin/?q/?steps/?debug/?cam/?nocine/?ctime/?shot/?capture`), `window.__G` introspection API |

---

## 2 · What is genuinely strong

**1. Radical portability without dumbing down.**
One file, zero dependencies, offline, `file://`-bootable — yet the graphics are
competition-grade. Most "single-file demos" achieve portability by simplifying;
GARGANTUA achieves it by *inlining everything* (even two audio tracks) and writing
raw GLSL instead of depending on three.js for rendering.

**2. Physics honesty as an architecture decision.**
The Kerr quantities are closed-form (`kerrDerived()` computes horizon, Bardeen ISCO,
prograde/retrograde photon orbits), and the a = 0 baseline is *bit-exact protected* —
mode gating (`applyModePhysics()`) is built so CINEMATIC cannot drift. Telemetry and
the mission scan derive values from the live model (`scanReport()` computes shadow
diameter from b = √27·M, frame-dragging rate from the ZAMO ω at the ISCO) rather than
displaying painted strings. This is rare, and it is what makes the project credible.

**3. Iterative hardening you can audit.**
The source banner is a changelog of user-report-driven fixes (V8 → V12.1): the
anti-flicker campaign (DOM diffing at 4 Hz, debounced resize, governor hysteresis),
the no-black-flash resize refill, the shutter weight cap that prevents the lensed
ring from smearing to black during flings. Each fix is local, commented with the
motivating report, and gated so it cannot regress the baseline.

**4. A real QA harness inside a creative artifact.**
`?shot` gives a deterministic freeze-frame with a `document.title = "SHOT_OK"`
handshake; `?capture=canvas` exposes raw canvas pixels; `window.__G` exposes engine
state; `?debug=0–9` exposes raw pipeline stages. This is a full golden-image
regression rig waiting for a CI job — almost nobody ships this in a demo.

**5. Graceful degradation done properly.**
WebGL 2 → WebGL 1 fallback; half-float support is *probed by actually rendering*
into the target, not by trusting extension strings; bloom silently disables without
it; the fatal card offers REINITIALISE / LOWER QUALITY recovery paths that
themselves use the URL override system.

**6. Interaction fidelity.**
The OrbitControls port is verbatim-semantics (identical spherical reconstruction,
fixed 0.06 damping, pole-safe `makeSafe()`), so orbit/zoom/pan feel exactly like the
reference implementation — and automation hand-off (gesture cancels flight/cinema
from the *current interpolated pose*) is handled without popping.

---

## 3 · Honest weaknesses & risks

**W1 · Monolith friction (maintainability).**
~4,900 lines in one file with a strict no-dependency doctrine. The section banners
help, but there is no module boundary, no type checking, no linting, no tests in the
repo. Risk: contribution friction and regressions in a file where everything shares
one closure. *Mitigation today:* the QA hooks; *future:* optional module split that
compiles back to a single dist file.

**W2 · Kerr transport is local, not global.**
The dragging term applies the exact ZAMO angular velocity field, but the ray is still
integrated in the Schwarzschild-form ODE; photon-ring morphology at high spin is
qualitatively right, not quantitatively exact. Exact at a = 0 (and the ISCO/orbit
*formulas* are exact); approximate in between. This is the single biggest physics
upgrade available (see R1).

**W3 · Disk model simplicity.**
Flat, infinitely thin disk + volumetric halo approximation; no polarization, no
transfer functions, no self-shadowing; blackbody is a stylized ramp; Doppler is
clamped per mode for stability. Fine for the cinematic scope; a limitation for
"scientific instrument" ambitions.

**W4 · First-load weight.**
2.2 MB inline (2.0 MB of it audio) — on slow connections the HTML parse itself
carries the audio cost before any pixel. No lazy loading is possible inside the
one-file doctrine without splitting the artifact (contradiction by definition).
Mitigation if ever needed: a `?mute` build variant or a second-file distribution.

**W5 · State surface is URL+localStorage only.**
23 live parameters, but no share-a-state links (only `mode/spin/steps/cam/debug`)
and no import/export. discoverability of deep links is limited to what the docs list.

**W6 · Automation edge case (observed).**
The `?shot&capture=canvas` path calls `canvas.toDataURL()` *inside* the render
callback (frame 3). On standard desktop browsers this is valid and reliable; in some
headless/automation environments it can stall the compositor (observed during this
repo's asset production). The workaround is CDP surface capture after `SHOT_OK`.
Not a user-facing bug — but anyone building CI on the hooks should know.

**W7 · UI is English-only, uppercase-terminal style.**
No i18n layer; the aesthetic is intentional but limits reach. The docs structure
(translatable markdown) is the natural place to compensate.

**W8 · Performance ceiling on weak GPUs at high tiers.**
MAX (520 steps) is genuinely heavy; the tier/budget system and opt-in governor
contain this, but integrated-GPU users must select LOW/MEDIUM themselves (deliberate:
V12.1 removed silent downgrading on purpose, trading convenience for predictability).

---

## 4 · Roadmap (ordered by value/cost)

- **R1 · Full Kerr geodesic integration** — replace the dragging-rotation transport
  with a Kerr Hamiltonian (Boyer–Lindquist or Kerr–Schild) integrator behind the same
  uniform surface; keep a = 0 bit-exactness as the regression gate. Biggest physics
  leap, contained blast radius.
- **R2 · CI golden-image harness** — the hooks already exist: a Playwright job
  loading `?shot&nocine&cam=<preset>&q=medium` per mode, comparing perceptual hashes
  against golden PNGs. Turns "did the baseline drift?" into a red/green checkbox.
- **R3 · Shareable state** — serialize the full 23-parameter state into a compact URL
  hash (`#p=…`), with import/export buttons in the console.
- **R4 · Optional modular build** — split into ES modules + a Vite build whose dist
  is the same single file; canonical artifact unchanged, developer experience fixed.
- **R5 · WebGPU path** — compute-shader geodesics (higher-order integration, more
  steps per ms) with the GLSL path kept as fallback.
- **R6 · Disk realism** — vertical structure, self-shadowing, polarization;
  optional physically-based starlight aberration/redshift.
- **R7 · i18n of the HUD** — string table + `?lang=`; docs already separate.

---

## 5 · Reproducibility notes for this repository's assets

All screenshots and GIFs in `assets/` were produced by the engine's own deterministic
harness (no external renderer, no mocked frames):

```text
stills:  GARGANTUA.html?shot&nocine&cam=<preset>&mode=<mode>&q=medium   (4-frame freeze)
GIFs:    live capture at 480×270, q=low, camera driven through the exposed
         window.__G flight API; frames encoded with ffmpeg palettegen/paletteuse
```

The gallery in the README is therefore exactly what the engine produces — a claim
that itself is checkable with the commands above.
