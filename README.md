# mkdocs-callouts
[![Build Status](https://img.shields.io/github/workflow/status/sondregronas/mkdocs-callouts/CI)](https://github.com/sondregronas/mkdocs-callouts/)
[![GitHub latest commit](https://img.shields.io/github/last-commit/sondregronas/mkdocs-callouts)](https://github.com/sondregronas/mkdocs-callouts/commit/)
[![PyPi](https://img.shields.io/pypi/v/mkdocs-callouts)](https://pypi.org/project/mkdocs-callouts/)
[![AGPLv3 license](https://img.shields.io/github/license/sondregronas/mkdocs-callouts)](https://www.gnu.org/licenses/agpl-3.0.en.html)
[![Buymeacoffee](https://badgen.net/badge/icon/buymeacoffee?icon=buymeacoffee&label)](https://www.buymeacoffee.com/u92RMis)

A simple plugin that converts Obsidian style callouts and converts them into mkdocs supported 'admonitions' (a.k.a. callouts).

## Setup
Install the plugin using pip:

`pip install mkdocs-callouts`

Activate the plugin in `mkdocs.yml`, note that the markdown_extensions `nl2br`, `admonition` and `pymdownx.details` are required for this plugin to render correctly:

```yaml
markdown_extensions:
  - nl2br
  - admonition
  - pymdownx.details

plugins:
  - search
  - callouts
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

## Usage
mkdocs-callouts converts the following:
```
> [!INFO] Title
> An information callout from Obsidian
> inspired by the syntax from the Microsoft Docs
```
and turns it into:
```
!!! info "Title"
    An admonition block for MkDocs.
    Allowing you to edit your notes
    with confidence using Obsidian.
```

Foldable blocks are also supported. (`> [!INFO]- Foldable closed by default`, `> [!INFO]+ Foldable open by default`)
