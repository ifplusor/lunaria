# Lunaria — Design Documentation

## 调色板

- **[palette.md](palette.md)** — 调色板设计总纲。CAM16 色彩外观模型、7 色调体系、三层对比度（soft/vivid/hc）、中性灰阶、背景色系列。
- **[palette-eink.md](palette-eink.md)** — E-Ink 调色板物理设计。CAM16 反射式建模、目标设备矩阵（BOOX Mira Pro / MacBook Pro XDR / LG IPS）、手调理由、完整 color token 参考。

## 平台实现

- **[vscode.md](vscode.md)** — VS Code 主题设计（全部 4 个变体）。跨变体共享规则、Light/Dark/Eclipse 深色反转设计、E-Ink 全浅色边框设计、完整差异对照表。

## 权威数据

调色板的数值定义位于仓库根目录：
- `lunaria-light.json` — Light palette
- `lunaria-dark.json` — Dark palette
- `lunaria-eclipse.json` — Eclipse palette
- `lunaria-eink.json` — E-Ink palette

调色板生成算法位于 `lunaria.ipynb`（Jupyter notebook），模板替换脚本为 `lunarize.py`。
