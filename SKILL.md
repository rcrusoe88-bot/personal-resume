---
name: personal-resume
description: >
  个人简历生成器，从 Markdown（.md）或 Word（.docx）简历文档生成 A4 尺寸的 HTML 简历
  （也支持结构化 JSON）。支持「楷体雅致」与「霞鹜致宋」共 8 套模板、12 种主题配色。
  自动检查文档分节完整性，缺失的必备分节引导用户补齐，可选分节用户可选择跳过。
  支持自定义姓名、联系方式、个人简介、教育背景、工作经历、项目经验、技能标签、
  荣誉证书和个人亮点。务必在以下场景使用：用户说"个人简历""生成简历""简历模板"
  "楷体""kaiti""致宋""霞鹜""zhisong""personal resume"；或用户需要从 .md / .docx
  文档生成或更新个人简历时。
---

# Personal Resume Skill — 多模板简历生成器

输入 Markdown（.md）或 Word（.docx）简历文档，输出可直接在浏览器预览、截图或打印为 PDF 的 A4 尺寸 HTML 简历。

## 触发条件

当用户提到以下关键词时激活此 skill：
- 个人简历、生成简历、简历模板
- 楷体、楷体雅致、kaiti、kaiti-elegant
- 致宋、霞鹜、霞鹜致宋、zhisong
- 烟粉、秋波蓝、柳黄 等配色名（提示换色）
- personal resume、kaiti resume

## 核心能力

### 生成简历 (generate)

从 Markdown / Word 简历文档生成指定模板与配色的 HTML 简历。

**触发示例：**
- "帮我生成个人简历"
- "用楷体风格生成简历，数据在 my_resume.md"
- "用致宋·经典左右分栏模板，烟粉配色，生成简历"
- "personal-resume generate resume.md --template zhisong-sidebar --color 烟粉"

**执行流程：**
1. 读取用户提供的简历文件（支持 `.md` / `.docx`，兼容 `.json`，或用户口述内容自行构建）
2. 确定模板（`--template`，默认楷体雅致）与配色（`--color`，默认红棕）
3. 运行 `scripts/generate.py` 填充模板
4. 输出完整 HTML 文件（含字体复制）

**输入格式说明：**
- **Markdown**（.md）：推荐，按标题分节，见下方 Markdown 简历格式；
- **Word**（.docx）：直接读取正文，按标题/段落识别，无需安装 python-docx；
- **JSON**（.json）：兼容，字段见下方说明。

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

**字段说明（JSON，兼容）：**
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

> 上表为 JSON 兼容字段说明；`contact`、`summary`、`honors`、`self_evaluation` 为可选字段，缺失时对应区域留空。

**Markdown 简历格式（推荐）：**

Markdown 输入按标题分节，列表项作条目，`·` 分隔公司/职位/时间。示例：

```markdown
# 张三

电话：138 0000 0000
邮箱：zhangsan@example.com
城市：上海市

## 个人简介
生物工艺方向资深工程师，深耕 mRNA 疫苗工艺开发。

## 教育背景
示例大学（985院校） · 2013.09 - 2020.07 · 生物工程 · 本科及学硕

## 工作经历
### 某生物技术有限公司 · 工艺开发工程师（mRNA疫苗方向） · 2023.08至今
- 负责mRNA疫苗的质粒模板生产和下游纯化工艺
- 负责工艺文件起草，包括工艺操作规程SOP

### 某医药科技有限公司 · 分子生物工程师 · 2019.07-2021.05
- 负责病毒类亚单位重组蛋白的构建及外源表达

## 项目经历
### 病毒Fiber重组蛋白表达
- 利用截短后目的基因插入pET系列载体
- 经NI-NTA纯化后获得纯度90%以上的目的蛋白

## 专业技能
- mRNA工艺开发
- 蛋白纯化

## 荣誉证书
- mRNA工艺开发能手

## 个人亮点
- 公众号运营：行业垂类公众号 3000+ 粉丝

## 自我评价
把复杂工艺拆成可落地的流程。
```

支持的分节标题：个人简介 / 教育背景 / 工作经历 / 项目经历 / 专业技能 / 荣誉证书 / 个人亮点 / 自我评价。
Word 文档（.docx）以同样方式识别段落与标题（无需 Markdown 标记）。

**命令行用法：**
```bash
python scripts/generate.py <简历文件> [--output <输出路径>] [--template <模板名>] [--color <配色名>]
```

**示例：**
```bash
# 使用示例数据测试（默认楷体雅致）
python scripts/generate.py examples/resume.md

# 致宋 · 经典左右分栏 + 烟粉配色
python scripts/generate.py examples/resume.md --template zhisong-sidebar --color smoke-pink

# 从 Markdown 简历生成（致宋 · 极简 + 秋波蓝）
python scripts/generate.py examples/resume.md --template zhisong-minimal --color autumn-blue

# 从 Word 简历生成（致宋 · 留白）
python scripts/generate.py my_resume.docx --template zhisong-breath

# 致宋 · 圆角卡片 + 秋波蓝，指定输出
python scripts/generate.py resume.md --template zhisong-cards --color 秋波蓝 --output my_resume.html

# 使用自定义模板路径
python scripts/generate.py resume.md --template ./my-template.html
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
│   └── generate.py             # 生成脚本（Markdown / Word → HTML，兼容 JSON）
└── examples/
    ├── resume.md               # 示例数据 · Markdown 格式（推荐）
    └── wushengjun.json         # 示例数据 · JSON 格式（兼容）
```

## 字体说明（霞鹜致宋模板）

- 致宋系列模板使用霞鹜致宋字体 `LXGWZhiSongMN.ttf`（约 8.7MB，单文件），
  已随仓库分发于 `assets/fonts/LXGWZhiSongMN.ttf`，clone 仓库即自带，开箱即用；
- 若使用不带字体的旧副本，可从 https://github.com/rcrusoe88-bot/personal-resume 或
  https://github.com/lxgw/LxgwZhiSong/releases 获取字体放入 `assets/fonts/`；
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

### 场景 1：从 Markdown / Word 文档生成简历
```
用户：帮我用致宋·极简风格生成简历，这是我的 resume.md，烟粉配色
Claude：[读取文档] [运行 generate.py --template zhisong-minimal --color smoke-pink] [输出 HTML]
```

### 场景 2：口述内容生成简历
```
用户：帮我生成简历，我是张三，在XX公司做工程师，喜欢用致宋留白风格
Claude：[整理为 Markdown 简历] [运行 generate.py --template zhisong-breath] [输出 HTML]
```

### 场景 3：更新现有简历 / 换配色
```
用户：帮我把简历换成秋波蓝配色
Claude：[重跑 generate.py --color autumn-blue] [输出新 HTML]
```

## 内容检查与引导

用户提交的简历（MD/DOCX）若未按标准分节书写，必须主动检查分节完整性，引导用户补齐；用户选择跳过时予以尊重。

### 分节清单

| 类型 | 分节 | 缺失时 |
|------|------|--------|
| 必备 | 个人简介 / 教育背景 / 工作经历 / 专业技能 / 联系方式 / 项目经历 | 引导用户补充 |
| 可选 | 荣誉证书 / 个人亮点 / 自我评价 | 询问跳过或补充 |

### 检查方式

解析文档后运行检查，查看分节报告：

```bash
python scripts/generate.py <简历文件> --check
```

报告示例：

```
简历内容检查：张三
  ❌ 缺失（必备，建议补齐） 个人简介
  ✅ 有 教育背景：示例大学（985院校）
  ✅ 有 工作经历：某生物技术有限公司
  ⚪ 缺失（可选，可跳过） 荣誉证书
  ⚪ 缺失（可选，可跳过） 个人亮点
```

### 引导规则

1. **先展示检查结果**，列出缺失分节，再一一引导；
2. **必备分节缺失**：说明重要性并给出引导问题与示例，尽量让用户补齐后再生成：
   - 个人简介：请用一两句话介绍您的背景与核心优势？
   - 教育背景：毕业院校、专业与起止时间？
   - 工作经历：每段工作的公司、职位、时间，以及 2-4 条可量化的成果？
   - 专业技能：您主要掌握的技能或工具？
   - 联系方式：电话、邮箱、所在城市？（简历必备）
   - 项目经历：参与过的代表性项目名称与 1-2 条成果？
3. **可选分节缺失**：询问"需要补充吗？可以跳过"；用户说"跳过"即不再追问；
4. **尊重跳过**：用户明确跳过的分节在简历中不展示；
5. **信息不完整时**：先按已有内容生成初稿，同时引导补齐缺失项。

### 引导对话示例

```
用户：用我这份简历生成（resume.docx）
Claude：已读取您的简历。以下必备分节缺失：个人简介、教育背景。
        建议先补充，我可以引导您填写。荣誉证书、个人亮点等可选部分也可以跳过。
用户：个人简介：我是生物工艺方向工程师，深耕 mRNA 疫苗工艺。
Claude：好的，已记录个人简介。教育背景需要补充吗？
用户：跳过教育背景吧。
Claude：明白，教育背景将不展示。现在开始生成简历。
```

## 注意事项

1. **隐私保护**：所有处理在本地完成，不上传任何数据
2. **输入格式**：支持 `.md` / `.docx`（兼容 `.json`），按扩展名自动识别
3. **模板/配色**：`--template` 仅接受上表模板名或文件路径；`--color` 接受上表配色名
4. **中文排版**：日期、章节标题等建议使用中文格式（如"二〇二六年六月"）
5. **内容精简**：工作经历每段控制在 3-5 条，突出量化成果
6. **单页约束**：致宋模板已针对常规数据压缩为 A4 单页；数据特别多时可适当精简内容
