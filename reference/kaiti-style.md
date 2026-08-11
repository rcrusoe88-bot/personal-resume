# 楷体雅致 — 视觉规范

本文档定义"楷体雅致"简历模板的完整视觉系统。模板 CSS 必须严格遵循以下规范，不可自由发挥。

## 色彩系统

| 角色 | 色值 | 用途 |
|------|------|------|
| 页面底色 | `#f0ece4` | body background，羊皮纸质感 |
| 简历底色 | `#fffef9` | .resume 背景，微暖白 |
| 主文字色 | `#3a3a3a` | 正文默认色 |
| 姓名/标题色 | `#4a3a2a` | 深棕，用于姓名、章节标题 |
| 公司名色 | `#3a2a1a` | 最深棕，用于公司名称 |
| 副文字色 | `#6a5a4a` | 用于职位、专业等次级信息 |
| 辅助文字色 | `#7a6a5a` | 用于个人信息等 |
| 日期色 | `#9a8a7a` | 用于日期文本 |
| 日期背景色 | `#f5f0e6` | 用于日期标签背景 |
| 强调色/金色 | `#c4b69c` | 核心装饰色：边框、标记、图标 |
| 分割线色 | `#d4c4a8` | 用于边框线、分割线、时间线 |
| 页脚色 | `#b0a090` | 用于底部文字 |

### 渐变背景

- 项目卡片：`linear-gradient(135deg, #faf6ee, #f5efe3)`
- 技能标签：`linear-gradient(135deg, #f5efe3, #ede5d5)`
- 亮点卡片背景：`#faf6ee`

## 字体系统

```css
font-family: "STKaiti", "KaiTi", "楷体", "Microsoft YaHei", serif;
```

- 优先使用楷体系列（STKaiti → KaiTi → 楷体）
- 回退到微软雅黑
- 最终回退到 serif

## 布局规范

- A4 尺寸：`width: 210mm; min-height: 297mm`
- 装饰性内边框：`top/left/right/bottom: 18px`，`1px solid #c4b69c`
- 内容区 padding：`48px 52px`
- 行高：`1.9`
- 打印适配：`@page { margin: 0; size: A4; }`

## 组件规范

### 头部（.header）
- 居中对齐
- 底部 `1px solid #d4c4a8` 分割线
- 姓名：38px，font-weight 400，letter-spacing 14px，颜色 `#4a3a2a`
- 个人信息：15px，颜色 `#7a6a5a`，flex 居中，gap 35px

### 章节标题（.section-title）
- 左侧 `◆` 菱形标记，10px，颜色 `#c4b69c`
- 右侧渐变分割线：`linear-gradient(90deg, #d4c4a8, transparent)`
- 18px，font-weight 400，颜色 `#4a3a2a`

### 工作经历（.experience）
- 左侧时间线：`2px solid #d4c4a8`
- 时间线节点：10px 方块，背景 `#c4b69c`，`border-radius: 2px`
- 公司名：17px，颜色 `#3a2a1a`
- 日期标签：13px，颜色 `#9a8a7a`，背景 `#f5f0e6`，padding `3px 12px`
- 职位：15px，颜色 `#6a5a4a`
- 描述列表：14px，颜色 `#4a3a2a`，金色方形 `■` 标记（8px，`#c4b69c`）

### 项目经验（.project）
- 左侧金色边框：`3px solid #c4b69c`
- 渐变背景：`linear-gradient(135deg, #faf6ee, #f5efe3)`
- padding：`14px 18px`
- 项目名：15px，颜色 `#3a2a1a`

### 技能标签（.skill-tag）
- flex 布局，wrap，gap 10px
- padding：`5px 14px`
- 渐变背景 + `1px solid #d4c4a8` 边框
- 13px，颜色 `#5a4a3a`

### 个人亮点（.highlights）
- 2 列 grid 布局，gap 14px
- 每项 padding `12px 16px`，背景 `#faf6ee`，左侧 `3px solid #c4b69c`
- 标签：12px，颜色 `#9a8a7a`
- 值：15px，颜色 `#3a2a1a`

## 设计约束（不可修改）

1. 色彩系统不可替换为其他色系
2. 楷体字体优先级链不可更改
3. 装饰性内边框必须保留
4. 章节标题的 ◆ 标记 + 渐变线组合必须保留
5. 工作经历的左侧时间线必须保留
6. 项目卡片的渐变背景 + 左侧金线必须保留
7. 打印适配样式必须保留