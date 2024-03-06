from django import template
from django.utils.html import mark_safe
import re

register = template.Library()

@register.filter
def convert_steam_tags(text):
    # Replace [h1] with <h1>
    text = re.sub(r'\[h1\]', r'<h1>', text)

    # Replace [/h1] with </h1>
    text = re.sub(r'\[\/h1\]', r'</h1>', text)

    # Replace [h2] with <h2>
    text = re.sub(r'\[h2\]', r'<h2>', text)

    # Replace [/h2] with </h2>
    text = re.sub(r'\[\/h2\]', r'</h2>', text)

    # Replace [h3] with <h3>
    text = re.sub(r'\[h3\]', r'<h3>', text)

    # Replace [/h3] with </h3>
    text = re.sub(r'\[\/h3\]', r'</h3>', text)

    # Replace [url=https://www.dota2.com/patches/7.35b] with <a href=https://www.dota2.com/patches/7.35b>
    text = re.sub(r'\[url=([^\]]+)\]', r'<a href=\1>', text)

    # Handle special case for [url] tags with [img] inside
    img_inside_url_pattern = re.compile(r'\[url=([^\]]+)\](.*?\[img\].*?\[/img\].*?)\[/url\]')
    text = img_inside_url_pattern.sub(r'\2', text)

    # Replace [url] without [img] to <a>
    text = re.sub(r'\[url=([^\]]+)\](?![^\[]*\[img\])[^\[]*\[/url\]', r'<a href=\1>', text)

    # Replace [/url] only if there is no [img] inside
    text = re.sub(r'\[\/url\](?![^\[]*\[img\])', r'</a>', text)

    # Replace [list] with <ul>
    text = re.sub(r'\[list\]', r'<ul>', text)
    text = re.sub(r'\[/list\]', r'</ul>', text)

    # Replace [*] with <li>
    text = re.sub(r'\[\*\]', r'<li>', text)

    # Replace [b] with <h3>
    text = re.sub(r'\[b\]', r'<h3>', text)

    # Replace [/b] with </h3>
    text = re.sub(r'\[\/b\]', r'</h3>', text)

    # Replace [img] with <img>
    text = re.sub(r'\[img\](.*?)\[/img\]', r'<img src=\1>', text)
    
    text = re.sub(r'\[i\]', r'<strong>', text)

    # Replace [/i] with </strong>
    text = re.sub(r'\[\/i\]', r'</strong>', text)
    

    return mark_safe(text)




    



