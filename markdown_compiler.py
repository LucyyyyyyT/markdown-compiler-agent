"""Markdown to HTML compiler."""
import re


def compile_heading(line):
    """Convert a markdown heading to HTML.

    >>> compile_heading('# Hello')
    '<h1>Hello</h1>'
    >>> compile_heading('## World')
    '<h2>World</h2>'
    >>> compile_heading('### Test')
    '<h3>Test</h3>'
    >>> compile_heading('Not a heading') is None
    True
    """
    match = re.match(r'^(#{1,3})\s+(.+)$', line)
    if match:
        level = len(match.group(1))
        text = match.group(2)
        return '<h{0}>{1}</h{0}>'.format(level, text)
    return None


def compile_bold(text):
    """Convert markdown bold syntax to HTML.

    >>> compile_bold('**bold**')
    '<strong>bold</strong>'
    >>> compile_bold('text **bold** more')
    'text <strong>bold</strong> more'
    >>> compile_bold('no bold here')
    'no bold here'
    """
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)


def compile_italic(text):
    """Convert markdown italic syntax to HTML.

    >>> compile_italic('*italic*')
    '<em>italic</em>'
    >>> compile_italic('text *italic* more')
    'text <em>italic</em> more'
    >>> compile_italic('no italic here')
    'no italic here'
    """
    return re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)


def compile_link(text):
    """Convert markdown link syntax to HTML.

    >>> compile_link('[Google](https://google.com)')
    '<a href="https://google.com">Google</a>'
    >>> compile_link('Visit [here](url) now')
    'Visit <a href="url">here</a> now'
    >>> compile_link('no link here')
    'no link here'
    """
    return re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)


def compile_inline(text):
    """Convert all inline markdown elements to HTML.

    >>> compile_inline('**bold** and *italic*')
    '<strong>bold</strong> and <em>italic</em>'
    >>> compile_inline('[link](url)')
    '<a href="url">link</a>'
    >>> compile_inline('**bold** *italic* [link](url)')
    '<strong>bold</strong> <em>italic</em> <a href="url">link</a>'
    """
    text = compile_link(text)
    text = compile_bold(text)
    text = compile_italic(text)
    return text


def compile_list_item(line):
    """Convert a markdown list item to HTML.

    >>> compile_list_item('- item')
    '<li>item</li>'
    >>> compile_list_item('- **bold** item')
    '<li><strong>bold</strong> item</li>'
    >>> compile_list_item('not a list') is None
    True
    """
    match = re.match(r'^-\s+(.+)$', line)
    if match:
        content = compile_inline(match.group(1))
        return '<li>{0}</li>'.format(content)
    return None


def is_list_item(line):
    """Check if a line is a list item.

    >>> is_list_item('- item')
    True
    >>> is_list_item('not a list')
    False
    >>> is_list_item('')
    False
    """
    return bool(re.match(r'^-\s+', line))


def compile(markdown):
    """Convert markdown text to HTML.

    >>> compile('# Hello')
    '<h1>Hello</h1>'
    >>> compile('## World')
    '<h2>World</h2>'
    >>> compile('### Test')
    '<h3>Test</h3>'
    >>> compile('**bold**')
    '<p><strong>bold</strong></p>'
    >>> compile('*italic*')
    '<p><em>italic</em></p>'
    >>> compile('[link](url)')
    '<p><a href="url">link</a></p>'
    >>> compile('- item1' + chr(10) + '- item2')
    '<ul><li>item1</li><li>item2</li></ul>'
    >>> compile('# Hello' + chr(10) + '**bold** and *italic*')
    '<h1>Hello</h1><p><strong>bold</strong> and <em>italic</em></p>'
    >>> compile('para1' + chr(10) + chr(10) + 'para2')
    '<p>para1</p><p>para2</p>'
    >>> compile('')
    ''
    """
    if not markdown.strip():
        return ''

    lines = markdown.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        heading = compile_heading(line)
        if heading:
            result.append(heading)
            i += 1
            continue

        if is_list_item(line):
            list_items = []
            while i < len(lines) and is_list_item(lines[i]):
                list_items.append(compile_list_item(lines[i]))
                i += 1
            result.append('<ul>{0}</ul>'.format(''.join(list_items)))
            continue

        para_lines = []
        while i < len(lines) and lines[i].strip():
            current = lines[i]
            if compile_heading(current) or is_list_item(current):
                break
            para_lines.append(current)
            i += 1

        if para_lines:
            para_text = ' '.join(para_lines)
            para_text = compile_inline(para_text)
            result.append('<p>{0}</p>'.format(para_text))

    return ''.join(result)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
