from django import template
import re
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def highlight_yellow(text, search_term):
    if text is not None and search_term:
        text = str(text)
        src_str = re.compile(re.escape(search_term), re.IGNORECASE)
        str_replaced = src_str.sub(
            lambda m: f'<span class="highlight">{m.group()}</span>', text
        )
        return mark_safe(str_replaced)
    return text


@register.filter()
def smart_truncate(text, search_term, length=200):
    if not text or not search_term:
        return text

    text = str(text)
    search_pos = text.lower().find(search_term.lower())

    if search_pos == -1:
        return text[:length] + '...' if len(text) > length else text

    start = max(0, search_pos - 20)
    end = min(len(text), start + length)

    result = text[start:end]

    if start > 0:
        result = '...' + result
    if end < len(text):
        result = result + '...'

    return result
