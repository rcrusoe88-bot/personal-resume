# 霞鹜致宋 — 视觉规范

本文档定义「霞鹜致宋」系列简历模板（`zhisong-*`）的视觉系统。模板 CSS 必须遵循以下规范。

## 概述

「霞鹜致宋」系列包含 7 套版式，统一使用霞鹜致宋（LXGW ZhiSong）字体，并通过 CSS 变量支持 12 种主题配色。所有配色由 `generate.py` 根据主色自动衍生，模板内只引用 4 个配色变量。

## 色彩系统

### 主色（12 种可选，`--color` 参数）

| 配色名 key | 中文名 | 主色 hex |
|------|--------|---------|
| red-brown | 红棕 | `#894E54` |
| smoke-pink | 烟粉 | `#E4B5C4` |
| willow | 柳黄 | `#C9E079` |
| camel | 浅驼色 | `#E2C17C` |
| cloud-white | 云峰白 | `#D8E3E7` |
| autumn-blue | 秋波蓝 | `#8ABCD1` |
| olive | 橄榄黄绿 | `#BEC936` |
| pearl | 珍珠灰 | `#E4DFD7` |
| almond | 杏仁黄 | `#F7E8AA` |
| cream | 奶油白 | `#FFF8E7` |
| pineapple-red | 菠萝红 | `#FC7930` |
| begonia | 海棠 | `#FF6F61` |

### 变量衍生规则（generate.py 自动计算）

模板 CSS 顶部必须声明以下 4 个变量，值由 `{{...}}` 占位符注入：

```css
:root {
  --primary: {{primary_color}};   /* 主色，用于横幅、标题、边框、点缀 */
  --deep:    {{deep_color}};      /* 深色（主色混 55% 黑），用于可读性强的强调文字 */
  --soft:    {{soft_color}};      /* 极浅色（主色混 88% 白），用于背景块、卡片 */
  --line:    {{line_color}};      /* 浅色（主色混 70% 白），用于分隔线 */
}
```

- 文字强调（标题、标签文字）一律使用 `--deep`，保证任何主色下均有足够对比度；
- 大面积背景使用 `--soft`，避免浅色主色时看不清；
- 主色 `--primary` 仅用于视觉焦点（横幅、胶囊、圆点、边框）。

## 字体系统

```css
@font-face {
  font-family: 'LXGW ZhiSong';
  src: url('assets/fonts/LXGWZhiSongMN.ttf') format('truetype');
  font-display: swap;
}
font-family: 'LXGW ZhiSong', 'Songti SC', 'STSong', 'SimSun', serif;
```

- 字体文件 `LXGWZhiSongMN.ttf`（约 8.7MB）已随仓库分发于 `assets/fonts/` 目录，clone 即自带；
- `generate.py` 生成简历时会把字体复制到输出目录的 `assets/fonts/`；
- 字体缺失时回退到系统宋体（`Songti SC` / `SimSun`），模板仍可用。
- 中文字体为单字重（Regular），标题层级通过字号、字距与颜色区分，不使用合成加粗。

## 布局规范

- A4 尺寸：`width: 210mm; min-height: 297mm`
- 页面底色：中性灰（`#E4E0DC` 附近），简历纸为白/浅色
- 行高：正文 `1.6 – 1.75`，保证饱满数据下单页容纳
- 打印适配：`@media print { @page { size: A4; margin: 0; } }`
- `body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }` 保证背景色打印

## 版式（7 套模板）

| 模板名 | 名称 | 布局要点 |
|--------|------|---------|
| zhisong-sidebar | 经典左右分栏 | 左侧 `--deep` 深色栏（头像、联系方式、技能、教育）+ 右侧白底主体 |
| zhisong-minimal | 极简居中 | 顶部大字姓名居中 + 细线，下方双栏内容 |
| zhisong-timeline | 叙事时间线 | 顶部主色横幅 + 时间线竖线圆点串联经历 |
| zhisong-magazine | 杂志版面 | 超大姓名 + 编号模块，双栏高密度 |
| zhisong-cards | 圆角卡片 | 主色渐变姓名卡 + 2×2 圆角卡片网格 |
| zhisong-handbook | 文创手账 | 印章圆形 + 虚线分隔 + 胶囊标签，文艺风格 |
| zhisong-breath | 留白大气 | 单栏细排版，大留白，底部自评收尾 |

## 组件规范（通用 class）

7 套模板共用同一套数据块占位符，由 `generate.py` 注入，模板 CSS 需样式化以下通用 class：

| class | 语义 | 建议视觉 |
|-------|------|---------|
| `.experience` | 一条工作经历 | 底部间距，时间线版式加竖线/圆点 |
| `.exp-company` | 公司名 | 主文字色、偏大字号 |
| `.exp-date` | 起止时间 | 次要色 / `--soft` 标签 |
| `.exp-position` | 职位 | `--deep` 色 |
| `.exp-description li` | 工作描述 | 正文色，`::marker` 用 `--primary` |
| `.project` | 一个项目 | 卡片或 `--soft` 背景 + 主色左边框 |
| `.project-name` | 项目名 | 主文字色 |
| `.project-detail li` | 项目细节 | 正文色 |
| `.skill-tag` | 技能标签 | `--deep` 文字 + 主色描边/胶囊 |
| `.honor-tag` | 荣誉条目 | 单行条目或标签 |
| `.highlight-item` | 个人亮点 | `--soft` 背景 + 主色左边框 |
| `.highlight-label` / `.highlight-value` | 亮点标签/值 | 次要色 / 主文字色 |

## 设计约束（不可修改）

1. 色彩通过 CSS 变量注入，模板内不得硬编码具体色值（中性色 `--ink`/`--muted` 除外）；
2. 强调文字必须使用 `--deep` 保证可读性；
3. 字体链必须以 `'LXGW ZhiSong'` 开头，回退链保持衬线；
4. 页面必须为 A4 单页（内容超长时优先压缩间距与字号）；
5. 打印适配样式必须保留。
