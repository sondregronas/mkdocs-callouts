import re

CALLOUT_BLOCK_REGEX = re.compile(r'^(\s*)((?:> ?)+) *\[!([^\]]*)\]([\-\+]?)(.*)?')
# (1): leading whitespace (all tabs and 4x spaces get reused)
# (2): indents (all leading '>' symbols)
# (3): callout type ([!'capture'] or [!'capture | attribute'] excl. brackets and leading !)
# (4): foldable token (+ or - or <blank>)
# (5): title

CALLOUT_CONTENT_SYNTAX_REGEX = re.compile(r'^(\s*)((?:> ?)+)')
# (1): leading whitespace (all tabs and 4x spaces get reused)
# (2): indents (all leading '>' symbols)


class CalloutParser:
    """Class to parse callout blocks from markdown and convert them to mkdocs supported admonitions."""
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

    def __init__(self, convert_aliases: bool = True, breakless_lists: bool = True):
        # Stack to keep track of the current indentation level
        self.indent_levels: list[int] = list()
        # Whether to convert aliases or not
        self.convert_aliases: bool = convert_aliases

        # Breakless list allow for lists to be created without a blank line between them
        # (Obsidian's default behavior, but not within the scope of the CommonMark spec)
        self.breakless_lists: bool = breakless_lists
        # Flags to keep track of the previous line's content for breakless list handling
        self.text_in_prev_line: bool = False
        self.list_in_prev_line: bool = False

        # Check that the callout isn't inside a codefence
        self.in_codefence: bool = False

    def _parse_block_syntax(self, block) -> str:
        """
        Converts the callout syntax from obsidian into the mkdocs syntax
        Takes an argument block, which is a regex match.
        """
        # Group 1: Leading whitespace (we need to reuse tabs and 4x spaces)
        whitespace = block.group(1).replace('    ', '\t')
        whitespace = re.sub(r'[^\t]', '', whitespace)

        # Group 2: Leading > symbols (indentation, for nested callouts)
        indent = block.group(2).count('>')
        indent = '\t' * (indent - 1)

        # Group 3: Callout block type (note, warning, info, etc.) + inline block syntax
        c_type = block.group(3).lower()
        c_type = re.sub(r' *\| *(inline|left) *$', ' inline', c_type)
        c_type = re.sub(r' *\| *(inline end|right) *$', ' inline end', c_type)
        c_type = re.sub(r' *\|.*', '', c_type)
        # Convert aliases, if enabled
        if self.convert_aliases:
            c_type = self._convert_aliases(c_type)

        # Group 4: Foldable callouts
        syntax = {'-': '???', '+': '???+'}
        syntax = syntax.get(block.group(4), '!!!')

        # Group 5: Title, add leading whitespace and quotation marks, if it exists
        title = block.group(5).strip()
        title = f' "{title}"' if title else ''

        # Construct the new callout syntax ({indent}!!! note "Title")
        return f'{whitespace}{indent}{syntax} {c_type}{title}'

    @staticmethod
    def _convert_aliases(c_type: str) -> str:
        """Converts aliases to their respective callout type, if its enabled"""
        for alias, identifier in CalloutParser.alias_tuples:
            c_type = re.sub(rf'^{alias}\b', identifier, c_type)
        return c_type

    def _breakless_list_handler(self, line: str) -> str:
        """
        Handles a breakless list by adding a newline if the previous line was text

        This is a workaround for Obsidian's default behavior, which allows for lists to be created
        without a blank line between them.
        """
        is_list = re.search(r'^\s*(?:[-+*]|\d+\.)\s', line)
        if is_list and self.text_in_prev_line:
            # If the previous line was a list, keep the line as is
            if self.list_in_prev_line:
                return line
            # If the previous line was text, add a newline before the list
            indent = re.search(r'^\t*', line).group()
            line = f'{indent}\n{line}'
        else:
            # Set text_in_prev_line according to the current line
            self.text_in_prev_line = line.strip() != ''
        self.list_in_prev_line = is_list
        return line

    def _convert_block(self, line: str) -> str:
        """Calls parse_block_syntax if regex matches, which returns a converted callout block"""
        match = re.search(CALLOUT_BLOCK_REGEX, line)
        if match:
            # Store the current indent level and add it to the list if it doesn't exist
            indent_level = match.group(2).count('>')
            if indent_level not in self.indent_levels:
                self.indent_levels.append(indent_level)
            return self._parse_block_syntax(match)

    def _convert_content(self, line: str) -> str:
        """
        Converts the callout content by replacing leading '>' symbols with '\t'.

        Will return the original line if active_callout is false or if line is missing leading '>' symbols.
        """
        match = re.search(CALLOUT_CONTENT_SYNTAX_REGEX, line)
        if match and self.indent_levels:
            # Group 1: Leading whitespace (we need to reuse tabs and 4x spaces)
            whitespace = match.group(1).replace('    ', '\t')
            whitespace = re.sub(r'[^\t]', '', whitespace)

            # Remove any higher levels whilst the current line
            # has a lower indent level than the last line.
            while match.group(2).count('>') < self.indent_levels[-1]:
                self.indent_levels = self.indent_levels[:-1]
            indent = '\t' * (self.indent_levels[-1] + whitespace.count('\t'))
            line = re.sub(rf'^\s*(?:> ?){{{self.indent_levels[-1]}}} ?', indent, line)

            # Handle breakless lists before returning the line, if enabled
            if self.breakless_lists:
                line = self._breakless_list_handler(line)
        else:
            # Reset the relevant variables
            self.indent_levels = list()
            # These are unused if breakless_lists is disabled
            self.list_in_prev_line = False
            self.text_in_prev_line = False
        return line

    def convert_line(self, line: str) -> str:
        """
        Converts the syntax for callouts to admonitions for a single line of markdown
        returns _convert_block if line matches that of a callout block syntax,
        if line is not a block syntax, it will return _convert_content.
        """
        # Toggle in_codefence if line contains a codefence
        if re.match(r'^\s*```', line):
            # TODO: Might be _almost_ impossible to do, but at the moment having a codefence containing
            #       callout syntax inside a callout block will convert the callout syntax within the codefence.
            #       (Extremely unlikely scenario, but still)
            self.in_codefence = not self.in_codefence
        if self.in_codefence:
            # Reset the indent levels if the callout is inside a codefence
            self.indent_levels = list()
            return line
        return self._convert_block(line) or self._convert_content(line)

    def parse(self, markdown: str) -> str:
        """Takes a markdown file input returns a version with converted callout syntax"""
        self.indent_levels = list()  # Reset (redundant in conjunction with mkdocs)
        # If markdown file does not contain a callout, skip it
        if not re.search(r'> *\[!', markdown):
            return markdown
        # Convert markdown line by line, then return it
        return '\n'.join(self.convert_line(line) for line in markdown.split('\n'))
