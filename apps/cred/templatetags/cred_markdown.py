from django import template
from django.utils.html import format_html
import markdown

register = template.Library()


@register.simple_tag
def markdown_cred(description):
    out = markdown.markdown(
        text=description,
        extensions=[
            'fenced_code',
            'nl2br',
            'tables',
        ],
        safe_mode='escape',
    )

    return format_html(out)
