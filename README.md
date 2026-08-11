# Personal Resume — 楷体雅致简历生成器

<p align="center">
  <img src="https://img.shields.io/github/license/rcrusoe88-bot/personal-resume?style=flat-square" alt="License">
  <img src="https://img.shields.io/github/stars/rcrusoe88-bot/personal-resume?style=flat-square" alt="Stars">
  <img src="https://img.shields.io/github/last-commit/rcrusoe88-bot/personal-resume?style=flat-square" alt="Last Commit">
  <img src="https://img.shields.io/github/languages/top/rcrusoe88-bot/personal-resume?style=flat-square" alt="Top Language">
</p>

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api/pin/?username=rcrusoe88-bot&repo=personal-resume&theme=vue&show_owner=true" alt="personal-resume 仓库数据">
</p>

> 一个基于「楷体雅致」视觉系统的个人简历生成器 Skill。输入结构化 JSON 数据，一键生成可直接在浏览器预览、截图或打印为 PDF 的 A4 尺寸 HTML 简历。

## 功能特性

- 🎨 **楷体雅致视觉系统**：楷体字体优先级链、暖棕色系配色、装饰性内边框、章节标题菱形标记、时间线式工作经历、渐变项目卡片、双列亮点 grid
- 📄 **A4 标准尺寸**：210mm × 297mm，浏览器直接打开即成品
- 🔒 **本地处理**：全部在本地完成，不上传任何数据，保护隐私
- 🖨️ **多种输出**：浏览器预览 / Ctrl+P 存 PDF / 开发者工具截全页
- 🧩 **结构化输入**：JSON 定义教育、经历、项目、技能、亮点，字段自由增减

## 快速开始

```bash
# 1. 准备 JSON 简历数据（格式见下方）
# 2. 使用示例数据测试
python scripts/generate.py examples/wushengjun.json

# 3. 指定输出路径
python scripts/generate.py examples/wushengjun.json --output my_resume.html

# 4. 使用自定义模板
python scripts/generate.py data.json --template templates/kaiti-elegant.html
```

生成成功后用浏览器打开 HTML 即可预览，Ctrl+P 可另存为 PDF。

## JSON 数据格式

```json
{
  "name": "姓名",
  "name_display": "姓 名（带空格展示）",
  "birthday": "出生日期",
  "location": "所在地",
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
  "highlights": [
    {
      "label": "亮点标签",
      "value": "亮点内容"
    }
  ],
  "update_date": "更新日期"
}
```

## 目录结构

```
personal-resume/
├── SKILL.md                    # Skill 定义文件（含触发条件与使用说明）
├── README.md                   # 本文件
├── reference/
│   └── kaiti-style.md          # 楷体雅致视觉规范（色彩、字体、布局、组件）
├── templates/
│   └── kaiti-elegant.html      # HTML 模板（含 {{占位符}}）
├── scripts/
│   └── generate.py             # 生成脚本（JSON → HTML）
└── examples/
    ├── wushengjun.json         # 示例数据（脱敏占位内容）
    └── wushengjun_楷体雅致.html # 示例输出
```

## 触发关键词

个人简历、生成简历、简历模板、楷体、楷体雅致、kaiti、kaiti-elegant、personal resume、kaiti resume

## 使用场景

1. **从 JSON 生成**：已有结构化数据，直接渲染为简历
2. **口述内容生成**：口述个人信息，助手构建 JSON 后生成
3. **更新现有简历**：修改 JSON 指定字段，重新生成 HTML

## 许可

本项目作为 Skill 开源发布，仅含通用模板与示例（示例数据为脱敏占位内容）。使用与再分发请遵循 Skill 原始授权约定。

## 📊 作者 GitHub 数据

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=rcrusoe88-bot&show_icons=true&theme=vue" alt="rcrusoe88-bot 的 GitHub 统计">
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=rcrusoe88-bot&layout=compact&theme=vue" alt="rcrusoe88-bot 的常用语言">
</p>
