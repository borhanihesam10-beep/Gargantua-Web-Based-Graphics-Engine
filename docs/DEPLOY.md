# 🌍 Deploy & Publish Guide

From this folder to a live, polished GitHub repository — two paths (web UI or git
CLI), plus GitHub Pages, repo presence polish, and releases.

---

## 1 · Prerequisites

- A GitHub account
- This repo folder, containing:
  `GARGANTUA.html`, `README.md`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`,
  `.gitignore`, `docs/`, `assets/`
- Everything is static — no build, no secrets, no environment.

---

## 2 · Path A — upload via the web UI (fastest)

1. Go to **github.com → New repository**.
2. Repository name: `gargantua-engine` · Description (copy-paste):
   ```text
   🕳 A real-time Kerr-metric relativistic black hole raytracer in a single self-contained HTML file — real geodesics, Doppler beaming, frame dragging. WebGL, zero dependencies, MIT.
   ```
   Visibility: **Public**. **Do not** initialize with a README (we have one).
3. On the empty-repo page click **"uploading an existing file"**.
4. Drag in **everything in this folder** (keep the folder structure: `docs/` and
   `assets/` must arrive as folders).
5. Commit message: `GARGANTUA engine v12.1 — initial public release`
6. **Commit changes** → done. Your engine is now on GitHub.

## 3 · Path B — git CLI (recommended if you will iterate)

```bash
cd gargantua-engine
git init
git add .
git commit -m "GARGANTUA engine v12.1 — initial public release"
git branch -M main
git remote add origin https://github.com/<username>/gargantua-engine.git
git push -u origin main
```

Updating later is just: edit → `git add .` → `git commit -m "..."` → `git push`.

---

## 4 · Enable GitHub Pages (the live demo) 🌐

1. Repository → **Settings → Pages**.
2. **Source**: `Deploy from a branch` · **Branch**: `main` · **Folder**: `/ (root)`.
3. Save. In ~1 minute the engine is live at:

```text
https://<username>.github.io/gargantua-engine/
```

Deep-link examples you can share:

```text
.../gargantua-engine/?mode=interstellar          # the film look, live
.../gargantua-engine/?nocine&cam=polar&q=high    # polar overflight, hands-on
```

> 💡 Tip: add the live URL to the repo's **About → Website** field (top-right gear
> on the repo page) — GitHub then shows it as a clickable tag.

---

## 5 · Polish the presence ✨

- **Social preview**: Settings → General → Social preview → upload
  `assets/hero-banner.png` (1280 × 640, exactly the recommended ratio). This is the
  card shown when the repo is shared on X/Telegram/Discord.
- **Topics** (About gear → Topics): `webgl`, `glsl`, `black-hole`, `raytracing`,
  `physics`, `interstellar`, `general-relativity`, `shader`, `creative-coding`,
  `single-file`, `javascript`.
- **Release**: Releases → Draft a new release → tag `v12.1` → title
  `GARGANTUA v12.1 — HYPERREAL` → paste the CHANGELOG's V12.1 section → publish.
  Attaching `GARGANTUA.html` to the release gives people a one-click download.
- **Description & pinned repo**: pin it on your profile; the banner does the rest.

---

## 6 · README asset paths

The README references assets relatively (`assets/hero-banner.png`,
`assets/gif-orbit.gif`, …) — they resolve correctly on the repo page **and** on the
GitHub Pages site without any configuration. If you rename anything, rename in
`README.md` too.

---

## 7 · Optional: custom domain

Pages → Custom domain → add your `engine.example.com` (CNAME to
`<username>.github.io`), enable **Enforce HTTPS**. The engine needs nothing else —
no cookies, no external requests, so it also behaves perfectly in locked-down CSPs.

---

## 8 · Post-launch checklist

- [ ] Open the Pages URL in a private window — intro plays, modes switch, sound works after a click
- [ ] README renders: banner, badges, gallery, GIFs animate
- [ ] Social preview card looks right (paste the repo URL into a chat to test)
- [ ] Topics + description + website set
- [ ] Release `v12.1` published with the HTML attached
- [ ] Star your own repo — every singularity needs an observer 🕳
