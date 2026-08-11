#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人简历生成器（JSON / Markdown / Word → HTML）

支持「楷体雅致」与「霞鹜致宋」系列多套模板，可切换 12 种主题配色。
输入支持 JSON（.json）、Markdown（.md）与 Word（.docx）三种格式。

用法：
    python generate.py <简历文件路径> [--output <输出路径>] [--template <模板名或路径>] [--color <配色名>]

模板名（--template）：
    kaiti-elegant      楷体雅致（默认）
    zhisong-sidebar    致宋 · 经典左右分栏
    zhisong-minimal    致宋 · 极简居中
    zhisong-timeline   致宋 · 叙事时间线
    zhisong-magazine   致宋 · 杂志版面
    zhisong-cards      致宋 · 圆角卡片
    zhisong-handbook   致宋 · 文创手账
    zhisong-breath     致宋 · 留白大气

配色名（--color）：red-brown 红棕 / smoke-pink 烟粉 / willow 柳黄 / camel 浅驼色
    / cloud-white 云峰白 / autumn-blue 秋波蓝 / olive 橄榄黄绿 / pearl 珍珠灰
    / almond 杏仁黄 / cream 奶油白 / pineapple-red 菠萝红 / begonia 海棠
    也接受中文名（如 --color 烟粉）。

示例：
    python generate.py ../examples/wushengjun.json
    python generate.py ../examples/wushengjun.json --template zhisong-sidebar --color smoke-pink
"""

import json
import os
import sys
import shutil
import re
import argparse
import zipfile
from xml.etree import ElementTree as ET


# ---------------------------------------------------------------- 模板注册表
# 模板名 -> 文件名（相对 templates/ 目录）
TEMPLATE_REGISTRY = {
    'kaiti-elegant': 'kaiti-elegant.html',
    'zhisong-sidebar': 'zhisong-sidebar.html',
    'zhisong-minimal': 'zhisong-minimal.html',
    'zhisong-timeline': 'zhisong-timeline.html',
    'zhisong-magazine': 'zhisong-magazine.html',
    'zhisong-cards': 'zhisong-cards.html',
    'zhisong-handbook': 'zhisong-handbook.html',
    'zhisong-breath': 'zhisong-breath.html',
}

# 默认配色（红棕）与 12 种可选配色：key -> (中文名, hex)
DEFAULT_COLOR = 'red-brown'
PALETTES = {
    'red-brown':     ('红棕',    '#894E54'),
    'smoke-pink':    ('烟粉',    '#E4B5C4'),
    'willow':        ('柳黄',    '#C9E079'),
    'camel':         ('浅驼色',  '#E2C17C'),
    'cloud-white':   ('云峰白',  '#D8E3E7'),
    'autumn-blue':   ('秋波蓝',  '#8ABCD1'),
    'olive':         ('橄榄黄绿', '#BEC936'),
    'pearl':         ('珍珠灰',  '#E4DFD7'),
    'almond':        ('杏仁黄',  '#F7E8AA'),
    'cream':         ('奶油白',  '#FFF8E7'),
    'pineapple-red': ('菠萝红',  '#FC7930'),
    'begonia':       ('海棠',    '#FF6F61'),
}


def hex_to_rgb(hex_str):
    h = hex_str.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


def mix_color(hex_a, hex_b, weight_a):
    """把颜色 A 与颜色 B 混合，weight_a 为 A 的权重（0-1）"""
    ca = hex_to_rgb(hex_a)
    cb = hex_to_rgb(hex_b)
    return rgb_to_hex(tuple(int(a * weight_a + b * (1 - weight_a)) for a, b in zip(ca, cb)))


def resolve_color(color_name):
    """把配色名（key 或中文名）解析为 primary hex，未匹配则回退默认"""
    if not color_name:
        return PALETTES[DEFAULT_COLOR][1]
    for key, (zh, hex_str) in PALETTES.items():
        if color_name == key or color_name == zh or color_name == hex_str.lower():
            return hex_str
    print('警告：未知配色 "{}"，已回退到默认红棕。可选配色：'.format(color_name))
    for key, (zh, hex_str) in PALETTES.items():
        print('    {} / {} / {}'.format(key, zh, hex_str))
    return PALETTES[DEFAULT_COLOR][1]


def derive_palette(primary):
    """由主色衍生整套配色：deep(深色文字) / soft(极浅背景) / line(分隔线)"""
    return {
        'primary_color': primary,
        'deep_color': mix_color(primary, '#000000', 0.45),
        'soft_color': mix_color(primary, '#FFFFFF', 0.12),
        'line_color': mix_color(primary, '#FFFFFF', 0.30),
    }


def load_json(json_path):
    """加载 JSON 简历数据"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_template(template_path):
    """加载 HTML 模板"""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


# ---------------------------------------------------------------- 多格式输入解析
# 分节标题关键词：字段 key -> 常见标题写法
SECTION_KEYWORDS = [
    ('summary',         ['个人简介', '简介', '关于我', '个人概述', 'summary']),
    ('education',       ['教育背景', '教育经历', '教育', 'education']),
    ('experiences',     ['工作经历', '职业经历', '工作履历', '职业履历', '履历', 'experience']),
    ('projects',        ['项目经历', '项目经验', '代表项目', '项目', 'project']),
    ('skills',          ['专业技能', '技能', '技术栈', 'skills']),
    ('honors',          ['荣誉证书', '荣誉', '获奖', '奖项', 'honors']),
    ('highlights',      ['个人亮点', '亮点', 'highlight']),
    ('self_evaluation', ['自我评价', '自评', '个人评价']),
]

DATE_RE = re.compile(r'(\d{4}[\s年./\-]\d{0,2}[\s月./\-]?\d{0,2}|至今|现在|二[〇零一二三四五六七八九]{3}年)')


def match_section(line):
    """判断一行是否为分节标题，返回字段 key 或 None"""
    line = line.strip().strip('#').strip()
    for key, keywords in SECTION_KEYWORDS:
        for kw in keywords:
            if line == kw or line.startswith(kw):
                return key
    return None


def parse_contact_line(line):
    """从一行文本提取联系方式字段，返回 dict 或 None"""
    contact = {}
    m = re.search(r'(?:电话|手机|手机号|联系方式)[:：]?\s*([0-9+\- ]{7,16})', line)
    if m:
        contact['phone'] = m.group(1).strip()
    m = re.search(r'[\w.+-]+@[\w-]+(?:\.[\w-]+)+', line)
    if m:
        contact['email'] = m.group(0)
    m = re.search(r'(?:主页|网站|GitHub|github)[:：]?\s*([a-zA-Z0-9][a-zA-Z0-9./:_-]{2,})', line)
    if m:
        contact['website'] = m.group(1).strip()
    m = re.search(r'(?:城市|坐标|所在地|现居|地址)[:：]?\s*([一-龥]{2,10})', line)
    if m:
        contact['city'] = m.group(1).strip()
    return contact or None


def parse_exp_title(line):
    """解析工作经历子标题：公司 · 职位 · 时间"""
    exp = {'company': line, 'date': '', 'position': '', 'description': []}
    parts = [p.strip() for p in re.split(r'[·|｜,，、/]', line) if p.strip()]
    if len(parts) >= 2:
        exp['company'] = parts[0]
        date_idx = None
        for i, p in enumerate(parts):
            if i > 0 and DATE_RE.search(p):
                exp['date'] = p
                date_idx = i
                break
        rest = [p for i, p in enumerate(parts) if i > 0 and i != date_idx]
        exp['position'] = ' · '.join(rest)
    return exp


DESC_VERBS = ('负责', '参与', '主导', '开发', '设计', '搭建', '完成', '推动', '制定',
              '组织', '协调', '优化', '实现', '落地', '编写', '维护', '支持', '协助',
              '整理', '运营', '管理', '部署', '迭代', '跟进', '处理', '独立', '规划',
              '统筹', '对接', '探索', '分析', '改进', '重构')


def looks_like_description(line):
    """判断纯文本行是否更像工作/项目描述而非新条目标题（docx 无 bullet 标记时使用）"""
    if DATE_RE.search(line):
        return False
    if re.search(r'[·|｜,，、/]', line):
        return False
    return line.startswith(DESC_VERBS)


def parse_proj_title(line):
    """解析项目子标题：项目名（· 时间）"""
    parts = [p.strip() for p in re.split(r'[·|]', line) if p.strip()]
    return {'name': parts[0] if parts else line, 'details': []}


def parse_education(lines):
    """从若干行解析教育背景"""
    edu = {'school': '', 'date': '', 'major': '', 'research': ''}
    for line in lines:
        parts = [p.strip() for p in re.split(r'[·|，,]', line) if p.strip()]
        if not parts:
            continue
        if not edu['school']:
            edu['school'] = parts[0]
        for p in parts[1:]:
            if DATE_RE.search(p) and not edu['date']:
                edu['date'] = p
            elif not edu['major']:
                edu['major'] = p
            else:
                edu['research'] = (edu['research'] + ' ' + p).strip()
    return edu


def parse_highlight(line):
    """解析亮点行：标签：值"""
    m = re.match(r'^([^:：]{1,12})[:：]\s*(.+)$', line)
    if m:
        return {'label': m.group(1).strip(), 'value': m.group(2).strip()}
    return {'label': '亮点', 'value': line}


def split_list_items(line):
    """技能/标签行可能用逗号、顿号分隔"""
    return [s.strip() for s in re.split(r'[,，、;；]', line) if s.strip()]


def parse_resume_text(text):
    """把 Markdown / docx 提取的纯文本解析为简历数据结构"""
    data = {
        'name': '', 'name_display': '', 'location': '', 'update_date': '',
        'contact': {}, 'summary': '', 'self_evaluation': '',
        'education': {}, 'experiences': [], 'projects': [],
        'skills': [], 'honors': [], 'highlights': [],
    }
    current = None
    name_found = False
    exp = None
    proj = None
    summary_lines = []
    self_lines = []
    edu_lines = []

    for raw in text.split('\n'):
        raw = raw.strip()
        if not raw:
            continue
        # Markdown 标题行
        hm = re.match(r'^(#{1,6})\s*(.*)$', raw)
        if hm:
            level = len(hm.group(1))
            content = hm.group(2).strip()
            sec = match_section(content)
            if sec:
                current = sec
                continue
            if level == 1 and not name_found:
                data['name'] = content
                data['name_display'] = content
                name_found = True
                continue
            if current == 'experiences':
                exp = parse_exp_title(content)
                data['experiences'].append(exp)
                continue
            if current == 'projects':
                proj = parse_proj_title(content)
                data['projects'].append(proj)
                continue
            continue
        # 列表项标记
        is_bullet = bool(re.match(r'^[-*+]\s+', raw))
        content = re.sub(r'^[-*+]\s*', '', raw).strip()
        if not content:
            continue
        # 纯文本分节标题（docx 通常无 # 标记）
        sec = match_section(content)
        if sec and len(content) <= 25:
            current = sec
            continue
        # 顶部区域：姓名 / 联系方式
        if current is None:
            if not name_found:
                data['name'] = content
                data['name_display'] = content
                name_found = True
                continue
            c = parse_contact_line(content)
            if c:
                data['contact'].update(c)
                continue
            summary_lines.append(content)
            continue
        # 分节内
        if current == 'summary':
            summary_lines.append(content)
        elif current == 'self_evaluation':
            self_lines.append(content)
        elif current == 'education':
            edu_lines.append(content)
        elif current == 'experiences':
            if is_bullet and exp is not None:
                exp['description'].append(content)
            elif looks_like_description(content) and exp is not None:
                exp['description'].append(content)
            else:
                exp = parse_exp_title(content)
                data['experiences'].append(exp)
        elif current == 'projects':
            if is_bullet and proj is not None:
                proj['details'].append(content)
            elif looks_like_description(content) and proj is not None:
                proj['details'].append(content)
            else:
                proj = parse_proj_title(content)
                data['projects'].append(proj)
        elif current == 'skills':
            data['skills'].extend(split_list_items(content))
        elif current == 'honors':
            data['honors'].append(content)
        elif current == 'highlights':
            data['highlights'].append(parse_highlight(content))

    data['summary'] = ' '.join(summary_lines).strip()
    data['self_evaluation'] = ' '.join(self_lines).strip()
    if edu_lines:
        data['education'] = parse_education(edu_lines)
    if not data['name']:
        data['name'] = data['name_display'] = '未命名'
    return data


def read_docx_text(docx_path):
    """从 .docx 中提取正文段落文本（仅用标准库，无需 python-docx）"""
    with zipfile.ZipFile(docx_path) as z:
        xml = z.read('word/document.xml')
    # 安全防护：拒绝含 DOCTYPE / ENTITY 声明的文档，防 XXE 与 billion-laughs 攻击
    if b'<!DOCTYPE' in xml[:4096] or b'<!ENTITY' in xml:
        raise ValueError('检测到不安全的 XML 声明，已拒绝解析该 .docx 文件')
    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    root = ET.fromstring(xml)
    lines = []
    for p in root.iter('{%s}p' % ns):
        texts = [t.text or '' for t in p.iter('{%s}t' % ns)]
        line = ''.join(texts).strip()
        if line:
            lines.append(line)
    return '\n'.join(lines)


def load_data(input_path):
    """按扩展名加载简历数据：.json / .md / .markdown / .docx"""
    ext = os.path.splitext(input_path)[1].lower()
    if ext == '.json':
        with open(input_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    if ext in ('.md', '.markdown'):
        with open(input_path, 'r', encoding='utf-8') as f:
            return parse_resume_text(f.read())
    if ext == '.docx':
        return parse_resume_text(read_docx_text(input_path))
    # 未知扩展名：尝试按 JSON 解析
    with open(input_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# ---------------------------------------------------------------- 内容完整性检查
REQUIRED_SECTIONS = [
    ('summary', '个人简介'),
    ('education', '教育背景'),
    ('experiences', '工作经历'),
    ('skills', '专业技能'),
    ('contact', '联系方式'),
    ('projects', '项目经历'),
]

OPTIONAL_SECTIONS = [
    ('honors', '荣誉证书'),
    ('highlights', '个人亮点'),
    ('self_evaluation', '自我评价'),
]


def has_content(data, key):
    """判断某分节是否有实际内容"""
    v = data.get(key)
    if key == 'contact':
        return isinstance(v, dict) and bool(v)
    if isinstance(v, str):
        return bool(v.strip())
    if isinstance(v, list):
        return len(v) > 0
    if isinstance(v, dict):
        return any(bool(x) for x in v.values())
    return False


def sample_value(data, key):
    """取某分节的一小段示例值，便于引导时展示"""
    v = data.get(key)
    if key == 'contact':
        return str(next(iter(v.values()), '')) if isinstance(v, dict) and v else ''
    if isinstance(v, str):
        return v[:20]
    if isinstance(v, list):
        if not v:
            return ''
        first = v[0]
        if isinstance(first, dict):
            return str(next(iter(first.values()), ''))[:20]
        return str(first)[:20]
    if isinstance(v, dict):
        return str(next(iter(v.values()), ''))[:20]
    return ''


def check_content(data):
    """返回分节完整性报告：[('required'|'optional', key, 中文名, 是否有内容, 示例值)]"""
    report = []
    for key, label in REQUIRED_SECTIONS:
        report.append(('required', key, label, has_content(data, key), sample_value(data, key)))
    for key, label in OPTIONAL_SECTIONS:
        report.append(('optional', key, label, has_content(data, key), sample_value(data, key)))
    return report


def print_check_report(data, report):
    """打印分节完整性报告（供引导用户补齐/跳过）"""
    print('简历内容检查：{}'.format(data.get('name', '未命名')))
    for kind, key, label, ok, sample in report:
        if kind == 'required':
            status = '✅ 有' if ok else '❌ 缺失（必备，建议补齐）'
        else:
            status = '✅ 有' if ok else '⚪ 缺失（可选，可跳过）'
        extra = '：' + sample if sample else ''
        print('  {} {}{}'.format(status, label, extra))


def build_experiences_html(experiences):
    """构建工作经历 HTML（相对缩进，相对于 section 层级）"""
    blocks = []
    for exp in experiences:
        desc_items = '\n'.join(
            f'                            <li>{item}</li>'
            for item in exp['description']
        )
        block = f'''\
                <div class="experience">
                    <div class="exp-header">
                        <span class="exp-company">{exp["company"]}</span>
                    </div>
                    <span class="exp-date">{exp["date"]}</span>
                    <p class="exp-position">{exp["position"]}</p>
                    <div class="exp-description">
                        <ul>
{desc_items}
                        </ul>
                    </div>
                </div>'''
        blocks.append(block)
    return '\n\n'.join(blocks)


def build_projects_html(projects):
    """构建项目经验 HTML"""
    blocks = []
    for proj in projects:
        detail_items = '\n'.join(
            f'                            <li>{item}</li>'
            for item in proj['details']
        )
        block = f'''\
                <div class="project">
                    <p class="project-name">{proj["name"]}</p>
                    <div class="project-detail">
                        <ul>
{detail_items}
                        </ul>
                    </div>
                </div>'''
        blocks.append(block)
    return '\n\n'.join(blocks)


def build_skills_html(skills):
    """构建技能标签 HTML"""
    tags = '\n'.join(
        f'                    <span class="skill-tag">{skill}</span>'
        for skill in skills
    )
    return tags


def build_honors_html(honors):
    """构建荣誉证书 HTML（致宋系列模板使用）"""
    tags = '\n'.join(
        f'                    <span class="honor-tag">{honor}</span>'
        for honor in honors
    )
    return tags


def build_highlights_html(highlights):
    """构建个人亮点 HTML"""
    items = []
    for h in highlights:
        item = f'''\
                    <div class="highlight-item">
                        <p class="highlight-label">{h["label"]}</p>
                        <p class="highlight-value">{h["value"]}</p>
                    </div>'''
        items.append(item)
    return '\n\n'.join(items)


def replace_block_placeholder(template, placeholder, block):
    """替换模板中的块占位符，自动处理缩进对齐"""
    pattern = re.compile(r'^([ \t]*)' + re.escape(placeholder) + r'[ \t]*$', re.MULTILINE)
    match = pattern.search(template)
    if not match:
        return template.replace(placeholder, block)
    line_indent = match.group(1)
    block_lines = block.split('\n')
    min_indent = None
    for line in block_lines:
        if line.strip():
            leading = len(line) - len(line.lstrip())
            if min_indent is None or leading < min_indent:
                min_indent = leading
    if min_indent is None:
        min_indent = 0
    adjusted_lines = []
    for line in block_lines:
        if line.strip():
            adjusted_lines.append(line_indent + line[min_indent:])
        else:
            adjusted_lines.append('')
    return pattern.sub('\n'.join(adjusted_lines), template)


def apply_color(template, color_name):
    """按配色替换模板中的 {{primary_color}} 等占位符（不存在则原样返回）"""
    if '{{primary_color}}' not in template:
        return template
    primary = resolve_color(color_name)
    palette = derive_palette(primary)
    for placeholder, value in palette.items():
        template = template.replace('{{' + placeholder + '}}', value)
    return template


def generate_resume(data, template):
    """用数据填充模板，生成完整 HTML"""
    result = template

    # 简单变量替换
    contact = data.get('contact', {})
    simple_vars = {
        '{{name}}': data.get('name', ''),
        '{{name_display}}': data.get('name_display', data.get('name', '')),
        '{{initial}}': (data.get('name', '') or '')[:1],
        '{{birthday}}': data.get('birthday', ''),
        '{{location}}': data.get('location', ''),
        '{{summary}}': data.get('summary', ''),
        '{{self_evaluation}}': data.get('self_evaluation', ''),
        '{{contact_phone}}': contact.get('phone', ''),
        '{{contact_email}}': contact.get('email', ''),
        '{{contact_city}}': contact.get('city', ''),
        '{{contact_website}}': contact.get('website', ''),
        '{{update_date}}': data.get('update_date', ''),
    }

    for key, value in simple_vars.items():
        result = result.replace(key, value)

    # 教育背景
    edu = data.get('education', {})
    result = result.replace('{{education_school}}', edu.get('school', ''))
    result = result.replace('{{education_date}}', edu.get('date', ''))
    result = result.replace('{{education_major}}', edu.get('major', ''))
    result = result.replace('{{education_research}}', edu.get('research', ''))

    # 复杂块替换（自动对齐缩进）
    result = replace_block_placeholder(result, '{{experiences}}', build_experiences_html(data.get('experiences', [])))
    result = replace_block_placeholder(result, '{{projects}}', build_projects_html(data.get('projects', [])))
    result = replace_block_placeholder(result, '{{skills}}', build_skills_html(data.get('skills', [])))
    result = replace_block_placeholder(result, '{{honors}}', build_honors_html(data.get('honors', [])))
    result = replace_block_placeholder(result, '{{highlights}}', build_highlights_html(data.get('highlights', [])))

    return result


def copy_font_if_exists(skill_dir, output_path):
    """把霞鹜致宋字体复制到输出目录的 assets/fonts/（不存在则提示回退）"""
    src = os.path.join(skill_dir, 'assets', 'fonts', 'LXGWZhiSongMN.ttf')
    if not os.path.exists(src):
        print('提示：未找到字体 assets/fonts/LXGWZhiSongMN.ttf，致宋模板将回退到系统宋体。')
        print('      可前往 https://github.com/lxgw/LxgwZhiSong 下载后放置。')
        return
    out_dir = os.path.join(os.path.dirname(os.path.abspath(output_path)), 'assets', 'fonts')
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, 'LXGWZhiSongMN.ttf')
    if not os.path.exists(dst):
        shutil.copyfile(src, dst)
        print('已复制霞鹜致宋字体: {}'.format(dst))


def main():
    parser = argparse.ArgumentParser(description='个人简历生成器（JSON / Markdown / Word → HTML）')
    parser.add_argument('input_file', help='简历数据文件路径（支持 .json / .md / .docx）')
    parser.add_argument('--output', '-o', help='输出 HTML 文件路径（默认与输入文件同目录）')
    parser.add_argument(
        '--template', '-t',
        help='模板名（如 zhisong-sidebar）或模板文件路径（默认 kaiti-elegant）',
        default=None
    )
    parser.add_argument(
        '--color', '-c',
        help='配色名，如 红棕/烟粉/柳黄/秋波蓝 等（默认红棕 #894E54）',
        default=None
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='仅解析并输出分节完整性报告（用于引导用户补齐内容），不生成 HTML'
    )
    args = parser.parse_args()

    # 脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)

    # 确定模板路径
    if args.template:
        if args.template in TEMPLATE_REGISTRY:
            template_path = os.path.join(skill_dir, 'templates', TEMPLATE_REGISTRY[args.template])
        else:
            template_path = args.template
    else:
        template_path = os.path.join(skill_dir, 'templates', 'kaiti-elegant.html')

    # 模板显示名（用于默认输出文件名）
    template_name = os.path.splitext(os.path.basename(template_path))[0]

    # 确定输出路径
    if args.output:
        output_path = args.output
    else:
        json_dir = os.path.dirname(os.path.abspath(args.input_file))
        json_name = os.path.splitext(os.path.basename(args.input_file))[0]
        output_path = os.path.join(json_dir, '{}_{}.html'.format(json_name, template_name))

    # 加载数据
    data = load_data(args.input_file)

    # 仅检查模式：输出分节完整性报告，供引导用户补齐/跳过
    if args.check:
        print_check_report(data, check_content(data))
        return

    template = load_template(template_path)

    # 应用配色
    template = apply_color(template, args.color)

    # 生成
    html = generate_resume(data, template)

    # 写入
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('简历已生成: {}'.format(output_path))

    # 复制字体（致宋系列模板需要）
    copy_font_if_exists(skill_dir, output_path)


if __name__ == '__main__':
    main()
