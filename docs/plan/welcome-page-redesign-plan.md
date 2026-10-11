# Welcome Page Redesign Plan

## Overview

Update the landing page at `/` to match `expected-welcome.png` (desktop) and
`expected-welcome-responsive.png` (mobile). The work is pure HTML/CSS — no new routes,
no database changes, no JS frameworks. Three files are touched: `landing.html`,
`public_base.html`, and `onyx.css`. One test file is also updated.

---

## Gap Analysis — Current vs Target

### Desktop gaps (> 900 px)

| Area | Current state | Target state |
|---|---|---|
| **Layout** | Single-column `landing-hero` (max-width 520px), no illustration | Two-column flex/grid: left = copy, right = illustration; vertically centered |
| **Headline size** | `42px`, font-weight 800 | ~88px, letter-spacing tight (≈ −2px), weight 800 |
| **Blue subheading** | Present, 18px | Present, larger (~22px), color `#3d6fe8` |
| **Gray support line** | "Supporting staff with clearer records and employment history." present | Same text, slightly smaller gray |
| **CTA button** | `inline-flex`, no fixed width, padding 14px 32px | Fixed width ~390px, taller padding, `display:block`, `text-align:center` |
| **Illustration** | **Absent** | Five white rounded cards with inline SVG icons (grad cap, briefcase, person profile, document, people), gray placeholder bars, thin blue solid + dotted connector lines, small blue dots, two overlapping soft-blue circles in the background |
| **Footer** | Centered, no border | Left-aligned text, **top border** `1px solid var(--border)`, left-side only "Onyx Reborn — BSSI Modernization" (no right-side text) |
| **Top-bar Sign in** | Present | Present (no change needed) |

### Mobile gaps (≤ 900 px)

| Area | Current state | Target state |
|---|---|---|
| **Top-bar Sign in button** | Visible | **Hidden** — wordmark only |
| **Alignment** | N/A (single column already) | Everything centered |
| **Headline size** | 42px | ~44px |
| **Support line** | "Supporting staff with clearer records and employment history." | **Shorter**: "Clearer records and employment history." |
| **Blue subheading** | Same as desktop | Same as desktop but centered |
| **CTA button** | inline-flex, not full-width | `width: 100%`, centered |
| **Illustration** | Absent | Smaller 2-card version: person card + briefcase card, curved S-connector, light dot patterns, soft circles |
| **Footer** | Centered | Centered, text "BSSI Modernization" only (no "Onyx Reborn —" prefix) |

### Both

| Area | Current | Target |
|---|---|---|
| **Focus ring** | Not explicit | Visible `:focus-visible` outline on buttons/links |
| **Reduced motion** | Not handled | `@media (prefers-reduced-motion: reduce)` disables transitions |
| **Tests** | Smoke test checks 200 + "Onyx Reborn" only | Add assertions: headline text present + `href="/login"` link present |

---

## Sub-tasks

---

### Sub-task 1 — CSS additions for landing layout

**Intent**
Add the CSS classes needed for the two-column hero, the illustration scaffold, the
responsive overrides, focus/motion rules, and footer border. Nothing in the HTML
changes yet — this task just extends `onyx.css` so the markup written in sub-task 2
has real styles to attach to.

**Expected Outcomes**
- New classes exist in `onyx.css`:
  - `.landing-grid` — two-column flex/grid, vertically centred, gap; collapses to single column at ≤ 900 px
  - `.landing-left`, `.landing-right` — left/right column wrappers
  - `.landing-title` updated — font-size 88px, letter-spacing −2px (unchanged weight 800, navy colour)
  - `.landing-lead` updated — font-size 22px
  - `.landing-btn` updated — `display:block`, `width:390px`, `text-align:center`, taller padding
  - `.landing-illustration` — relative container, holds circles + cards
  - `.illus-circles` — two overlapping soft-blue (`#dbe8ff` / `#cad9ff`) filled circles via pseudo-elements or child divs
  - `.illus-card` — white, `border-radius:14px`, `box-shadow: 0 4px 18px rgba(0,0,0,.08)`, `padding:16px`, `display:flex`, `gap:12px`, positioned absolutely within the illustration
  - `.illus-icon` — 40–56 px square, `color: #1b2a4a` (navy)
  - `.illus-bars` — stacked gray placeholder bars (`height:8px`, `border-radius:4px`, `background:#dde2ef`)
  - `.illus-connector` — SVG element absolutely positioned, contains solid and dotted path lines + dot circles
  - Mobile overrides at `@media (max-width:900px)`: `.landing-title` 44px, `.landing-btn` width 100%, `.landing-right` reordered below CTA, `.landing-sub-mobile` shown / `.landing-sub-desktop` hidden, `.topbar-signin` hidden, `.landing-left` text-align center, footer centered with "BSSI Modernization" text only via content override class
  - `a:focus-visible, .landing-btn:focus-visible` — `outline: 3px solid var(--blue)`, `outline-offset:3px`
  - `@media (prefers-reduced-motion: reduce)` — set `transition:none` on `.landing-btn`
  - `.public-footer` — add `border-top: 1px solid var(--border)`, change to `text-align:left` at desktop, `text-align:center` at mobile

**Todo List**
1. Read `onyx.css` lines 753–865 (public/landing section) to confirm exact current selectors.
2. Add all new classes after the existing `.landing-btn:hover` block and before `.auth-card`.
3. Update `.landing-title` font-size to 88px and add letter-spacing.
4. Update `.landing-lead` font-size to 22px.
5. Update `.landing-btn` to block + 390px width + centered text.
6. Update `.public-footer` to add top border and left-align at desktop.
7. Add `@media (max-width:900px)` block with all mobile overrides.
8. Add focus-visible and reduced-motion rules.

**Relevant Context**
- File: `app/static/css/onyx.css`, lines 782–865 (landing section)
- Design tokens already in `:root`: `--navy`, `--blue`, `--border`, `--muted`
- Illustration soft-blue circle color `#dbe8ff` is new — add as `--blue-softer` in `:root` or inline

**Status** `[ ] pending`

---

### Sub-task 2 — HTML restructure of `landing.html` and `public_base.html`

**Intent**
Restructure the landing template to use the two-column grid and inject the full
HTML/CSS/SVG illustration on the right. Add mobile-specific sub line. Add
`topbar-signin` class to the topbar button so CSS can hide it at mobile. Update
footer to support desktop-left / mobile-center behaviour.

**Expected Outcomes**
- `public_base.html`:
  - The `<a href="/login" …>Sign in</a>` in the topbar block gains class `topbar-signin` so CSS can `display:none` it at ≤ 900 px.
  - Footer markup: left-side `<span class="footer-full">Onyx Reborn — BSSI Modernization</span>` + `<span class="footer-short">BSSI Modernization</span>` (CSS shows/hides each per breakpoint).
- `landing.html`:
  - Outer wrapper becomes `<div class="landing-grid">` replacing `landing-hero`.
  - Left column `<div class="landing-left">` contains:
    - `<h1 class="landing-title">A new chapter for student success</h1>`
    - `<p class="landing-lead">Student and employment management, modernized.</p>`
    - `<p class="landing-sub landing-sub-desktop">Supporting staff with clearer records and employment history.</p>`
    - `<p class="landing-sub landing-sub-mobile">Clearer records and employment history.</p>`
    - `<a href="/login" class="landing-btn">Sign in →</a>` (arrow as text entity or SVG; keep accessible)
    - `<p class="landing-cta-note">Use your organization account to continue.</p>`
  - Right column `<div class="landing-right">` contains the illustration `<div class="landing-illustration">` with:
    - Two soft-blue circle divs (`.illus-circle-1`, `.illus-circle-2`)
    - Five `.illus-card` divs, each with an inline SVG icon + `.illus-bars` stubs, positioned absolutely
    - One inline `<svg class="illus-connector">` with solid and dotted `<path>` elements and `<circle>` dots
  - Mobile illustration `<div class="landing-illustration landing-illustration-mobile">` with only person + briefcase card and curved connector
    - Hidden at desktop, visible at ≤ 900 px — use a single illustration div that adapts via CSS rather than two DOM trees, showing/hiding cards individually

**Todo List**
1. Add `topbar-signin` class to the Sign in anchor in `public_base.html`.
2. Update footer markup in `public_base.html` for dual-span desktop/mobile text.
3. Replace `landing-hero` wrapper with `landing-grid` in `landing.html`.
4. Add `landing-left` div with all copy elements including both sub-lines (desktop + mobile).
5. Add `landing-right` div with full illustration SVG/HTML (5 cards at desktop, collapse to 2 at mobile via CSS classes).
6. Verify the arrow in the button is `→` (HTML entity `&rarr;`) or an inline SVG — use SVG for crispness, same as current.

**Relevant Context**
- Files: `app/templates/public_base.html`, `app/templates/public/landing.html`
- Illustration icons needed (inline SVG, ~40×40 px, navy `#1b2a4a` fill):
  - Graduation cap (top-left card)
  - Briefcase (top-right card)
  - Person/profile silhouette — largest center card
  - Document with lines (bottom-left card)
  - Group of people (bottom-right card)
- Connector SVG: one solid curved line (grad cap → person), one solid line (person → doc), dotted lines (briefcase → person, person → people); small filled circles at junction points
- The illustration is decorative — all cards/connectors get `aria-hidden="true"`

**Status** `[ ] pending`

---

### Sub-task 3 — Tests

**Intent**
Keep the existing smoke test passing and add the two new assertions required by the task.

**Expected Outcomes**
- `tests/test_smoke.py` `test_landing_ok` continues to pass.
- New test `test_landing_headline` asserts:
  - `"A new chapter for student success"` is in the response body
  - `href="/login"` appears in the response body (the Sign in button links correctly)
- `pytest -q` → all tests pass (currently 10; will become 11).

**Todo List**
1. Add `test_landing_headline` to `tests/test_smoke.py` after `test_landing_ok`.
2. Run `pytest -q` and confirm 11 passed, 0 failed.

**Relevant Context**
- File: `tests/test_smoke.py`
- `client` fixture is already set up in `tests/conftest.py`

**Status** `[ ] pending`

---

## Files Changed

| File | Change |
|---|---|
| `app/static/css/onyx.css` | New/updated selectors for landing grid, illustration, responsive overrides, focus, motion, footer |
| `app/templates/public_base.html` | `topbar-signin` class on Sign in button; dual-span footer |
| `app/templates/public/landing.html` | Full restructure — two-column grid, illustration HTML/SVG |
| `tests/test_smoke.py` | New `test_landing_headline` test |

No routes, models, migrations, or other templates change.

---

## How to Check

**Desktop (> 900 px)**
1. Start the server: `.venv\Scripts\uvicorn app.main:app --reload`
2. Open `http://127.0.0.1:8000/` in a browser window wider than 900 px.
3. Verify: navy top bar with "Onyx Reborn" wordmark + blue "Sign in" button; two-column hero with large headline (~88px), blue subheading, gray support line, wide blue "Sign in →" button, helper note; illustration with 5 cards, connector lines, soft circles on the right; footer with top border, left-aligned "Onyx Reborn — BSSI Modernization".

**Mobile (≤ 900 px)**
1. Open DevTools → responsive mode → set width to 390 px (iPhone size).
2. Verify: top bar shows wordmark only (no Sign in button); everything centered; headline ~44px; shorter support line "Clearer records and employment history."; full-width "Sign in →" button; smaller illustration (2 cards, curved connector, dot patterns); footer centered "BSSI Modernization".

**Tests**
Run `.venv\Scripts\pytest -q` → 11 passed, 0 failed.
