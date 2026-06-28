# Lunaria — VSCode Theme Design

> **Navigation**: [palette.md](palette.md) covers the general palette design philosophy. [palette-eink.md](palette-eink.md) covers the E-Ink palette's physical design. This document covers how those palettes are applied to VS Code UI chrome for all four theme variants.

Semantic Lunaria 扩展为 VS Code 提供 4 个主题：Light、Dark、Eclipse、E-Ink。前三个共享 `template.yaml`，E-Ink 使用独立的 `template-eink.yaml`。全部启用 `semanticHighlighting: true`，同时定义 `tokenColors`（TextMate 语法）和 `semanticTokenColors`（LSP 语义高亮）。

---

## 1. 设计原则

以下规则跨所有 4 个变体一致。

### 1.1 高亮语义

四个高亮层使用不同的色相，用户一眼能分辨高亮来源：

```
层次          色相         示例 token                     语义
────────────────────────────────────────────────────────────
用户选区       冷色          selectionBackground            用户交互（鼠标/键盘选中）
被动词匹配     中性灰        wordHighlightBackground        光标处符号的其他出现
搜索匹配       暖色          findMatchBackground            查找/替换结果
诊断（波浪线）  vivid        editorError/Warning/Info       错误/警告/信息
```

- **选区** = 用户主动操作（冷色）
- **词高亮** = 被动提示（中性灰，不抢夺注意力）
- **搜索匹配** = 查找结果（暖色，荧光笔隐喻）
- **诊断** = 问题指示（vivid，文化联想：红=错误，黄=警告）

### 1.2 编辑器前景

- **不设 `selectionForeground`** — 非 HC 主题下 VS Code 忽略它，token 语法色保留
- **不设 `findMatchForeground` / `findMatchHighlightForeground`** — 搜索匹配内语法色保留
- **不设诊断 `background` / `border`** — 波浪线（foreground）已传递信号，重复视觉元素是噪音（E-Ink 因反射式屏幕清晰度需要而例外设了 background，见 §3.4）

### 1.3 边框约定

| 级别 | Token | 用途 |
|------|-------|------|
| 结构级 | `contrastBorder`、`*.border` | 主要 chrome 区域边界 |
| 控件级 | `mediumGray` | 浮动 widget、输入框边界 |

透明边框 `#00000000` 用于**明确抑制**不需要的边框（`editor.lineHighlightBorder`、`textBlockQuote.border`）。

### 1.4 覆盖范围

所有变体都定义以下现代 VS Code token：

- `editorGhostText.*` — 内联建议（Copilot 等）
- `editorStickyScroll.*` — 滚动粘性标题
- `editor.inlineValues*` — debug 内联值
- `editorBracketHighlight.foreground1-6` — 6 色调括号对
- `editorBracketHighlight.unexpectedBracket.foreground`
- `editorUnnecessaryCode.opacity` — 未使用代码淡化
- `editorGutter.foldingControlForeground` — 折叠箭头
- `editorOverviewRuler.background` — 显式透明防 bug
- `diffEditor.*Border` — diff 区域边框（替代 HC 自动虚线）
- `merge.border` — 合并冲突边框
- `breadcrumb.*` — 面包屑导航
- `sash.hoverBorder` — 面板拖拽手柄
- `terminal.background` — 终端背景与 editor 统一
- `terminal.findMatch*Border` — 终端搜索边框
- `terminal.tab.activeBorder` — 终端 tab 激活

> **注意**：部分 token 在 Regular（Light/Dark/Eclipse）模板中注释掉了，因为 VS Code 在发射式屏幕上的默认值已足够。E-Ink 为反射式屏幕的清晰度显式定义了全部。详见 §4 差异对照表。

### 1.5 不定义清单

以下 token 在所有变体中均不定义：

- `editor*.background` / `editor*.border` 诊断背景 — 波浪线已够
- `problems*Icon.foreground` — 跟随 foreground，不单独设图标色
- `scrollbarSlider.*` — 信任系统默认
- `notebook.*`、`charts.*`、`testing.*` — 这些子系统 VS Code 默认已够

### 1.6 语义高亮规则

全部变体共享同一套语义高亮规则：

| 语义 | 颜色 | 字体 |
|------|------|------|
| comment | `deEmphFg` | — |
| keyword | — | **bold** |
| operator | `softBlue` | — |
| number | `softBlue` | — |
| string | `softGreen` | — |
| regexp | `softRed` / E-Ink: `hcRed` | — |
| namespace | `softYellow` | — |
| type / class / enum / interface / struct | `softViolet` | — |
| method / property / enumMember | — | *italic* |
| parameter | `softMagenta` | — |
| parameter.declaration | — | underline |
| macro | `deEmphFg` | — |

---

## 2. Light / Dark / Eclipse（Regular 变体）

三款 Regular 主题共享同一个 `template.yaml`，通过不同的 palette JSON（`lunaria-light.json`、`lunaria-dark.json`、`lunaria-eclipse.json`）代入颜色值。`@invBg@`、`@fg@` 等变量在不同主题中解析为不同 hex，但 token 结构完全相同。

### 2.1 主题类型

| 主题 | `type` | VS Code base |
|------|--------|-------------|
| Light | `vs` | Visual Studio Light |
| Dark | `vs-dark` | Visual Studio Dark |
| Eclipse | `vs-dark` | Visual Studio Dark |

### 2.2 设计特征：深色反转

Regular 主题的核心设计特征：**Activity Bar 和 Title Bar 使用深色反转**。

| 区域 | Light | Dark | Eclipse |
|------|-------|------|---------|
| Activity Bar | `invBg`（深色） | `invBg` | `invBg` |
| Title Bar | `invBg`（深色） | `invBg` | `invBg` |
| Side Bar | `bg`（浅色） | `bg` | `bg` |
| Editor | `bg`（浅色） | `bg` | `bg` |
| Panel | `bg`（浅色） | `bg` | `bg` |

反转区域形成清晰的视觉层次：深色顶栏/侧栏 → 浅色工作区。与 E-Ink 的「全浅色 + 边框分隔」形成对比。

### 2.3 背景色差分隔

Regular 主题**不使用 `contrastBorder`**。Chrome 区域之间依赖背景色差来区分：

```
Light:  Activity Bar (#111) → Side Bar (#EEE) → Editor (#EEE)
Dark:   Activity Bar (#111) → Side Bar (#1A1A1A) → Editor (#1A1A1A)
```

Side Bar 和 Editor 同色，Activity Bar 深色反转——两个区域层级通过背景色自然分开。

### 2.4 逐区分析

#### 基础色

- `focusBorder`: `mediumGray`
- `foreground`: `fg`
- `selection.background`: `bgLowlight@40` — 全局 UI 选区，暖灰（非蓝）
- `errorForeground`: `softRed`

#### Activity Bar — 深色反转

Activity Bar 是界面中最左侧的深色区域，用 `vividViolet` 作为激活指示——与 Status Bar 形成统一的紫色锚点。徽章使用 `invVividViolet` 底 + `invBg` 字。

#### Side Bar — 浅色工作区

与 Editor 同背景色（`bg`），用 `emphFg`（近黑色）边框与 Editor 分隔——极简、低调。

#### Tabs — 隐形边框

`tab.border: "@bg@"` — 与背景同色，使 tab 之间没有可见分隔线，形成连续的标签栏。active tab 背景 `bg`，inactive tab 背景 `emphBg`。文件修改指示用 `bgBlue`。

#### Editor — 灰度高亮体系

**选区 & 搜索（统一灰度系）**：Selection 和 Find Match 都使用灰度系（`bgLowlight` / `bgHighlight`）。没有 E-Ink 的暖冷分离。所有高亮都是灰度层次——低调、不引入额外色相。

```
选区:  editor.selectionBackground:          bgLowlight@40   (暖灰)
搜索:  editor.findMatchBackground:           bgHighlight@    (白色)
      editor.findMatchHighlightBackground:  bgHighlight@80  (半透白)
```

**诊断**：统一用 vivid。只设 foreground（波浪线），不设 background/border。
```
editorError.foreground:   vividRed
editorWarning.foreground: vividYellow
editorInfo.foreground:    vividGreen
editorHint.foreground:    fg
```

**行号**：`softBlue`（非 hc 级——在发射式屏幕上 soft 已够清晰）

**括号对着色**：不定义（信任 VS Code 默认）

#### Panel & Status Bar

- `panel.border`: `emphFg`（近黑分隔线）
- `statusBar.background`: `vividViolet` — 唯一色彩锚点
- Status Bar 状态变化：debugging → `vividGreen`，noFolder → `vividYellow`

#### Terminal

ANSI 16 色使用 `termLow*`/`termHigh*` token。终端内选区使用 `bgLowlight@40`。终端背景跟随 editor（`bg`）。

### 2.5 控件定义

Regular 和 E-Ink 都定义了完整的 UI 控件。核心配色：

| 控件 | 配色 |
|------|------|
| Button | `vividViolet` 底 + `bg` 字 → hover `softViolet` |
| Secondary Button | `mediumGray` 底 → hover `fg` |
| Checkbox | `emphBg` 底 + `mediumGray` 边框 |
| Dropdown / Input | `emphBg` 底 + `mediumGray` 边框 |
| Input Validation | error → `vividRed` 边框，warning → `vividYellow` 边框 |
| List | active selection → `deEmphBg`，focus → `softBlue@80`，hover → `deEmphBg@80` |
| Menu | `emphBg` 底 + `mediumGray` 边框，selection → `bg` |

### 2.6 Git 装饰

所有 gitDecoration 使用 `fg`（单色），不引入色彩区分。在发射式屏幕上，文件资源管理器的图标已提供足够的视觉区分。

---

## 3. E-Ink 变体

E-Ink 主题使用独立的 `template-eink.yaml`，palette 来自 `lunaria-eink.json`。其设计围绕一个核心约束：**反射式 e-ink 显示器**。

### 3.1 主题类型

`type: "vs"`（标准 Visual Studio Light）。E-Ink 始终是浅色主题。

### 3.2 设计特征：全浅色 + 不反转

整个 UI 保持一致的浅色基调，不使用深色反转区域：

| 区域 | Regular | E-Ink |
|------|---------|-------|
| Activity Bar | `invBg`（深色反转） | `bg`（浅色，不反转） |
| Title Bar | `invBg`（深色反转） | `bg`（浅色，不反转） |
| Status Bar | `vividViolet` | `vividViolet`（唯一色彩锚点，与 Regular 相同） |

**为什么**：反射式 e-ink 显示器上，深色反转区域会产生不自然的亮暗过渡，破坏纸质感。全浅色 + 边框分隔的方式在 B&W e-ink 和彩色显示器上都更一致。

### 3.3 设计特征：Border 层级系统

E-Ink 用**两级边框**替代背景色差来分隔界面区域：

| 级别 | 颜色 | Token | 用途 |
|------|------|-------|------|
| **结构级** | `softBlue` (#47627E) | `contrastBorder`、`*.border` | Activity Bar、Side Bar、Editor Group、Panel、Peek View 等主要 chrome 区域边界 |
| **控件级** | `mediumGray` (#787878) | `editorWidget.border`、`panelInput.border` 等 | 浮动 widget、输入框等二级控件边界 |

这与 Regular 的「背景色差 + 无 contrastBorder」形成鲜明对比。

### 3.4 逐区分析

#### 基础色

- `contrastBorder` / `contrastActiveBorder`: `softBlue` — 核心设计元素
- `focusBorder`: `mediumGray`
- `foreground`: `fg`
- `selection.background`: `hcBlue@60` — 全局 UI 选区用蓝（与编辑器选区统一）

#### Activity Bar — 浅色 + 边框

全界面保持一致浅色背景 `bg`。用 `softBlue` 边框替代深色反转来区分区域——在 B&W e-ink 上边框线始终清晰，而背景色差可能模糊。

- `activityBar.background`: `bg`
- `activityBar.activeBackground`: `deEmphBg`（激活项有微妙背景色差）
- `activityBar.border`: `softBlue`
- `activityBarBadge`: `vividViolet` 底 + `bg` 字

#### Side Bar

与 Activity Bar 同背景，用 `softBlue` 边框分隔。

- `sideBar.border`: `softBlue`

#### Tabs — 可见边框

```
tab.border:           softBlue       — 可见边框（非隐形）
tab.activeBorder:     softBlue
tab.activeBorderTop:  vividRed       — 激活 tab 顶部红色指示条
tab.inactiveBackground: bg           — 非激活与激活同背景
tab.hoverBackground:  deEmphBg@40    — hover 可见
```

与 Regular 的 `tab.border: "@bg@"`（隐形）形成对比。

#### Editor — 暖冷高亮分离

E-Ink 编辑器高亮的**核心设计**：选区（冷蓝）和搜索匹配（暖金）使用不同的色相。在 B&W e-ink 上，暖金和冷蓝的灰度差异也足以区分。

```
语义层              色系      示例 token                    色相
─────────────────────────────────────────────────────────
用户主动操作（选区）  冷色·蓝    selectionBackground            hcBlue
被动提示（词匹配）    中性·灰    wordHighlightBackground        bgLowlight
搜索匹配（查找）     暖色·金    findMatchBackground            bgYellow
范围限定             冷色·淡蓝  findRangeHighlightBackground   bgBlue
─────────────────────────────────────────────────────────
```

**选区（冷色系）**：
```
editor.selectionBackground:           hcBlue@60     — 蓝底，约 38% 不透明度
editor.selectionHighlightBackground:  hcBlue@30     — 相同文本高亮，更淡
editor.inactiveSelectionBackground:   hcBlue@30     — 失焦时淡化
editor.selectionHighlightBorder:      hcBlue@       — 同词高亮的边框
```

**搜索匹配（暖色系）**：
```
editor.findMatchBackground:           bgYellow@     — 当前匹配，不透明暖金
editor.findMatchHighlightBackground:  bgYellow@60   — 其他匹配，半透明
editor.findMatchBorder:               hcYellow@     — 当前匹配边框
editor.findMatchHighlightBorder:      hcYellow@80   — 其他匹配边框
```

**设计要点**：
- findMatch 渲染在 selection 之上（VS Code 的装饰层叠顺序），重叠时暖金遮盖冷蓝——符合「搜索结果比选区更紧急」的语义
- 当前匹配用不透明背景 + 边框，其他匹配用半透明背景 + 淡边框——层级分明
- 所有前景色不设——非 HC 主题下 token 语法色自然保留
- range 高亮用蓝色系（`bgBlue@20`），与搜索的暖色区分

**词高亮（中性灰）**：
```
editor.wordHighlightBackground:       bgLowlight@25
editor.wordHighlightBorder:           deEmphFg
editor.wordHighlightStrongBackground: bgLowlight@25
editor.wordHighlightStrongBorder:     fg
```

词高亮属于被动提示，使用中性灰——不抢夺注意力，不与选区（蓝）或搜索（金）混淆。

**诊断**：E-Ink 在这里与 Regular 有区别——除了 foreground（波浪线）还设置了 background，在反射式屏幕上确保可见性：
```
editorError.foreground:    vividRed      editorError.background:    bgRed@40
editorWarning.foreground:  vividYellow   editorWarning.background:  bgYellow@40
editorInfo.foreground:     softBlue      editorInfo.background:     bgBlue@20
```

problems icons 也显式定义：error → `vividRed`，warning → `vividYellow`，info → `softBlue`。

**行号**：`hcBlue`（hc 级——比 Regular 的 `softBlue` 更高对比度，在 e-ink 上确保导航元素清晰）

**括号对着色**：显式定义 6 色 soft 循环（`softRed` → `softYellow` → `softGreen` → `softBlue` → `softViolet` → `softMagenta`），`unexpectedBracket` 用 `vividRed`。

#### overview ruler（滚动条标记）

overview ruler 的标记色与编辑器高亮色系保持一致——暖色标记搜索、冷色标记选区/词高亮：
```
findMatchForeground:           bgYellow@80     (暖色)
selectionHighlightForeground:  hcBlue@80       (冷色)
wordHighlightForeground:       softBlue@80     (冷色)
```

#### Panel / Terminal

Panel 和 Terminal 延续 Editor 的配色逻辑。`panel.border` 用 `softBlue`（非 Regular 的 `emphFg`），`terminal.border` 同样用 `softBlue`。

Terminal ANSI 16 色使用 `termLow*`/`termHigh*` token。终端内选区使用 `bgLowlight@40`，与编辑器蓝选区区分（终端有独立的交互语境）。终端搜索边框使用 `hcYellow@` / `hcYellow@80`。

#### Status Bar — 唯一色彩锚点

Status Bar 是整个界面中**唯一使用饱和色背景**的元素，作为浅色界面底部的视觉锚点。通过颜色变化传达状态（violet → green → yellow）。

- `statusBar.border`: `softBlue` — 在 e-ink 上为状态栏提供清晰边界

#### Title Bar — 轻量系统风格

保持浅色背景 `bg`，与 Regular 的深色反转形成对比。`titleBar.border` 用 `softBlue`。非激活状态文字用 `mediumGray`。

### 3.5 控件定义

E-Ink 共享 Regular 的控件定义体系，但有少量差异：

| Token | Regular | E-Ink | 理由 |
|-------|---------|-------|------|
| `menu.selectionBackground` | `bg` | `deEmphBg@40` | E-Ink 需要可见的选中反馈 |
| `list.activeSelectionBackground` | `deEmphBg` | `deEmphBg@60` | 透明度差异 |
| `list.inactiveSelectionBackground` | `deEmphBg` | `deEmphBg@40` | 透明度差异 |

### 3.6 Git 装饰

E-Ink 对 Git 状态使用 vivid 色彩区分（非 Regular 的全 `fg` 单色）：

| 状态 | Regular | E-Ink |
|------|---------|-------|
| added | `fg` | `vividGreen` |
| modified | `fg` | `vividYellow` |
| deleted | `fg` | `vividRed` |
| untracked | `fg` | `vividGreen` |
| ignored | `fg` | `mediumGray` |
| conflicting | `fg` | `vividRed` |
| submodule | `fg` | `vividBlue` |

### 3.7 对比度策略

#### 三层体系在 UI 中的映射

| 层级 | Token 类 | UI 用途 |
|------|---------|--------|
| **关键** | `hc*` | `contrastBorder`、链接、行号、编辑器选区 |
| **强调** | `vivid*` | 状态栏、错误/警告指示、徽章 |
| **正文** | `soft*` | 语法高亮、hover 高亮、边框颜色 |
| **中性** | grayscale | `fg`=正文、`mediumGray`=辅助、`deEmphFg`=注释 |

#### B&W E-Ink 保险

在 B&W e-ink（BOOX Mira Pro）上，`soft*` 和 `vivid*` 的颜色差异会坍缩为灰度，但：
- **hc\* 与 fg 的对比度依然足够**——UI 可用性不依赖色彩区分
- **暖金（bgYellow）和冷蓝（hcBlue）在灰度上也有明显差异**——搜索和选区在灰度上依然可分
- **边框系统是纯灰度元素**——`softBlue` 和 `mediumGray` 的 L\* 值确保在任何设备上可见

---

## 4. 变体差异对照表

### 4.1 核心策略差异

所有差异都从显示物理（发射式 vs 反射式）推导。非显示驱动的差异已统一。

| 维度 | Regular (Light/Dark/Eclipse) | E-Ink | 推导 |
|------|------------------------------|-------|------|
| `type` | `vs` / `vs-dark` | `vs` | 深色主题在 e-ink 上不可用 |
| Chrome 分隔 | 深色反转（`invBg`）+ 背景色差 | 全浅色（`bg`）+ `softBlue` 统一边框 | 深色反转在反射式屏幕上破坏纸感、导致鬼影 |
| `contrastBorder` | 不设 | `softBlue` | E-Ink 用 contrastBorder 作为全局边框回退 |
| 选区 vs 搜索 | 同灰度系（`bgLowlight` / `bgHighlight`） | 冷暖分离（`hcBlue` vs `bgYellow`） | B&W e-ink 上冷暖色的灰度差异 > 同色系的灰度差异 |
| 对比度层级 | soft / vivid 体系 | hc / vivid 体系（基线更高） | 反射式屏幕对比度低，关键元素需要 hc 级 |
| 诊断信号 | 仅 foreground（波浪线） | foreground + background（双边强调） | 反射式屏幕仅波浪线不够醒目 |
| Tab 分隔 | 隐形边框（`@bg@`）+ 背景色差 | 可见边框（`softBlue`）+ 红色激活指示条 | e-ink 上背景色差不可靠 |
| 边框色 | 近黑（`emphFg`）/ `mediumGray` | `softBlue`（所有结构级） | e-ink 需要统一的可见边框色 |
| Editor Group Header | `emphBg`（有层次） | `bg`（扁平） | e-ink 减少视觉噪音 |

### 4.2 Token 级差异

#### E-Ink 额外定义（Regular 不设——显示物理驱动）

这些 token 在 E-Ink 中显式定义以补偿反射式屏幕的可见性需求，Regular 在发射式屏幕上不需要。

| 类别 | Token | E-Ink 值 | 理由 |
|------|-------|---------|------|
| 诊断双边 | `editorError.background` | `bgRed@40` | 反射式需双边强调 |
| | `editorWarning.background` | `bgYellow@40` | 同上 |
| | `editorInfo.background` | `bgBlue@20` | 同上 |
| 搜索增强 | `editor.findMatchBorder` | `hcYellow@` | 搜索匹配在 e-ink 上需边框加强 |
| | `editor.findMatchHighlightBorder` | `hcYellow@80` | 同上 |
| | `editor.findRangeHighlightBorder` | `hcBlue@80` | 同上 |
| | `editor.selectionHighlightBorder` | `hcBlue@` | 选区同词高亮需边框 |
| 编辑器增强 | `editor.lineHighlightBackground` | `deEmphBg@40` | e-ink 上当前行需可见背景 |
| Diff 可见性 | `diffEditor.insertedTextBorder` | `bgGreen@60` | e-ink 上 diff 区域需边框 |
| | `diffEditor.removedTextBorder` | `bgRed@60` | 同上 |
| | `diffEditor.border` | `mediumGray@60` | 同上 |
| 边框扩展 | `statusBar.border` | `softBlue` | e-ink 状态栏需边界 |
| | `merge.border` | `softBlue@40` | 合并冲突需边框 |
| | `sash.hoverBorder` | `softBlue` | 面板拖拽手柄需可见 |
| | `minimap.background` | `bg` | e-ink 显式 minimap 背景 |
| | `minimap.infoHighlight` | `softBlue@80` | 同上 |
| | `terminal.tab.activeBorder` | `softBlue` | 终端 tab 激活指示 |
| Tab 可见性 | `tab.activeBorder` | `softBlue` | e-ink tab 需可见边框 |
| | `tab.activeBorderTop` | `vividRed` | 激活指示条 |
| | `tab.unfocusedActiveBorder` | `mediumGray` | 失焦 tab 边框 |
| | `tab.unfocusedActiveBorderTop` | `mediumGray` | 同上 |
| | `tab.hoverBackground` | `deEmphBg@40` | hover 反馈 |
| | `editorGroupHeader.tabsBorder` | `softBlue` | 标签栏底部边框 |
| | `editorGroupHeader.border` | `softBlue` | 编辑器组边框 |
| | `editorGroup.emptyBackground` | `bg` | 空编辑器组背景 |
| 终端搜索 | `terminal.findMatchBorder` | `hcYellow@` | 终端搜索可见性 |
| | `terminal.findMatchHighlightBorder` | `hcYellow@80` | 同上 |
| | `terminalCursor.foreground` | `emphFg` | 终端光标清晰度 |
| 面板分隔 | `panelSection.border` | `mediumGray@60` | 面板分区可见 |
| 状态指示 | `statusBarItem.errorForeground` | `vividRed` | 状态栏错误/警告可见 |
| | `statusBarItem.warningForeground` | `vividYellow` | 同上 |

#### 值不同的 token（同色相，不同对比度层级）

| Token | Regular | E-Ink | 理由 |
|-------|---------|-------|------|
| `editor.selectionBackground` | `bgLowlight@40` | `hcBlue@60` | 灰度系 vs 冷暖分离 |
| `editor.inactiveSelectionBackground` | `bgLowlight@20` | `hcBlue@30` | 同上 |
| `editor.selectionHighlightBackground` | `bgLowlight@20` | `hcBlue@30` | 同上 |
| `editor.findMatchBackground` | `bgHighlight@` | `bgYellow@` | 同上 |
| `editor.findMatchHighlightBackground` | `bgHighlight@80` | `bgYellow@60` | 同上 |
| `editor.findRangeHighlightBackground` | `bgHighlight@40` | `bgBlue@20` | E-Ink 用蓝区分 range |
| `editorLineNumber.foreground` | `softBlue` | `hcBlue` | 反射式导航需更高对比度 |
| `textLink.foreground` | `vividBlue` | `hcBlue` | 同色相（蓝），不同层级 |
| `textLink.activeForeground` | `softBlue` | `vividBlue` | 同色相，hover 反馈用相邻层级 |
| `editorOverviewRuler.findMatchForeground` | `bgHighlight@80` | `bgYellow@80` | 跟随编辑器搜索色 |
| `editorOverviewRuler.selectionHighlightForeground` | `bgLowlight@80` | `hcBlue@80` | 跟随编辑器选区色 |
| `minimap.findMatchHighlight` | `bgHighlight@80` | `bgYellow@40` | 同上 |
| `minimap.selectionHighlight` | `bgLowlight@40` | `hcBlue@80` | 同上 |
| `editorGroup.dropBackground` | `bgLowlight@40` | `bgBlue@40` | E-Ink 用蓝保持冷色一致 |
| `list.activeSelectionBackground` | `deEmphBg` | `deEmphBg@60` | E-Ink 用透明度分层 |
| `list.inactiveSelectionBackground` | `deEmphBg` | `deEmphBg@40` | 同上 |

#### 值不同的 token（Chrome 反转策略）

| Token | Regular | E-Ink | 理由 |
|-------|---------|-------|------|
| `activityBar.background` | `invBg` | `bg` | 深色反转 vs 全浅色 |
| `activityBar.foreground` | `invEmphFg` | `fg` | 跟随背景反转 |
| `activityBar.inactiveForeground` | `invFg` | `mediumGray` | 同上 |
| `activityBarBadge.background` | `invVividViolet` | `vividViolet` | 同上 |
| `titleBar.activeBackground` | `invBg` | `bg` | 同上 |
| `titleBar.activeForeground` | `invEmphFg` | `fg` | 同上 |
| `titleBar.inactiveForeground` | `invFg` | `mediumGray` | 同上 |
| `tab.inactiveBackground` | `emphBg` | `bg` | 反转 vs 扁平 |
| `editorGroupHeader.noTabsBackground` | `emphBg` | `bg` | 同上 |
| `editorGroupHeader.tabsBackground` | `emphBg` | `bg` | 同上 |

#### 值不同的 token（边框策略）

E-Ink 用 `softBlue` 统一所有结构级边框，Regular 用 `emphFg` / `mediumGray` 混用。

| Token | Regular | E-Ink |
|-------|---------|-------|
| `sideBar.border` | `emphFg` | `softBlue` |
| `panel.border` | `emphFg` | `softBlue` |
| `editorGroup.border` | `mediumGray` | `softBlue` |
| `peekView.border` | `mediumGray` | `softBlue` |
| `titleBar.border` | `mediumGray` | `softBlue` |
| `terminal.border` | `mediumGray` | `softBlue` |
| `tab.border` | `bg`（隐形） | `softBlue`（可见） |
| `panel.dropBorder` | `#00000000` | `softBlue@40` |
| `terminal.ansiWhite` | `lightGray` | `mediumGray` | E-Ink 终端白平衡调整 |
