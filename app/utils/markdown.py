import textwrap
import markdown


def to_markdown(text):
    indented_text = textwrap.indent(text, '> ')

    return markdown.markdown(indented_text)
