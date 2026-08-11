---
name: personal-resume
description: >
  个人简历生成器，基于楷体雅致主题风格，从 JSON 数据生成 A4 尺寸的 HTML 简历。
  支持自定义姓名、教育背景、工作经历、项目经验、技能标签和个人亮点。
  务必在以下场景使用：用户说"个人简历""生成简历""简历模板""楷体""kaiti"
  "personal resume""kaiti resume"；或用户需要基于楷体雅致风格生成或更新个人简历时。
---

# Personal Resume Skill — 楷体雅致

基于"楷体雅致"视觉系统的个人简历生成器。输入结构化 JSON 数据，输出可直接在浏览器预览、截图或打印为 PDF 的 A4 尺寸 HTML 简历。

## 触发条件

当用户提到以下关键词时激活此 skill：
- 个人简历、生成简历、简历模板
- 楷体、楷体雅致、kaiti、kaiti-elegant
- personal resume、kaiti resume

## 核心能力

### 生成简历 (generate)

从 JSON 数据生成楷体雅致风格的 HTML 简历。

**触发示例：**
- "帮我生成个人简历"
- "用楷体风格生成简历"
- "personal-resume generate data.json"

**执行流程：**
1. 读取用户提供的 JSON 简历数据文件（或用户口述内容自行构建 JSON）
2. 加载 `templates/kaiti-elegant.html` 模板
3. 运行 `scripts/generate.py` 填充模板
4. 输出完整 HTML 文件

**JSON 数据格式：**
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

**命令行用法：**
```bash
python scripts/generate.py <json文件> [--output <输出路径>]
```

**示例：**
```bash
# 使用示例数据测试
python scripts/generate.py examples/wushengjun.json

# 指定输出路径
python scripts/generate.py examples/wushengjun.json --output my_resume.html

# 使用自定义模板
python scripts/generate.py data.json --template templates/kaiti-elegant.html
```

## 文件结构

```
personal-resume/
├── SKILL.md                    # 本文件
├── reference/
│   └── kaiti-style.md          # 楷体雅致视觉规范（色彩、字体、布局、组件）
├── templates/
│   └── kaiti-elegant.html      # HTML 模板（含 {{占位符}}）
├── scripts/
│   └── generate.py             # 生成脚本（JSON → HTML）
└── examples/
    └── wushengjun.json         # 示例数据
```

## 输出格式

- **格式**：HTML（单文件，CSS 内嵌）
- **尺寸**：A4（210mm × 297mm）
- **预览**：浏览器直接打开
- **打印**：Ctrl+P → 保存为 PDF
- **截图**：浏览器开发者工具截取全页

## 视觉规范

生成的简历必须严格遵循 `reference/kaiti-style.md` 中定义的视觉系统：
- 楷体字体优先级链
- 暖棕色系色彩系统
- 装饰性内边框
- 章节标题菱形标记 + 渐变线
- 工作经历时间线
- 项目卡片渐变背景
- 技能标签 flex 布局
- 亮点卡片双列 grid

## 使用场景

### 场景 1：从 JSON 生成简历
```
用户：帮我用楷体风格生成个人简历，数据在 my_data.json
Claude：[读取 JSON] [运行 generate.py] [输出 HTML 文件]
```

### 场景 2：口述内容生成简历
```
用户：帮我生成楷体风格的简历，我是张三，在XX公司做工程师...
Claude：[构建 JSON 数据] [运行 generate.py] [输出 HTML 文件]
```

### 场景 3：更新现有简历
```
用户：帮我更新简历，把工作经历改一下
Claude：[读取现有 JSON] [修改指定字段] [重新生成 HTML]
```

## 注意事项

1. **隐私保护**：所有处理在本地完成，不上传任何数据
2. **设计约束**：色彩系统、字体、布局必须严格遵循 kaiti-style.md
3. **中文排版**：日期、章节标题等使用中文格式（如"二〇二六年六月"）
4. **内容精简**：工作经历每段控制在 3-5 条，突出量化成果