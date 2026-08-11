---
name: personal-resume
description: >
  个人简历生成器，从 JSON 数据生成 A4 尺寸的 HTML 简历。支持「楷体雅致」与
  「霞鹜致宋」共 8 套模板，以及 12 种主题配色（红棕/烟粉/柳黄/秋波蓝等）。
  支持自定义姓名、联系方式、个人简介、教育背景、工作经历、项目经验、技能标签、
  荣誉证书和个人亮点。务必在以下场景使用：用户说"个人简历""生成简历""简历模板"
  "楷体""kaiti""致宋""霞鹜""zhisong""personal resume"；或用户需要生成或更新
  个人简历时。
---

# Personal Resume Skill — 多模板简历生成器

输入结构化 JSON 数据，输出可直接在浏览器预览、截图或打印为 PDF 的 A4 尺寸 HTML 简历。

## 触发条件

当用户提到以下关键词时激活此 skill：
- 个人简历、生成简历、简历模板
- 楷体、楷体雅致、kaiti、kaiti-elegant
- 致宋、霞鹜、霞鹜致宋、zhisong
- 烟粉、秋波蓝、柳黄 等配色名（提示换色）
- personal resume、kaiti resume

## 核心能力

### 生成简历 (generate)

从 JSON 数据生成指定模板与配色的 HTML 简历。

**触发示例：**
- "帮我生成个人简历"
- "用楷体风格生成简历，数据在 my_data.json"
- "用致宋·经典左右分栏模板，烟粉配色，生成简历"
- "personal-resume generate data.json --template zhisong-sidebar --color 烟粉"

**执行流程：**
1. 读取用户提供的 JSON 简历数据文件（或用户口述内容自行构建 JSON）
2. 确定模板（`--template`，默认楷体雅致）与配色（`--color`，默认红棕）
3. 运行 `scripts/generate.py` 填充模板
4. 输出完整 HTML 文件（含字体复制）

### 模板一览（--template）

| 模板名 | 风格 | 说明 |
|--------|------|------|
| `kaiti-elegant` | 楷体雅致 | 楷体、暖棕、菱形标记、时间线（默认） |
| `zhisong-sidebar` | 致宋 · 经典左右分栏 | 左深色栏 + 右白底 |
| `zhisong-minimal` | 致宋 · 极简居中 | 大字居中，双栏克制留白 |
| `zhisong-timeline` | 致宋 · 叙事时间线 | 顶部横幅 + 时间线 |
| `zhisong-magazine` | 致宋 · 杂志版面 | 超大姓名 + 编号模块 |
| `zhisong-cards` | 致宋 · 圆角卡片 | 姓名卡 + 2×2 卡片网格 |
| `zhisong-handbook` | 致宋 · 文创手账 | 印章 + 虚线 + 标签 |
| `zhisong-breath` | 致宋 · 留白大气 | 单栏细排版，大留白 |

### 配色一览（--color，12 种）

`red-brown 红棕 / smoke-pink 烟粉 / willow 柳黄 / camel 浅驼色 / cloud-white 云峰白 /
autumn-blue 秋波蓝 / olive 橄榄黄绿 / pearl 珍珠灰 / almond 杏仁黄 / cream 奶油白 /
pineapple-red 菠萝红 / begonia 海棠`（中英文名均可）

配色由主色自动衍生深色强调、浅色背景与分隔线，保证任意主色下可读性。

**JSON 数据格式：**
```json
{
  "name": "姓名",
  "name_display": "姓 名（带空格展示）",
  "birthday": "出生日期",
  "location": "所在地",
  "contact": {
    "phone": "电话",
    "email": "邮箱",
    "city": "城市",
    "website": "个人主页"
  },
  "summary": "个人简介",
  "education": {
    "school": "学校名称",
    "date": "起止时间",
    "major": "专业",
    "research": "研究方向"
  },
  "experiences": [
    {
      "company": "公司名称",
      "date": "起止时间",
      "position": "职位",
      "description": ["工作内容1", "工作内容2"]
    }
  ],
  "projects": [
    {
      "name": "项目名称",
      "details": ["项目细节1", "项目细节2"]
    }
  ],
  "skills": ["技能1", "技能2"],
  "honors": ["荣誉1", "荣誉2"],
  "highlights": [
    {
      "label": "亮点标签",
      "value": "亮点内容"
    }
  ],
  "self_evaluation": "自我评价",
  "update_date": "更新日期"
}
```

> `contact`、`summary`、`honors`、`self_evaluation` 为可选字段，缺失时对应区域留空；
> 旧版 JSON（无上述字段）同样兼容。

**命令行用法：**
```bash
python scripts/generate.py <json文件> [--output <输出路径>] [--template <模板名>] [--color <配色名>]
```

**示例：**
```bash
# 使用示例数据测试（默认楷体雅致）
python scripts/generate.py examples/wushengjun.json

# 致宋 · 经典左右分栏 + 烟粉配色
python scripts/generate.py examples/wushengjun.json --template zhisong-sidebar --color smoke-pink

# 致宋 · 圆角卡片 + 秋波蓝，指定输出
python scripts/generate.py data.json --template zhisong-cards --color 秋波蓝 --output my_resume.html

# 使用自定义模板路径
python scripts/generate.py data.json --template ./my-template.html
```

## 文件结构

```
personal-resume/
├── SKILL.md                    # 本文件
├── reference/
│   ├── kaiti-style.md          # 楷体雅致视觉规范
│   └── zhisong-style.md        # 霞鹜致宋视觉规范（12 色配色 + 7 版式）
├── templates/
│   ├── kaiti-elegant.html      # 楷体雅致模板（默认）
│   ├── zhisong-sidebar.html    # 致宋 · 经典左右分栏
│   ├── zhisong-minimal.html    # 致宋 · 极简居中
│   ├── zhisong-timeline.html   # 致宋 · 叙事时间线
│   ├── zhisong-magazine.html   # 致宋 · 杂志版面
│   ├── zhisong-cards.html      # 致宋 · 圆角卡片
│   ├── zhisong-handbook.html   # 致宋 · 文创手账
│   └── zhisong-breath.html     # 致宋 · 留白大气
├── scripts/
│   └── generate.py             # 生成脚本（JSON → HTML，含配色衍生）
└── examples/
    └── wushengjun.json         # 示例数据（含 contact/summary/honors 等）
```

## 字体说明（霞鹜致宋模板）

- 致宋系列模板使用霞鹜致宋字体 `LXGWZhiSongMN.ttf`（约 8.7MB，单文件，不随仓库分发）；
- 首次使用前请从 https://github.com/lxgw/LxgwZhiSong/releases 下载，
  放置到 skill 的 `assets/fonts/LXGWZhiSongMN.ttf`；
- 生成时脚本会自动把字体复制到输出目录的 `assets/fonts/`；
- 若字体缺失，模板回退到系统宋体，仍可正常使用。

## 输出格式

- **格式**：HTML（单文件，CSS 内嵌；致宋模板含同目录 `assets/fonts/`）
- **尺寸**：A4（210mm × 297mm）
- **预览**：浏览器直接打开
- **打印**：Ctrl+P → 保存为 PDF
- **截图**：浏览器开发者工具截取全页

## 视觉规范

- 楷体雅致模板遵循 `reference/kaiti-style.md`；
- 致宋系列模板遵循 `reference/zhisong-style.md`（色彩、字体、版式、通用组件 class）。

## 使用场景

### 场景 1：从 JSON 生成简历
```
用户：帮我用致宋·极简风格生成简历，数据在 my_data.json，烟粉配色
Claude：[读取 JSON] [运行 generate.py --template zhisong-minimal --color smoke-pink] [输出 HTML]
```

### 场景 2：口述内容生成简历
```
用户：帮我生成简历，我是张三，在XX公司做工程师，喜欢用致宋留白风格
Claude：[构建 JSON] [运行 generate.py --template zhisong-breath] [输出 HTML]
```

### 场景 3：更新现有简历 / 换配色
```
用户：帮我把简历换成秋波蓝配色
Claude：[重跑 generate.py --color autumn-blue] [输出新 HTML]
```

## 注意事项

1. **隐私保护**：所有处理在本地完成，不上传任何数据
2. **模板/配色**：`--template` 仅接受上表模板名或文件路径；`--color` 接受上表配色名
3. **中文排版**：日期、章节标题等建议使用中文格式（如"二〇二六年六月"）
4. **内容精简**：工作经历每段控制在 3-5 条，突出量化成果
5. **单页约束**：致宋模板已针对常规数据压缩为 A4 单页；数据特别多时可适当精简内容
