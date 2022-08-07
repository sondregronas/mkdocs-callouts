from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mkdocs-callouts',
    version='1.6.0',
    description="A simple plugin that converts Obsidian style callouts and converts them into mkdocs supported 'admonitions' (a.k.a. callouts).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='mkdocs markdown callouts admonitions obsidian',
    url='https://github.com/sondregronas/mkdocs-callouts',
    author='Sondre Grønås',
    author_email='mail@sondregronas.com',
    license='AGPLv3',
    python_requires='>=3.6',
    install_requires=['mkdocs>=1'],
    tests_require=["pytest"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={'mkdocs.plugins': [
        'callouts = mkdocs_callouts.plugin:CalloutsPlugin']}
)
