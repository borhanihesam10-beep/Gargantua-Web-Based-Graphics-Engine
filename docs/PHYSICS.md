# 🧮 The Physics of GARGANTUA

This document describes what the renderer actually computes — the integration scheme,
the exact relativistic quantities, the disk model, the post pipeline — and, just as
importantly, the approximations it knowingly makes. "No fake physics" is a claim about
intent, and intent is only credible when the math is on the table.

**Units.** Everything is measured in Schwarzschild radii of the hole: `rs = 1`,
so the mass parameter is `M = rs/2 = 0.5`. The engine's hole is `1.0 × 10⁸ M☉`
(`rs ≈ 2.953 × 10⁸ km ≈ 1.97 AU`), which is what the km/AU telemetry uses.

---

## 1 · Light transport: null geodesics, integrated per pixel

For every pixel, a ray `(position p⃗, direction v̂)` is marched through the field with
a symplectic-flavored leapfrog scheme. In Schwarzschild spacetime the photon geodesic
can be written exactly as a central-force problem in pseudo-Newtonian form
(with `h = |p⃗ × v⃗|` the conserved specific angular momentum, `rs = 1`):

```
d²p⃗/dλ² = −(3/2) · rs · h² · p⃗ / r⁵          (accAt() in the shader)
```

This is the standard exact reduction of the Schwarzschild null geodesic
(`d²u/dφ² + u = 3Mu²` in orbital form) — not an approximation of bending "strength",
but the actual ODE whose solutions *are* the lensed photon paths. Everything iconic —
the shadow, the photon ring, the disk fold-over above and below the hole — falls out
of integrating it.

**Adaptive marching.**

- Step size `dt = max(0.012, r · mix(0.02, 0.06, smoothstep(6, 20, r)))` — fine near
  the hole, coarse in flat space.
- For `r < 4.4 rs` the integrator switches to **two RK2 sub-steps per frame step**
  (midpoint evaluation, renormalized direction) — the photon-ring region demands it.
- Escape conditions: `r < 1.03 rs` (captured — contributes blackness), or
  `r > 45 rs` moving outward (escaped → background sampled along the final direction).
- Budget: up to 600 steps (`uSteps`, tier-controlled 90–520).

**Kerr frame dragging.** With spin `a = a/M · rs` (uniform `uSpin`, scaled by 0.5 to
keep `M = 0.5 rs`), each step first rotates **both the position and the direction**
into the locally-non-rotating frame using the exact Kerr ZAMO angular velocity:

```
ω(r,θ) = 2 M a r / ( (r² + a²)² − a² Δ sin²θ ),      Δ = r² − 2Mr + a²
dφ = ω(r,θ) · dt                                     (ray advanced by dφ each step)
```

At `a = 0` this term is a bit-exact no-op — the CINEMATIC baseline renders the same
Schwarzschild integrator it was validated with. (~15 ALU ops per step, branch-guarded.)

> **Honesty note:** this transports the ray through the *exact dragging field* but is
> not a full Kerr-metric geodesic integration (no Kerr ray-tracing Hamiltonian, no
> horizon-crossing corrections). The `a → 0` limit is exact; the finite-`a` transport
> is a controlled approximation — see §6.

---

## 2 · The accretion disk

A geometrically thin, optically thick disk in the equatorial plane (`|y| < 0.45`
with exponential vertical falloff for the volumetric halo pass), sampled at every
plane crossing along the ray — crossings are detected analytically between integration
steps, and **multiple crossings accumulate** (that is how the classic "see the far side
of the disk folded over the hole" image emerges).

**Radial structure — Page & Thorne-style thin-disk flux** with the prograde ISCO:

```
F(r) ∝ (3/x)³ · (1 − √(x_isco / x)),      x = r,   x_isco = Bardeen ISCO(a)
T(r) ∝ F(r)^¼ · uTempK
```

The **Bardeen prograde ISCO** (in M units, converted to rs) is computed in closed form
from spin via Bardeen's Z₁, Z₂:

```
Z₁ = 1 + (1−a²)^(1/3) · [ (1+a)^(1/3) + (1−a)^(1/3) ]
Z₂ = √(3a² + Z₁²)
r_isco = M · [ 3 + Z₂ − √((3−Z₁)(3+Z₁+2Z₂)) ]
```

Consequences you can verify in the sim: raise the spin and the disk's inner edge
physically climbs inward toward the horizon while the inner temperature rises.

**Temperature → color** runs through a blackbody-style ramp (ember → amber → cream →
blue-white). **Pattern advection** uses the exact Kerr-equatorial orbital angular
velocity ratio (reduces identically to the Keplerian Schwarzschild value at a = 0):

```
Ω_kerr / Ω_schw = rs^(3/2) / ( rs^(3/2) + 0.35355 · a )        (a in rs units)
```

**Turbulence** is procedural fbm noise (5 octaves, warped), advected with the orbital
shear so the disk visibly streams at differential rates.

---

## 3 · Relativistic imaging terms

For each disk sample, with the ray direction `n̂` at the crossing:

- **Special-relativistic Doppler** `D = 1 / ( γ (1 − β·n̂) )`, where `β` is the exact
  Kerr prograde orbital speed factor:
  `β(r) = 0.70711 · r / ( r^1.5 + 0.35355·a )`
- **Gravitational redshift** `g = √(1 − rs/r)`
- **Combined intensity**: `I ∝ pow(D, mix(0.5, beamExp, dopExp)) · g · B(T·D·g)`

`beamExp = 3` gives the damped, film-like asymmetry; `beamExp = 4` (REALISTIC) and
`4.2` (HYPERREAL) with `dopExp = 1` give the full physical `D⁴` beaming — the reason a
real accretion disk looks dramatically brighter on the approaching side.
`D` is clamped per mode (`uDopMax` 1.85 film / 2.40 realistic / 2.60 hyperreal) to
keep the film modes renderable and stable.

**Volumetric halo.** Between plane crossings, rays accumulate a soft emissive term
near the disk (`exp(−|y|·30)` falloff, scaled by the local flux) — this produces the
luminous glow hugging the photon ring in the film-look modes (gain `uHaloBoost`).

**Photon-ring accent.** A faint analytic accent at the minimum ray radius
(`exp(−((minR − 1.55)·4)²)`) adds the razor-thin ring glint.

---

## 4 · Background sky

The starfield is procedural: four hashed star layers with distinct rotations/sizes,
a sparse "hero star" layer with bloom-ready cores, and an fbm Milky-Way band with
dust absorption. Escaped rays sample this sky along their **final bent direction** —
so the background is lensed by the same integration as the disk (Einstein-ring
smearing near the shadow comes free).

---

## 5 · Post pipeline

Rendered in HDR into a half-float target (capability-probed; bloom degrades gracefully
to LDR on hardware without it):

1. **Luminance high-pass** (threshold ~0.55, smooth width 0.01)
2. **Progressive separable Gaussian** over 5 mip levels (kernels 3, 5, 7, 9, 11)
3. **Mip composite** with per-level factors (1.0 → 0.2) and radius mirror-blend —
   the UnrealBloomPass recipe, reimplemented raw
4. **Additive blend** back over the scene
5. **Temporal shutter** — film-style motion blur: `out = mix(current, previous, k)`
   with `k = min(0.50, sweptAngle · 2.3)`; `k = 0` whenever the camera stands still
   (bit-exact static frames, deterministic QA captures)
6. **Composite**: ACES-ish tonemap, vignette, 24 fps-seeded film grain, radial
   chromatic aberration

---

## 6 · Known approximations (the honest list)

1. **Kerr transport** — the dragging term rotates the ray by the exact ZAMO ω each
   step, but the underlying integration scheme is the Schwarzschild-form geodesic ODE.
   Exact at a = 0; a controlled local approximation at finite a. A full Kerr
   Hamiltonian integration is the obvious next milestone (see TECHNICAL_NOTES roadmap).
2. **Thin disk + halo** — no vertical structure, no self-shadowing, no polarization,
   no transfer-function radiative transfer.
3. **Doppler clamp** — `uDopMax` trims the physical distribution per mode.
4. **Blackbody ramp** — a stylized 4-stop ramp, not a Planck-accurate LUT.
5. **Background stars** — lensed by direction sampling, but no relativistic
   aberration of the observer and no gravitational redshift of starlight.
6. **Telemetry simplifications** — ship clock uses the static-observer formula
   √(1−rs/r) (no orbital velocity term); radiative load is 1/r² against a 12 rs
   reference, not a transfer computation.

---

## 7 · Where these live in the code

| Piece | Where |
|---|---|
| Geodesic ODE, step control, disk crossings | `RAY_FRAG` — `accAt()`, `diskCross()`, `main()` march loop |
| ZAMO dragging | `RAY_FRAG` — the `uSpin > 0.0001` block |
| ISCO / photon orbits / horizon | `kerrDerived()` in the script |
| Mode look tables (beaming, grade, temperature) | `MODE_LOOK` |
| Deep-field scan math (shadow Ø = 2·asin(√27·M / D), etc.) | `scanReport()` |
| Bloom stack | `HIGHPASS_FRAG`, `BLUR_FRAG_BODY`, `BLOOMCOMP_FRAG`, `BLEND_FRAG` |
| Shutter | `SHUTTER_FRAG` + the per-frame weight in `frame()` |
| ACES / grain / CA / vignette | `COMPOSITE_FRAG` |

## 8 · References

- Bardeen, J. M., Press, W. H., & Teukolsky, S. A. (1972) — *Rotating black holes:
  locally nonrotating frames…* — the ISCO and photon-orbit closed forms.
- Page, D. N., & Thorne, K. S. (1974) — thin accretion disk flux profile.
- James, O., von Tunzelmann, E., Franklin, P., & Thorne, K. S. (2015) — *DNGR*,
  the *Interstellar* rendering paper (the film-look modes pay homage here).
- Luminet, J.-P. (1979) — the classic analytic image of a Schwarzschild black hole.
