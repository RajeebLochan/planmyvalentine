"""Render stored plan text as safe HTML.

Plans are stored either as raw markdown (fallback plans) or as the partly
converted HTML that core.prompts.format_plan_content produced. Both are
normalised back to markdown, escaped, then rendered, so the page never
outputs unescaped user or model text.
"""
import html
import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

_BULLET = re.compile(r'^\s*[-*•]\s+(.*)$')
_HEADING = re.compile(r'^(#{1,3})\s+(.+)$')
_BOLD_LINE = re.compile(r'^\*\*([^*]+)\*\*:?$')
_RULE = re.compile(r'^(-{3,}|\*{3,}|_{3,})$')


def _to_markdown(text):
    """Turn legacy stored HTML back into the markdown it came from."""
    text = text.replace('\r\n', '\n')
    text = re.sub(r'<strong>(.*?)</strong>', r'**\1**', text, flags=re.S)
    text = re.sub(
        r'<h([1-3])>(.*?)</h\1>',
        lambda m: '\n\n' + '#' * int(m.group(1)) + ' ' + m.group(2).strip() + '\n\n',
        text,
        flags=re.S,
    )
    text = re.sub(r'<li>(.*?)</li>', r'\n- \1', text, flags=re.S)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'</?(p|ul|ol)>', '\n\n', text)
    return text


def _inline(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<![\w*])\*([^*\n]+?)\*(?![\w*])', r'<em>\1</em>', text)
    return text


@register.filter
def render_plan(value):
    if not value:
        return ''

    lines = html.escape(_to_markdown(str(value)), quote=False).split('\n')
    out = []
    paragraph = []
    items = []

    def flush():
        if paragraph:
            out.append('<p>' + '<br>'.join(paragraph) + '</p>')
            paragraph.clear()
        if items:
            out.append('<ul>' + ''.join(f'<li>{item}</li>' for item in items) + '</ul>')
            items.clear()

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            flush()
            continue

        if _RULE.match(stripped):
            flush()
            out.append('<hr>')
            continue

        heading = _HEADING.match(stripped)
        if heading:
            flush()
            level = len(heading.group(1))
            out.append(f'<h{level}>{_inline(heading.group(2))}</h{level}>')
            continue

        bold_line = _BOLD_LINE.match(stripped)
        if bold_line:
            flush()
            out.append(f'<h3>{bold_line.group(1).strip()}</h3>')
            continue

        bullet = _BULLET.match(line)
        if bullet:
            if paragraph:
                flush()
            items.append(_inline(bullet.group(1).strip()))
            continue

        # Indented text under a bullet continues that bullet
        if items and line.startswith((' ', '\t')):
            items[-1] += '<br>' + _inline(stripped)
            continue

        if items:
            flush()
        paragraph.append(_inline(stripped))

    flush()
    return mark_safe('\n'.join(out))
