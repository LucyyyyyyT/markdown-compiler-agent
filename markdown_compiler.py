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
    match = re.match(r'^(#{1,3}) (.+)$', line)
    if match:
        hashes = match.group(1)
        text = match.group(2)
        level = len(hashes)
        return '<h' + str(level) + '>' + text + '</h' + str(level) + '>'
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
    pattern = re.compile(r'\*\*(.+?)\*\*')
    return pattern.sub(r'<strong>\1</strong>', text)


def compile_italic(text):
    """Convert markdown italic syntax to HTML.

    >>> compile_italic('*italic*')
    '<em>italic</em>'
    >>> compile_italic('text *italic* more')
    'text <em>italic</em> more'
    >>> compile_italic('no italic here')
    'no italic here'
    """
    pattern = re.compile(r'\*(.+?)\*')
    return pattern.sub(r'<em>\1</em>', text)


def compile_link(text):
    """Convert markdown link syntax to HTML.

    >>> compile_link('[Google](https://google.com)')
    '<a href="https://google.com">Google</a>'
    >>> compile_link('Visit [here](url) now')
    'Visit <a href="url">here</a> now'
    >>> compile_link('no link here')
    'no link here'
    """
    pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    return pattern.sub(r'<a href="\2">\1</a>', text)


def compile_inline(text):
    """Convert all inline markdown elements to HTML.

    >>> compile_inline('**bold** and *italic*')
    '<strong>bold</strong> and <em>italic</em>'
    >>> compile_inline('[link](url)')
    '<a href="url">link</a>'
    >>> compile_inline('plain text')
    'plain text'
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
    match = re.match(r'^- (.+)$', line)
    if match:
        content = compile_inline(match.group(1))
        return '<li>' + content + '</li>'
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
    return line.startswith('- ')


def is_heading(line):
    """Check if a line is a heading.

    >>> is_heading('# Hello')
    True
    >>> is_heading('not a heading')
    False
    >>> is_heading('')
    False
    """
    return bool(re.match(r'^#{1,3} ', line))


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
    >>> compile('- one')
    '<ul><li>one</li></ul>'
    >>> compile('hello')
    '<p>hello</p>'
    >>> compile('')
    ''
    >>> compile('# Hello' + '\\n' + '**bold** and *italic*')
    '<h1>Hello</h1><p><strong>bold</strong> and <em>italic</em></p>'
    >>> compile('- a' + '\\n' + '- b')
    '<ul><li>a</li><li>b</li></ul>'
    >>> compile('p1' + '\\n' + '\\n' + 'p2')
    '<p>p1</p><p>p2</p>'
    """
    if not markdown:
        return ''
    if not markdown.strip():
        return ''

    lines = markdown.split('\n')
    output = []
    idx = 0

    while idx < len(lines):
        line = lines[idx]

        if not line.strip():
            idx += 1
            continue

        if is_heading(line):
            output.append(compile_heading(line))
            idx += 1
            continue

        if is_list_item(line):
            list_items = []
            while idx < len(lines) and is_list_item(lines[idx]):
                list_items.append(compile_list_item(lines[idx]))
                idx += 1
            output.append('<ul>' + ''.join(list_items) + '</ul>')
            continue

        para_lines = []
        while idx < len(lines):
            current = lines[idx]
            if not current.strip():
                break
            if is_heading(current):
                break
            if is_list_item(current):
                break
            para_lines.append(current)
            idx += 1

        if para_lines:
            para_text = ' '.join(para_lines)
            para_text = compile_inline(para_text)
            output.append('<p>' + para_text + '</p>')

    return ''.join(output)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
