# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.0.6 - 2026-06-28

### Changed

- **E-Ink palette redesign** — Complete overhaul for eye comfort and display compatibility.
  Warm paper-tone neutrals (bg `#E8E2DA`, fg `#47423E`), moderate contrast (7.7:1),
  three-tier L\* spacing (soft 49–52, vivid 38–47, hc 30–32) with clear separation.
  Vivid colors desaturated ~10% for reduced visual fatigue during extended reading.
- **Regular / E-Ink template unification** — Removed unjustified differences between
  Regular and E-Ink variants. Both now share the same token set; remaining differences
  are strictly display-physics-driven (chrome inversion, border strategy, contrast tier).
- **Engine requirement** bumped from `^1.63.0` to `^1.81.0` for modern token support.

### Added

- Bracket pair colorization (`editorBracketHighlight.foreground1-6`) for all variants.
- Color-differentiated Git decorations (vivid) for all variants.
- Modern editor tokens: `editorGhostText`, `editorStickyScroll`, `editor.inlineValues`,
  `editorUnnecessaryCode.opacity`, `diffEditor.*Border`, `editorGutter.foldingControlForeground`.
- `eink-targets.json` + `eink-tune.py` — scientific OKLCH-based palette tuning tool.

### Fixed

- `terminal.ansiBrightWhite` now uses `@brightWhite@` (was incorrectly `@white@`).
- E-Ink `terminalCursor` foreground/background no longer identical (cursor was invisible).
- `editorOverviewRuler.background` explicitly set to `#00000000` to prevent rendering bugs.
- Removed deprecated `editor.onTypeRenameBackground`.

### Documentation

- Design docs: `palette.md` (color science), `palette-eink.md` (E-Ink physics),
  `vscode.md` (theme design), `index.md` (navigation).

## 0.0.5 - 2026-06-24

### Changed

- Updated E-Ink theme.

## 0.0.4 - 2023-07-19

### Changed

- Upgraded vsce to 2.15.0 to support `--pre-release` publishing.

## 0.0.3 - 2023-07-19

### Added

- New E-Ink theme, a high-contrast light theme optimized for e-ink displays.

### Fixed

- Horizontal rule (`prose`) styling.

### Changed

- Normalized theme template format (YAML).

### Build

- Added `.vscodeignore` to exclude Makefile and other artefacts from the extension package.

## 0.0.2 - 2022-01-03

### Added

- New semantic highlighting.

### Msic

- Reduce the size of artefact.

## 0.0.1 - 2021-01-28

- Initial release.
