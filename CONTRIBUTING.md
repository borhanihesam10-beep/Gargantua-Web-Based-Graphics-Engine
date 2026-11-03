# 🤝 Contributing to GARGANTUA

First off — thank you for flying toward the singularity. This project has an unusual
shape (one canonical, self-contained HTML file), so read the two rules below before
opening a pull request. They keep the artifact special.

## 🧭 The two ground rules

1. **The single-file artifact is the product.** `GARGANTUA.html` must stay fully
   self-contained (no CDNs, no external fetches, works from `file://` offline).
   If your change needs a library, port the minimal semantics into the file, exactly
   like the existing OrbitControls port does.
2. **The CINEMATIC baseline is sacred.** Mode `cinematic` (spin a = 0) is the frozen
   reference look. Physics changes must be gated behind the non-cinematic modes and
   must collapse to bit-exact no-ops at a = 0 — see `applyModePhysics()`.

## 🛠 Working without a build step

There is no toolchain. Edit `GARGANTUA.html` and reload the browser tab.

- Keep the file's internal style: ES5-flavored JavaScript inside the single IIFE,
  section banner comments (`/* ==== SECTION ==== */`), no new globals
  (the only intentional leak is the `window.__G` QA handle).
- CSS lives in the one `<style>` block; GLSL lives in the string arrays at the top
  of the script. Respect the existing indent style.

## 🧪 Verify your change (the harness makes this easy)

The engine ships with deterministic QA hooks — use them instead of eyeballing:

```text
# deterministic freeze-frame (renders 4 frames, then sets document.title = "SHOT_OK")
GARGANTUA.html?shot&nocine&cam=poster&q=medium

# raw pipeline inspection (0 = final, 3 = geodesic-step heatmap, 7 = disk crossings)
GARGANTUA.html?shot&nocine&cam=edge&q=medium&debug=3

# scripted introspection in the DevTools console
window.__G.S.mode, window.__G.uniforms.uSteps.value, window.__G.camRadius(), ...
```

A PR is easy to accept when it includes:

- [ ] Before/after captures via `?shot&nocine&cam=<preset>` (attach images)
- [ ] A note on which modes were checked (`5`–`9`) and at which quality tier
- [ ] Confirmation that the `a = 0` baseline renders identically (rule 2)
- [ ] A CHANGELOG entry under a new `Unreleased` heading

## 🐞 Reporting issues

Great bug reports include: browser + OS + GPU, quality tier, the URL with parameters
you used, console output, and — if it is visual — a `?shot` capture or a screen recording.
Performance reports are most useful with the tier, your `window.__G.S.fpsSmooth` value
and whether AUTO RES was on.

## 🎨 Non-code contributions

Documentation fixes, new FAQ entries, translations of the docs, and benchmark data
from exotic hardware are genuinely valuable — open a PR against `docs/` or `CHANGELOG.md`.

Clear skies, and mind the photon sphere. 🕳
