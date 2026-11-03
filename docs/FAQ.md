# ❓ FAQ

Quick answers to the questions that actually come up. Deeper material:
[Physics](PHYSICS.md) · [Performance](PERFORMANCE.md) · [Controls](CONTROLS.md) ·
[Technical notes](TECHNICAL_NOTES.md).

**Q: Is this a game?**
A: It is an engine and an instrument — a real-time relativistic raytracer with a
mission-mode overlay. There is no goal, score or ending; there is a hole, a disk,
and physics. MISSION mode adds objectives if you want one.

**Q: Does it really solve Einstein's equations? Or is it a shader trick?**
A: It integrates the exact Schwarzschild null-geodesic ODE per pixel, per frame, on
the GPU, and applies the exact Kerr frame-dragging angular velocity when spin is
active. The lensing you see is computed, not painted. The finite-spin transport is a
controlled approximation (exact at a = 0) — [PHYSICS.md §6](PHYSICS.md#6-known-approximations-the-honest-list)
lists every simplification.

**Q: Why does the disk look brighter on one side?**
A: Relativistic Doppler beaming. The side rotating toward you emits `D⁴` more light
(in the full-physics modes). In the film-look modes the effect is deliberately damped,
exactly the artistic call the *Interstellar* team made.

**Q: Why can't I zoom closer than ~4.5 rs?**
A: Safety floor. Below the photon sphere (3.0 rs) the shadow swallows the entire sky —
the view goes legitimately, physically black. The floor keeps the optics in view.

**Q: The picture flickered / resolution changed on its own — did that get fixed?**
A: Yes, twice over. The adaptive-resolution governor that could step resolution down
is now **opt-in** (AUTO RES: OFF by default), and every backing-store change refills
the new buffer from the previous frame, so tier changes never flash black. If you
ever see flicker with AUTO RES off, that is a bug — please report it.

**Q: Where are my settings stored? Will they sync?**
A: `localStorage` (`gargantua.params.v1`, `gargantua.mode.v1`), per browser. Private
windows may refuse storage — the engine degrades to a toast, never a crash. There is
no cloud sync (and no network use at all).

**Q: Does it work offline?**
A: Fully. The file ships both audio tracks embedded (that's most of the 2.2 MB).
Open it from disk, a USB stick, a plane — it is self-contained by design.

**Q: Why is the file 2.2 MB?**
A: ~2 MB of that is the two MP3 tracks, base64-inlined so the artifact stays one
file. The engine itself is ~200 KB of HTML/CSS/GLSL/JS.

**Q: Which browsers are supported?**
A: Anything with WebGL: Chrome, Edge, Firefox, Safari (desktop + mobile). WebGL 2 and
half-float render targets enable the full HDR pipeline; on older stacks the engine
falls back to WebGL 1 and disables bloom gracefully.

**Q: Is it heavy on the GPU?**
A: It can be — that is what the five tiers are for. LOW runs on integrated graphics;
MAX wants a discrete GPU. See [PERFORMANCE.md](PERFORMANCE.md).

**Q: Can I use screenshots/footage in my project?**
A: Yes — MIT licensed. Credit appreciated but not required.

**Q: Can I embed it in an iframe / my site?**
A: Yes. It is one file; iframe it or serve it as-is. Sound still needs a user gesture
in the embedding page.

**Q: How do I report a bug?**
A: Open an issue with browser/OS/GPU, tier, the exact URL you used, console output,
and a `?shot` capture if visual. The QA hooks ([CONTRIBUTING.md](../CONTRIBUTING.md))
make visuals reproducible.

**Q: Is this affiliated with the Interstellar film?**
A: No. It is an independent fan-physics homage. The INTERSTELLAR/MISSION modes recreate
the *look* (spin a/M = 0.60, damped beaming, creamy grade) with the engine's own math.
