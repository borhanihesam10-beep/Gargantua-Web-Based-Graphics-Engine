# 🕹 Controls & Interface Reference

Everything you can touch in GARGANTUA — mouse, touch, keyboard, the flight deck,
the parameters console, the HUD and the mission console.

---

## 1 · Camera (mouse & touch)

The observer camera is a verbatim-semantics OrbitControls port: damped, pole-safe,
with an orbital safety floor. If any automation (cinematic camera, preset flight) is
active, **your first gesture takes over instantly** from the current interpolated pose.

| Input | Action |
|---|---|
| Left-drag / one-finger drag | Orbit around the hole |
| Wheel / pinch | Dolly in & out |
| Right-drag / two-finger drag | Pan the orbit target |
| Middle-drag | Dolly |
| Arrow keys | Orbit / pan (keyboard pan, 7 px per tick) |

**Safety floor — 4.5 rs.** You cannot dolly closer than 4.5 Schwarzschild radii.
This is deliberate: below the photon sphere (3.0 rs) the shadow legitimately swallows
the entire sky and the screen goes physically black. Station-keeping inside the
photon sphere is not survivable — even for observers.

---

## 2 · Keyboard map

| Key | Action |
|---|---|
| <kbd>1</kbd> | **POSTER** preset — r = 24 rs, incl 38°, the classic hero framing |
| <kbd>2</kbd> | **EDGE** preset — r = 26 rs, incl 6°, near-edge-on disk |
| <kbd>3</kbd> | **POLAR** preset — r = 28 rs, incl 82°, lensed disk from above |
| <kbd>4</kbd> | **CLOSE** preset — r = 9 rs, incl 14°, close approach |
| <kbd>5</kbd>–<kbd>9</kbd> | CINEMATIC · INTERSTELLAR · REALISTIC · MISSION · HYPERREAL |
| <kbd>C</kbd> | Toggle the **cinematic camera sequence** |
| <kbd>R</kbd> | Toggle **auto-orbit** (uses ORBIT SPEED from the console) |
| <kbd>P</kbd> | Toggle the **parameters console** |
| <kbd>M</kbd> | Toggle **sound** (browser policy: click the page once first) |
| <kbd>H</kbd> | Toggle the **HUD** |
| <kbd>F</kbd> | Cycle **FPS target** NATIVE → 120 → 60 |
| <kbd>S</kbd> | **Deep-field scan** (MISSION mode only) |

All flights (presets, mode signature views) ease along a spherical arc — radius,
elevation and azimuth interpolate independently, so long hops never dive through
the shadow.

---

## 3 · The flight deck (bottom-right)

| Control | Behavior |
|---|---|
| **CINEMATIC / INTERSTELLAR / REALISTIC / MISSION / HYPERREAL** | Mode buttons — see the table in the README. Entering INTERSTELLAR or MISSION also flies you to that mode's signature view. |
| **CINE CAM** | Engages the 176 s looping cinematic spline (8 Catmull-Rom keys × 11 s). Any gesture hands control back to you. |
| **POSTER / EDGE / POLAR / CLOSE** | Preset flights (same as keys 1–4). |
| **AUTO** | Auto-orbit around the target at ORBIT SPEED. |
| **Quality button** (CINEMATIC/MEDIUM/…) | Cycles the graphics tier LOW → MEDIUM → HIGH → EXTRA → MAX → LOW. The first click from the default lands on EXTRA, never LOW. |
| **FPS: NATIVE** | Cycles NATIVE → 120 → 60. Pure pacing — skipped frames never touch simulation time. |
| **AUTO RES: OFF** | Opt-in adaptive resolution. When ON and fps stays below 32 for four confirmed windows, render scale steps down (min 62%), with 6 s spacing and a 20 s climb lockout. OFF = your tier is never touched. |
| **PARAMS** | Opens the parameters console (top-right). |
| **HUD** | Hides/shows the whole HUD for clean screenshots. |
| **🔊 SOUND: OFF** | Two embedded tracks: the intro theme, then the 176 s main loop that stays phase-locked to the cinematic clock. Browser autoplay policy: press after your first click/keypress. |

---

## 4 · HUD elements (top & bottom)

| Element | Meaning |
|---|---|
| **OBSERVER DISTANCE** | Camera radius in Schwarzschild radii (rs) |
| **DISK INCLINATION** | Your elevation above the disk plane, degrees |
| **GEODESIC STEPS** | Current integration budget per ray (tier-dependent) |
| **RENDER PROFILE** | Tier + AUTO flag + current render scale + FPS cap |
| **FRAME RATE** | 1-second-window FPS, smoothed |
| **METRIC tag** (under the title) | Active metric: `SCHWARZSCHILD` or `KERR // A/M = x // FRAME DRAGGING ACTIVE` |
| **MISSION ELAPSED** | Wall-clock mission timer |

---

## 5 · Scientific telemetry panel (bottom-left, non-cinematic modes)

Live values computed from the Kerr model and camera state — nothing is painted:

| Row | Meaning |
|---|---|
| METRIC | Active metric + spin |
| HORIZON r+ | Outer Kerr horizon in rs |
| PHOTON ORBIT | Prograde / retrograde photon-orbit radii |
| ISCO (PROGRADE) | Bardeen innermost stable circular orbit |
| ISCO ORBIT VEL | Orbital speed at the ISCO (fraction of c) |
| BEAMING | Mode's Doppler treatment |
| RANGE TO HOLE | Camera range in km and AU (for the 1.0 × 10⁸ M☉ hole, rs ≈ 2.95 × 10⁸ km) |
| SHIP CLOCK RATE | Your gravitational time dilation √(1−rs/r) vs Earth |
| TELEMETRY LINK / UPLINK / RAD FLUX / STATUS | Mission-mode rows: light-time to relay, 1/r² radiative load vs the 12 rs reference, thermal status |

---

## 6 · MISSION OPS console (MISSION mode)

- **MISSION OBJECTIVES 0/5** — computed live from your actual position:
  1. **ORBITAL SWEEP** — accumulate 360° of azimuth coverage
  2. **EQUATORIAL PASS** — inclination ≤ 10° at r ≤ 18 rs
  3. **POLAR OVERFLIGHT** — inclination ≥ 65°
  4. **CLOSE APPROACH** — r ≤ 10 rs
  5. **RING GEODESY** — run the deep scan at r ≤ 12 rs
- **NAVIGATION** — PERIAPSIS (8 rs) · OVERFLIGHT (22 rs, 78°) · FAR RELAY (60 rs)
- **◉ DEEP FIELD SCAN** (or <kbd>S</kbd>) — 3.2 s sweep, then a geodesy report in the
  mission log: shadow diameter, photon-ring diameters, ISCO radius & velocity,
  frame-dragging rate at the ISCO, Novikov–Thorne flux peak radius.
- **MISSION LOG** — timestamped T+ entries; objectives and alerts post here.

---

## 7 · Parameters console (<kbd>P</kbd>)

Every slider applies live and persists to `localStorage` (URL overrides win for the
current session; RESET restores defaults).

| Slider | Range (default) | What it does |
|---|---|---|
| GEODESIC STEPS | 60–600 (460) | Integration budget per ray — the main quality/cost dial |
| DISK INNER EDGE | 2–4 rs (2.75) | Inner cutoff; clamped to the ISCO in real-physics modes |
| DISK OUTER EDGE | 10–80 rs (40) | Outer cutoff (mode look tables re-tune this) |
| DOPPLER CAP | 1–3 (1.85) | Upper clamp on the Doppler factor |
| OPACITY NEAR / FAR | 0.5–1 / 0.3–1 | Disk opacity near vs far from the hole |
| DISK / STAR BRIGHTNESS | 0.2–3 (1.0) | Exposure of the two light sources |
| SKY FLOOR | 0–0.15 (0.04) | Deep-space ambient floor |
| DISK ROTATION | 0–3 (1.0) | Pattern advection speed |
| BLOOM STRENGTH / RADIUS / THRESHOLD | 0–1.5 / 0–1 / 0–1 | The HDR bloom stack |
| VIGNETTE | 0–1.5 (1.0) | Lens falloff |
| FILM GRAIN | 0–0.15 (0.045) | Animated grain amplitude (REALISTIC freezes it) |
| CHROMATIC ABERRATION | 0–0.01 (0.0028) | Radial channel shift |
| FIELD OF VIEW | 25–80° (44°) | Projection FOV |
| MAX DISTANCE | 40–300 rs (150) | Dolly limit |
| ORBIT SPEED | 0–1 (0.12) | Auto-orbit rate |
| CINE SEGMENT | 4–30 s (11) | Duration of each cinematic spline segment |
| KERR SPIN A/M | 0–0.9 (0) | The spin. 0.60 = the film's Gargantua |
| DOPPLER BEAMING | 0–1 (1.0) | 1.00 = full computed physics; lower = film-like symmetric glow |
| DEBUG MODE | 0–9 (0) | Raw pipeline views — see below |

### Debug views (DEBUG MODE 0–9)

| Value | View |
|---|---|
| 0 | Final image |
| 1 | Disk emission only (no background) |
| 2 | Background only (lensed starfield) |
| 3 | Geodesic-step usage heatmap |
| 4 | First disk-crossing radius (color-coded) |
| 5 | Disk turbulence field |
| 6 | Min radius / crossing count |
| 7 | Disk-crossing count classifier |
| 8 | First-crossing azimuth |
| 9 | Radius bands |

---

## 8 · URL parameters

| Param | Values | Effect |
|---|---|---|
| `mode` | `cin` `cinematic` `ist` `interstellar` `sci` `scientific` `real` `realistic` `mis` `mission` `ultra` `hyper` `hyperreal` | Boot into a mode |
| `spin` | 0 … 0.9 | Kerr spin override for this session |
| `q` | `low` `medium` `high` `extra` `max` (invalid → `high`) | Graphics tier |
| `steps` | 60 … 600 | Geodesic step override |
| `debug` | 0–9 | Debug view override |
| `cam` | `poster` `edge` `polar` `close` `ist` `mis` `mperi` `mpolar` `mrelay` | Exact camera pose (auto-orbit off) |
| `nocine` | — | Boot without the cinematic camera |
| `ctime` | seconds | Start position inside the cinematic loop |
| `shot` | — | QA freeze-frame: intro hidden, 4 frames, then `document.title = "SHOT_OK"` and `window.__SHOT_DONE = true` |
| `capture=canvas` | with `shot` | Exposes `window.__SHOT_PNG` (canvas pixels) on frame 3 |

Example — deterministic INTERSTELLAR promo pose:

```text
GARGANTUA.html?shot&nocine&cam=ist&mode=interstellar&q=high
```

---

## 9 · Storage

- `gargantua.params.v1` — your console sliders (finite values only, clamped on load)
- `gargantua.mode.v1` — last active mode
- Private-browsing storage failures degrade to a toast, never a crash.
