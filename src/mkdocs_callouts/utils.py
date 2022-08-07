import re

CALLOUT_BLOCK_REGEX = re.compile(r'^ ?(>+) *\[!([^\]]*)\]([\-\+]?)(.*)?')
# (1): indents (all leading '>' symbols)
# (2): callout type ([!'capture'] or [!'capture | attribute'] excl. brackets and leading !)
# (3): foldable token (+ or - or <blank>)
# (4): title

CALLOUT_CONTENT_SYNTAX_REGEX = re.compile(r'^ ?(>+) ?')
# (1): indents (all leading '>' symbols)


class CalloutParser:
    def __init__(self):
        self.active_callout: bool = False

    @staticmethod
    def _parse_block_syntax(block: re.Match) -> str:
        """Converts the callout syntax from obsidian into the mkdocs syntax"""
        # Group 1: Leading > symbols (indentation, for nested callouts)
        indent = block.group(1).count('>')
        indent = '\t' * (indent - 1)

        # Group 2: Callout block type (note, warning, info, etc.) + inline block syntax
        c_type = block.group(2).lower()
        c_type = re.sub(r' ?\| *(inline|left) *$', ' inline', c_type)
        c_type = re.sub(r' ?\| *(inline end|right) *$', ' inline end', c_type)
        c_type = re.sub(r' ?\|.*', '', c_type)

        # Group 3: Foldable callouts
        syntax = {'-': '???', '+': '???+'}
        syntax = syntax.get(block.group(3), '!!!')

        # Group 4: Title, add leading whitespace and quotation marks, if it exists
        title = block.group(4).strip()
        title = f' "{title}"' if title else ''

        # Construct the new callout syntax ({indent}!!! note "Title")
        return f'{indent}{syntax} {c_type}{title}'

    def _convert_block(self, line: str) -> str:
        """Calls parse_block_syntax if regex matches, which returns a converted callout block"""
        match = re.search(CALLOUT_BLOCK_REGEX, line)
        if match:
            self.active_callout = True
            return self._parse_block_syntax(match)

    def _convert_content(self, line: str) -> str:
        """
        Converts the callout content by replacing leading '>' symbols with '\t'.

        Will return the original line if active_callout is false or line is missing leading '>' symbols.
        """
        match = re.search(CALLOUT_CONTENT_SYNTAX_REGEX, line)
        if match and self.active_callout:
            indent = '\t' * match.group(1).count('>')
            line = re.sub(CALLOUT_CONTENT_SYNTAX_REGEX, indent, line)
        else:
            self.active_callout = False
        return line

    def convert_line(self, line: str) -> str:
        """
        Converts the syntax for callouts to admonitions for a single line of markdown
        Calls _convert_block if line matches that of a callout block syntax,
        if line is not a block syntax, it will call _convert_content.
        """
        block = self._convert_block(line)
        return block if block else self._convert_content(line)

    def parse(self, markdown: str) -> str:
        """Takes a markdown file input returns a version with converted callout syntax"""
        self.active_callout = False  # Reset (doesn't matter for mkdocs)
        # If markdown file does not contain a callout, skip it
        if not re.search(r'> *\[!', markdown):
            return markdown
        # Convert markdown line by line, then return it
        return '\n'.join(self.convert_line(line) for line in markdown.split('\n'))
