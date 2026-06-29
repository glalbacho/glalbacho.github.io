# Instructions for Claude

When performing `git add` or `git commit` in this project:
- Never add yourself (Claude) as a co-author or author in commit messages
- Do not include any `Co-Authored-By: Claude` or similar lines
- Commits should only reflect the human author

## Always commit and push after changes

- After completing any request that modifies files in this repo, automatically `git add`, `git commit`, and `git push origin main` — do not wait to be asked to push.
- This keeps the live GitHub Pages site in sync with every change.

## Multilingual pages (EN / DE / KU) — single source of truth

- Page content lives **only** in `src/*.html` (trilingual, using `lang-en` / `lang-de` / `lang-ku` classes). These are the files to edit.
- Run `python3 tools/gen_i18n.py` to regenerate the live, single-language pages at `/` (en), `/de/` and `/ku/`, plus `sitemap.xml`. The generator also builds the nav, language switcher, `hreflang`/canonical tags and per-page meta.
- Do **not** hand-edit the generated `index.html`, `de/`, `ku/`, `research/`, `cv/`, `impressum/` files — they are overwritten on each run.
- Language is selected by URL path, not JavaScript. `theme.js` only handles the dark/light theme and opening the language dropdown.

## Paper: AngularBimeron.tex

- Do NOT suggest writing a proof for Corollary 3.1 (existence at prescribed angular momentum) — the proof is trivial and not needed
- Do NOT suggest writing the abstract — the abstract is written last, when the paper is finished

## Common mistake to avoid: energy bounds and bubbling exclusion

$E_{\lambda,\varepsilon}(\mathbf{m}_k) < 4\pi$ for every individual $k$ does NOT imply
$\liminf_k E_{\lambda,\varepsilon}(\mathbf{m}_k) < 4\pi$, and therefore does NOT allow
bubbling to be excluded. The sequence could have $E(\mathbf{m}_k) \to 4\pi$ from below.

To exclude bubbling and obtain precompactness, one needs a UNIFORM bound
$\sup_k E_{\lambda,\varepsilon}(\mathbf{m}_k) \leq E_0 < 4\pi$ (strict, uniform in $k$).

In this paper the uniform bound comes from $J(\mathbf{m}_k) \leq J_\star < \pi$:
since $J(\mathbf{m}_{R,a}) \to \pi$ as $a \to 0$, the constraint $J_k \leq J_\star < \pi$
forces the trial-field parameter $a_k \geq a_\star > 0$, giving Dirichlet energy
$\leq 4\pi R^2/(R^2 + a_\star^2) < 4\pi$ uniformly. Without $J_\star < \pi$ (strictly),
the uniform bound does not follow and the argument breaks down.
