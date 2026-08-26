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
