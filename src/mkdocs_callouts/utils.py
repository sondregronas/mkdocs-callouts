import re

CALLOUT_BLOCK_REGEX = re.compile(r'^ ?(>+) *\[!([^\]]*)\]([\-\+]?)(.*)?')
# (1): indents (all leading '>' symbols)
# (2): callout type ([!'capture'] or [!'capture | attribute'] excl. brackets and leading !)
# (3): foldable token (+ or - or <blank>)
# (4): title

CALLOUT_CONTENT_SYNTAX_REGEX = re.compile(r'^ ?(>+) ?')
# (1): indents (all leading '>' symbols)


class CalloutParser:
    # From https://help.obsidian.md/How+to/Use+callouts#Types
    aliases = {
        'abstract': ['summary', 'tldr'],
        'tip':      ['hint', 'important'],
        'success':  ['check', 'done'],
        'question': ['help', 'faq'],
        'warning':  ['caution', 'attention'],
        'failure':  ['fail', 'missing'],
        'danger':   ['error'],
        'quote':    ['cite']
    }
    alias_tuples = [(alias, c_type) for c_type, aliases in aliases.items() for alias in aliases]

    def __init__(self, convert_aliases: bool = True):
        self.active_callout: bool = False
        self.convert_aliases: bool = convert_aliases

    def _parse_block_syntax(self, block) -> str:
        """Converts the callout syntax from obsidian into the mkdocs syntax
        Takes an argument block, which is a regex match.
        """
        # Group 1: Leading > symbols (indentation, for nested callouts)
        indent = block.group(1).count('>')
        indent = '\t' * (indent - 1)

        # Group 2: Callout block type (note, warning, info, etc.) + inline block syntax
        c_type = block.group(2).lower()
        c_type = re.sub(r' *\| *(inline|left) *$', ' inline', c_type)
        c_type = re.sub(r' *\| *(inline end|right) *$', ' inline end', c_type)
        c_type = re.sub(r' *\|.*', '', c_type)
        # Convert aliases, if enabled
        if self.convert_aliases:
            c_type = self._convert_aliases(c_type)

        # Group 3: Foldable callouts
        syntax = {'-': '???', '+': '???+'}
        syntax = syntax.get(block.group(3), '!!!')

        # Group 4: Title, add leading whitespace and quotation marks, if it exists
        title = block.group(4).strip()
        title = f' "{title}"' if title else ''

        # Construct the new callout syntax ({indent}!!! note "Title")
        return f'{indent}{syntax} {c_type}{title}'

    @staticmethod
    def _convert_aliases(c_type: str) -> str:
        """Converts aliases to their respective callout type, if its enabled"""
        for alias, identifier in CalloutParser.alias_tuples:
            c_type = re.sub(rf'^{alias}\b', identifier, c_type)
        return c_type

    def _convert_block(self, line: str) -> str:
        """Calls parse_block_syntax if regex matches, which returns a converted callout block"""
        match = re.search(CALLOUT_BLOCK_REGEX, line)
        if match:
            self.active_callout = True
            return self._parse_block_syntax(match)

    def _convert_content(self, line: str) -> str:
        """
        Converts the callout content by replacing leading '>' symbols with '\t'.

        Will return the original line if active_callout is false or if line is missing leading '>' symbols.
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
        returns _convert_block if line matches that of a callout block syntax,
        if line is not a block syntax, it will return _convert_content.
        """
        return self._convert_block(line) or self._convert_content(line)

    def parse(self, markdown: str) -> str:
        """Takes a markdown file input returns a version with converted callout syntax"""
        self.active_callout = False  # Reset (redundant in conjunction with mkdocs)
        # If markdown file does not contain a callout, skip it
        if not re.search(r'> *\[!', markdown):
            return markdown
        # Convert markdown line by line, then return it
        return '\n'.join(self.convert_line(line) for line in markdown.split('\n'))
