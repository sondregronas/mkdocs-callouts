from mkdocs_callouts.utils import CalloutParser


def test_title_from_first_bold():
    parser = CalloutParser(title_from_first_bold=True)

    mkdown = "> [!INFO]\n> **Bold Title**\n> Text"
    result = '!!! info "Bold Title"\n\tText'

    assert parser.parse(mkdown) == result

    mkdown = "> [!INFO]\n> **Bold Title** and more text\n> Text"
    result = "!!! info\n\t**Bold Title** and more text\n\tText"

    assert parser.parse(mkdown) == result

    mkdown = "> [!INFO] No bold title\n> Text"
    result = '!!! info "No bold title"\n\tText'

    assert parser.parse(mkdown) == result


def test_no_content():
    parser = CalloutParser(title_from_first_bold=True)

    mkdown = "> [!INFO]"
    result = "!!! info"

    assert parser.parse(mkdown) == result


def test_nested_callouts():
    parser = CalloutParser(title_from_first_bold=True)

    mkdown = ">[!INFO]-\n> Folded content\n>>[!INFO]+\n>> Folded content"
    result = "??? info\n\tFolded content\n\t???+ info\n\t\tFolded content"

    assert parser.parse(mkdown) == result

    mkdown = ">[!INFO]-\n> **Bold Title**\n> Folded content\n>>[!INFO]+\n>> **Bold Title 2**\n>> Folded content"
    result = '??? info "Bold Title"\n\tFolded content\n\t???+ info "Bold Title 2"\n\t\tFolded content'

    assert parser.parse(mkdown) == result


def test_multiple_blocks():
    parser = CalloutParser(title_from_first_bold=True)

    mkdown = "> [!INFO]\n> [!WARNING]\n> **Bold Title**\n> Text"
    result = '!!! info\n!!! warning "Bold Title"\n\tText'
    assert parser.parse(mkdown) == result

    mkdown = "> [!INFO]\n>> [!WARNING]\n>>> [!DANGER]\n>>> **Bold Title**\n>>> Text"
    result = '!!! info\n\t!!! warning\n\t\t!!! danger "Bold Title"\n\t\t\tText'
    assert parser.parse(mkdown) == result

    mkdown = "> [!INFO]\n>> [!WARNING]\n>> **Bold Title**\n>>> [!DANGER]\n>>> **Bold Title**\n>>> Text"
    result = (
        '!!! info\n\t!!! warning "Bold Title"\n\t\t!!! danger "Bold Title"\n\t\t\tText'
    )
    assert parser.parse(mkdown) == result


def test_false_positive_bold():
    parser = CalloutParser(title_from_first_bold=True)

    mkdown = "> [!INFO]\n>> [!WARNING]\n> **Not A Bold Title**"
    result = "!!! info\n\t!!! warning\n\t**Not A Bold Title**"
    assert parser.parse(mkdown) == result

    mkdown = "> [!INFO]\n>> [!WARNING]\n>>> **A bolded blockquote**"
    result = "!!! info\n\t!!! warning\n\t\t> **A bolded blockquote**"
    assert parser.parse(mkdown) == result