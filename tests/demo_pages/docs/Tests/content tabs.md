# Content tabs

Content tabs are very similar to admonitions and use almost the same syntax as them, but you can still write callouts inside them even though you probably should just use the original admonition syntax in this context. However, both will work.

See https://squidfunk.github.io/mkdocs-material/reference/content-tabs/#usage 

(https://github.com/sondregronas/mkdocs-callouts/issues/11)


=== "rendered"

    > [!note] Custom title here
    > Lorem ipsum dolor sit amet, consectetur adipiscing elit.

=== "source"

    ```md
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

        ```md
        > [!note]
        > Content

        > [!note]- Collapsed
        > Content
        
        > [!note]+ Expanded
        > Content
        ```

## Source

```md
=== "rendered"

    > [!note] Custom title here
    > Lorem ipsum dolor sit amet, consectetur adipiscing elit.

=== "source"

    ```md
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

        ```md
        > [!note]
        > Content

        > [!note]- Collapsed
        > Content
        
        > [!note]+ Expanded
        > Content
        ```
```