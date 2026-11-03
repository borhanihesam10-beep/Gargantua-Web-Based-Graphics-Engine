# 📜 Changelog

All notable engine milestones, newest first. The version trail below is the one the
engine itself carries in its source banner.

## [V12.1] — HYPERREAL

**The five-mode era.**

- ✨ New **HYPERREAL** mode (`9` / `?mode=ultra`): max-fidelity full computed physics —
  full Doppler beaming (beam exponent 4.2), hottest blue-shifted inner disk (T×1.28),
  widest disk extent (48 rs), cleanest grain.
- 🎛 Graphics tiers reorganized into five user-facing profiles **LOW / MEDIUM / HIGH /
  EXTRA / MAX** (steps 90→520, DPR caps 0.75→2.2, pixel budgets 0.9→4.8 MP).
- 🎯 **FPS target** control: NATIVE (uncapped — 120 Hz displays run at 120), 120, 60.
  Pacing only: skipped ticks never touch simulation time, and graphics are never lowered.
- 🛡 **Adaptive resolution is now OPT-IN** (`AUTO RES: OFF` by default) — the chosen
  tier is never silently degraded by itself.
- 🕳 Temporal shutter weight capped at 0.50 so the lensed ring can never smear to black
  during hard camera flings.

## [V11.3] — SHUTTER

- 🎞 Film-style **temporal motion blur**: a per-frame blend against the previously
  presented frame, weighted by swept camera angle — fast drags no longer flash across
  the empty-sky gap. Static-camera output is bit-exact unchanged (`k = 0`).

## [V11.2] — ULTRASTABLE

- 🩹 Governor hardening: 32 fps gate + four confirmed 4 s windows + 6 s minimum spacing
  between backing-store reallocations + 20 s climb lockout — no more hitch-storms on
  borderline machines, no more periodic resolution pops.

## [V11.1] — ALWAYS-FRESH

- 🩹 Hard 6 s spacing between governor resizes; each step reallocates 12 render
  targets, and back-to-back steps on weak GPUs read as freezes.

## [V11] — NO-BLACK-FLASH

- 🩹 Backing-store changes (tier change, DPR change, governor step) refill the new
  canvas bitmap from the still-intact previous scene texture *before* tearing down
  the old targets — the compositor never sees a cleared buffer.

## [V10] — ANTIFLICKER

- 🩹 Debounced window resize (a dragged preview panel used to reallocate the whole
  render-target set per event); telemetry panel switched to DOM row diffing at 4 Hz.

## [V9] — MISSION OPS

- 🛰 **MISSION mode console**: five live-computed survey objectives (orbital sweep,
  equatorial pass, polar overflight, close approach, ring geodesy), deep-field scan
  with geodesy report, navigation waypoints, mission log with MET timestamps,
  Quindar-style WebAudio beeps, thermal alerts from the live 1/r² radiative load.
- 🩹 REALISTIC grain frozen to a static dither (animated grain read as flicker).

## [V8] — QUADMODE

- 🎬 **Mode system**: CINEMATIC / INTERSTELLAR / REALISTIC / MISSION look tables,
  session-scoped so stored user parameters and the baseline stay untouched.
- 🪐 Kerr spin equips the film value a/M = 0.60 on first entry into real physics.
- 📷 Signature camera poses (`ist`, `mis`) + spherical-arc preset flights that no
  longer dive through the shadow region mid-flight.

## [V7] — TRIMODE

- 🌀 **Kerr physics**: exact ZAMO frame-dragging angular velocity per ray step,
  Bardeen prograde ISCO, prograde/retrograde photon orbits, Kerr orbital β,
  Doppler-beaming exponent mix, film grade uniforms — all collapsing to bit-exact
  no-ops at a = 0.

## [V5.5] — BASELINE

- 🕳 The original deliverable: Schwarzschild null-geodesic raytracer, volumetric
  halo, 5-mip bloom, ACES + grain + vignette + chromatic aberration, cinematic
  Catmull-Rom camera loop, verbatim-semantics OrbitControls, embedded audio.

---

<sub>Format inspired by Keep a Changelog; the engine itself is the source of truth for dates and details.</sub>
