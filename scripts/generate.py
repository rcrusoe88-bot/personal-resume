#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人简历生成器（JSON → HTML）

支持「楷体雅致」与「霞鹜致宋」系列多套模板，可切换 12 种主题配色。

用法：
    python generate.py <json文件路径> [--output <输出路径>] [--template <模板名或路径>] [--color <配色名>]

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
    parser = argparse.ArgumentParser(description='个人简历生成器（JSON → HTML）')
    parser.add_argument('json_file', help='JSON 简历数据文件路径')
    parser.add_argument('--output', '-o', help='输出 HTML 文件路径（默认与 JSON 同目录）')
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
        json_dir = os.path.dirname(os.path.abspath(args.json_file))
        json_name = os.path.splitext(os.path.basename(args.json_file))[0]
        output_path = os.path.join(json_dir, '{}_{}.html'.format(json_name, template_name))

    # 加载数据和模板
    data = load_json(args.json_file)
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
