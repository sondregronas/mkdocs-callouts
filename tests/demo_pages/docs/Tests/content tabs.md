# Content tabs

See https://squidfunk.github.io/mkdocs-material/reference/content-tabs/#usage 

(https://github.com/sondregronas/mkdocs-callouts/issues/11)


=== "rendered"

    > [!note] Custom title here
    > Lorem ipsum dolor sit amet, consectetur adipiscing elit.

=== "source"

    ``` markdown
    > [!note] Custom title here
    > Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    ```

!!! question "How to use"

    Some text

    Look here:

    ===! "rendered"

        > [!note]
        > Content

        > [!note]- Collapsed
        > Content
        
        > [!note]+ Expanded
        > Content

    === "source"

        ``` md
        > [!note]
        > Content

        > [!note]- Collapsed
        > Content
        
        > [!note]+ Expanded
        > Content
        ```