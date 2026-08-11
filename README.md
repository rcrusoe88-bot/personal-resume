# Personal Resume — 多模板简历生成器

<p align="center">
  <img src="https://img.shields.io/github/license/rcrusoe88-bot/personal-resume?style=flat-square" alt="License">
  <img src="https://img.shields.io/github/stars/rcrusoe88-bot/personal-resume?style=flat-square" alt="Stars">
  <img src="https://img.shields.io/github/last-commit/rcrusoe88-bot/personal-resume?style=flat-square" alt="Last Commit">
</p>

> 一个基于 Markdown / Word 简历文档的个人简历生成器 Skill。输入 `.md` 或 `.docx` 简历文档（也支持结构化 JSON），一键生成可预览、截图或打印为 PDF 的 A4 HTML 简历，支持「楷体雅致」与「霞鹜致宋」两套视觉系统、8 套模板与 12 种配色，并会自动检查分节完整性、引导补齐或跳过。

## 功能特性

- 🎨 **两套视觉系统**：
  - **楷体雅致**（kaiti-elegant）：楷体字体、暖棕色系、菱形标记、时间线式经历、渐变项目卡片
  - **霞鹜致宋**（zhisong-*）：霞鹜致宋字体、7 套版式（左右分栏/极简/时间线/杂志/卡片/手账/留白）、12 种主题配色
- 🎨 **12 种配色**：红棕 / 烟粉 / 柳黄 / 浅驼色 / 云峰白 / 秋波蓝 / 橄榄黄绿 / 珍珠灰 / 杏仁黄 / 奶油白 / 菠萝红 / 海棠
- 📄 **A4 标准尺寸**：210mm × 297mm，浏览器直接打开即成品
- 🔒 **本地处理**：全部在本地完成，不上传任何数据，保护隐私
- 🖨️ **多种输出**：浏览器预览 / Ctrl+P 存 PDF / 开发者工具截全页
- 🧩 **多格式输入**：支持 Markdown（.md）/ Word（.docx）/ JSON（.json），自动识别并解析
- 💬 **内容引导**：解析后检查分节完整性，缺失的必备分节引导补齐，可选分节（荣誉/亮点等）可选择跳过

## 快速开始

```bash
# 1. 准备 JSON 简历数据（格式见下方）
# 2. 使用示例数据测试（默认楷体雅致）
python scripts/generate.py examples/wushengjun.json

# 3. 致宋 · 经典左右分栏 + 烟粉配色
python scripts/generate.py examples/wushengjun.json --template zhisong-sidebar --color smoke-pink

# 4. 致宋 · 圆角卡片 + 秋波蓝，指定输出路径
python scripts/generate.py data.json --template zhisong-cards --color 秋波蓝 --output my_resume.html

# 5. 从 Markdown / Word 简历生成（自动识别格式）
python scripts/generate.py resume.md --template zhisong-minimal --color 烟粉
python scripts/generate.py resume.docx --template zhisong-breath

# 6. 使用自定义模板
python scripts/generate.py data.json --template templates/kaiti-elegant.html
```

生成成功后用浏览器打开 HTML 即可预览，Ctrl+P 可另存为 PDF。

## 模板一览

| 模板名 | 风格 | 配色支持 |
|--------|------|---------|
| `kaiti-elegant` | 楷体雅致（默认） | — |
| `zhisong-sidebar` | 致宋 · 经典左右分栏 | ✅ 12 色 |
| `zhisong-minimal` | 致宋 · 极简居中 | ✅ 12 色 |
| `zhisong-timeline` | 致宋 · 叙事时间线 | ✅ 12 色 |
| `zhisong-magazine` | 致宋 · 杂志版面 | ✅ 12 色 |
| `zhisong-cards` | 致宋 · 圆角卡片 | ✅ 12 色 |
| `zhisong-handbook` | 致宋 · 文创手账 | ✅ 12 色 |
| `zhisong-breath` | 致宋 · 留白大气 | ✅ 12 色 |

## 字体说明

- **楷体雅致**：使用系统楷体（STKaiti / KaiTi），无需额外文件；
- **霞鹜致宋**：使用霞鹜致宋字体 `LXGWZhiSongMN.ttf`（约 8.7MB），已随仓库分发于
  `assets/fonts/` 目录，clone 后开箱即用；生成时脚本自动复制到输出目录。
  缺失（或使用不带字体的旧副本）时回退系统宋体，仍可正常使用。

## 内容引导

用户提交的简历若未按标准分节书写，skill 会先检查分节完整性并引导补齐：
- **必备分节**：个人简介 / 教育背景 / 工作经历 / 专业技能（缺失时引导补充）
- **可选分节**：联系方式 / 项目经历 / 荣誉证书 / 个人亮点 / 自我评价（可跳过）

```bash
# 先查看分节检查报告
python scripts/generate.py resume.md --check
```

用户可随时说"跳过"，对应分节不展示。详细引导规则见 [SKILL.md](SKILL.md)。

## JSON 数据格式

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

> `contact`、`summary`、`honors`、`self_evaluation` 为可选字段（致宋模板展示）；旧版 JSON 完全兼容。

> **Markdown 输入**（.md）：按标题分节（个人简介/教育背景/工作经历/项目经历/专业技能/荣誉证书/个人亮点/自我评价），
> 列表项作条目，`·` 分隔公司/职位/时间。完整规范见 [SKILL.md](SKILL.md)。**Word 输入**（.docx）：直接读取正文段落，按同样规则识别。

## 目录结构

```
personal-resume/
├── SKILL.md                    # Skill 定义文件（含触发条件与使用说明）
├── README.md                   # 本文件
├── reference/
│   ├── kaiti-style.md          # 楷体雅致视觉规范
│   └── zhisong-style.md        # 霞鹜致宋视觉规范
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
│   └── generate.py             # 生成脚本（JSON → HTML）
└── examples/
    ├── wushengjun.json         # 示例数据 · JSON 格式（脱敏占位内容）
    └── resume.md               # 示例数据 · Markdown 格式
```

## 触发关键词

个人简历、生成简历、简历模板、楷体、楷体雅致、kaiti、kaiti-elegant、致宋、霞鹜、zhisong、personal resume

## 使用场景

1. **从 JSON 生成**：已有结构化数据，直接渲染为简历
2. **口述内容生成**：口述个人信息，助手构建 JSON 后生成
3. **更新现有简历**：修改 JSON 指定字段或更换配色，重新生成 HTML

## 许可

本项目作为 Skill 开源发布，仅含通用模板与示例（示例数据为脱敏占位内容）。霞鹜致宋字体遵循 [IPA Font License 1.0](https://opensource.org/licenses/IPA/)。
