import re


def parse_callout_title(line: str, nb: int):
    title = re.search(r'^( ?>*)*\[!(.*)\]', line)
    rest_line = re.sub(r'^( ?>*)*\[!(.*)\][\+\-]?', '', line)
    title = title.group(2).lower()
    if ']-' in line:
        title = '??? ' + title
    elif ']+' in line:
        title = '???+ ' + title
    else:
        title = '!!! ' + title
    if len(rest_line) > 1:
        title = title + ' "' + rest_line.strip() + '"'
    if nb > 1:
        title = '\t' * (nb-1) + title
    return title
