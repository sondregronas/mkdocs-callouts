# Callouts in nested codefences

Not a typical usecase, but if you have a codefence inside of a codefence containing a callout, the callout inside the nested codefence will be converted.

A solution would be to capture and keep track of which level we enter / leave a codefence.

```md
> [!NOTE] Callout syntax
> ```md
> > [!WARNING]
> > This is a warning inside a codefence
> ```

Without the codefence:

> [!NOTE] Callout syntax
> > [!WARNING]
> > This is a warning inside a blockquote
```