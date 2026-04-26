# Markdown Compiler Agent Instructions

Your task is to implement a markdown compiler in Python.

## What to build

Create a file called `markdown_compiler.py` that converts markdown to HTML.

It must support:
- Headings: `# H1`, `## H2`, `### H3`
- Bold: `**text**`
- Italic: `*text*`
- Unordered lists: `- item`
- Paragraphs: plain text separated by blank lines
- Links: `[text](url)`

## Requirements
- The main function should be called `compile(markdown)` and return HTML as a string
- Every function must have doctests
- All doctests must pass
- Code must be flake8 compliant

## Example
Input:
# Hello
**bold** and *italic*

Output:
<h1>Hello</h1>
<p><strong>bold</strong> and <em>italic</em></p>
