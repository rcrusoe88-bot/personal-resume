#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
楷体雅致简历生成器

用法：
    python generate.py <json文件路径> [--output <输出路径>] [--template <模板路径>]

示例：
    python generate.py ../examples/wushengjun.json
    python generate.py ../examples/wushengjun.json --output ../../伍生军_简历_楷体雅致.html
"""

import json
import os
import sys
import argparse


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
    import re
    # 找到占位符所在行的缩进
    pattern = re.compile(r'^([ \t]*)' + re.escape(placeholder) + r'[ \t]*$', re.MULTILINE)
    match = pattern.search(template)
    if not match:
        return template.replace(placeholder, block)
    # 占位符行的缩进
    line_indent = match.group(1)
    # 去除 block 每行的公共前缀缩进，然后重新加上占位符行的缩进
    block_lines = block.split('\n')
    # 找 block 的最小非空缩进
    min_indent = None
    for line in block_lines:
        if line.strip():
            leading = len(line) - len(line.lstrip())
            if min_indent is None or leading < min_indent:
                min_indent = leading
    if min_indent is None:
        min_indent = 0
    # 重新缩进
    adjusted_lines = []
    for line in block_lines:
        if line.strip():
            adjusted_lines.append(line_indent + line[min_indent:])
        else:
            adjusted_lines.append('')
    return pattern.sub('\n'.join(adjusted_lines), template)


def generate_resume(data, template):
    """用数据填充模板，生成完整 HTML"""
    result = template

    # 简单变量替换
    simple_vars = {
        '{{name}}': data.get('name', ''),
        '{{name_display}}': data.get('name_display', data.get('name', '')),
        '{{birthday}}': data.get('birthday', ''),
        '{{location}}': data.get('location', ''),
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
    result = replace_block_placeholder(result, '{{highlights}}', build_highlights_html(data.get('highlights', [])))

    return result


def main():
    parser = argparse.ArgumentParser(description='楷体雅致简历生成器')
    parser.add_argument('json_file', help='JSON 简历数据文件路径')
    parser.add_argument('--output', '-o', help='输出 HTML 文件路径（默认与 JSON 同目录）')
    parser.add_argument(
        '--template', '-t',
        help='HTML 模板路径（默认为 templates/kaiti-elegant.html）',
        default=None
    )
    args = parser.parse_args()

    # 脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)

    # 确定模板路径
    if args.template:
        template_path = args.template
    else:
        template_path = os.path.join(skill_dir, 'templates', 'kaiti-elegant.html')

    # 确定输出路径
    if args.output:
        output_path = args.output
    else:
        json_dir = os.path.dirname(os.path.abspath(args.json_file))
        json_name = os.path.splitext(os.path.basename(args.json_file))[0]
        output_path = os.path.join(json_dir, f'{json_name}_楷体雅致.html')

    # 加载数据和模板
    data = load_json(args.json_file)
    template = load_template(template_path)

    # 生成
    html = generate_resume(data, template)

    # 写入
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'简历已生成: {output_path}')


if __name__ == '__main__':
    main()